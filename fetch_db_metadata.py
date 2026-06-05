"""
ECHS DB Metadata Fetcher — fixed version.
- Skips tables > 500 MB for exact COUNT (uses approx from information_schema)
- Uses settimeout(300) on SSH channel reads
- Batches of 10, with sub-batch retry of 5 on timeout
"""

import paramiko
import json
import sys

import os
from dotenv import load_dotenv
load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = int(os.getenv('SSH_PORT', 22))
SSH_USER = os.getenv('SSH_USER')
SSH_PASS = os.getenv('SSH_PASS')
DB_USER  = os.getenv('DB_USER')
DB_PASS  = os.getenv('DB_PASS')
DB_NAME  = os.getenv('DB_NAME')

SIZE_LIMIT_MB = 500   # skip exact COUNT(*) on tables larger than this

def run_mysql_stdin(client, sql):
    cmd = f'mysql -u {DB_USER} -p{DB_PASS} {DB_NAME} -B -N'
    stdin_c, stdout, stderr = client.exec_command(cmd, timeout=600)
    stdin_c.write(sql.encode('utf-8'))
    stdin_c.channel.shutdown_write()
    stdout.channel.settimeout(300)   # 5-min read timeout
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    err_lines = [l for l in err.splitlines() if 'Using a password' not in l and l.strip()]
    if err_lines:
        print(f"  [WARN] {' | '.join(err_lines)[:400]}", file=sys.stderr)
    return out

def main():
    print("Connecting to SSH...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASS)
    print("Connected.\n")

    # ── Step 1: Table list with sizes ─────────────────────────────────────────
    print("Fetching table list...")
    meta_sql = """
        SELECT TABLE_NAME,
               COALESCE(TABLE_ROWS, 0)  AS approx_rows,
               COALESCE(DATA_LENGTH, 0) AS data_bytes
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = 'ECHS' AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME;
    """
    raw_tables = run_mysql_stdin(client, meta_sql)
    tables = []
    for line in raw_tables.splitlines():
        p = line.split('\t')
        if len(p) >= 3:
            tables.append({'name': p[0], 'approx_rows': p[1], 'data_bytes': p[2]})
    print(f"  => {len(tables)} tables found.")

    # ── Step 2: All columns ───────────────────────────────────────────────────
    print("Fetching all columns...")
    cols_sql = """
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE,
               COALESCE(COLUMN_KEY,''), COALESCE(EXTRA,''), COALESCE(COLUMN_COMMENT,'')
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'ECHS'
        ORDER BY TABLE_NAME, ORDINAL_POSITION;
    """
    raw_cols = run_mysql_stdin(client, cols_sql)
    col_map = {}
    for line in raw_cols.splitlines():
        p = line.split('\t')
        if len(p) < 3:
            continue
        tbl = p[0]
        col_map.setdefault(tbl, []).append({
            'name':    p[1],
            'dtype':   p[2],
            'key':     p[3] if len(p) > 3 else '',
            'extra':   p[4] if len(p) > 4 else '',
            'comment': p[5] if len(p) > 5 else '',
        })

    # ── Step 3: Build UNION queries, skip giant tables ─────────────────────────
    DATE_TYPES = {'date', 'datetime', 'timestamp'}
    print(f"\nBuilding UNION count+date queries (skipping tables > {SIZE_LIMIT_MB} MB)...")

    parts = []
    skipped_large = []
    for t in tables:
        name     = t['name']
        size_mb  = int(t['data_bytes'] or 0) / 1024 / 1024
        cols     = col_map.get(name, [])
        date_cols = [c['name'] for c in cols if c['dtype'].lower() in DATE_TYPES]
        dc = date_cols[0] if date_cols else None

        if size_mb > SIZE_LIMIT_MB:
            skipped_large.append((name, f'{size_mb:.0f} MB'))
            continue

        if dc:
            parts.append(
                f"SELECT '{name}' AS tbl, COUNT(*) AS cnt, "
                f"CAST(MIN(`{dc}`) AS CHAR) AS mn, CAST(MAX(`{dc}`) AS CHAR) AS mx "
                f"FROM `{name}`"
            )
        else:
            parts.append(
                f"SELECT '{name}' AS tbl, COUNT(*) AS cnt, "
                f"NULL AS mn, NULL AS mx FROM `{name}`"
            )

    print(f"  Querying {len(parts)} tables exactly.")
    if skipped_large:
        print(f"  Skipped {len(skipped_large)} large tables (approx rows used):")
        for name, sz in skipped_large:
            print(f"    - {name}: {sz}")

    # ── Step 4: Run batches ───────────────────────────────────────────────────
    BATCH = 10
    count_map = {}
    total_batches = (len(parts) + BATCH - 1) // BATCH
    for bi, start in enumerate(range(0, len(parts), BATCH)):
        chunk = parts[start:start + BATCH]
        print(f"  Batch {bi+1}/{total_batches} ({len(chunk)} tables)...", end=' ', flush=True)
        try:
            union_sql = '\nUNION ALL\n'.join(chunk) + ';'
            raw = run_mysql_stdin(client, union_sql)
        except Exception as e:
            print(f"timeout ({e}), retrying in sub-batches of 5...")
            raw = ''
            for sub_start in range(0, len(chunk), 5):
                sub = chunk[sub_start:sub_start + 5]
                try:
                    sub_sql = '\nUNION ALL\n'.join(sub) + ';'
                    raw += '\n' + run_mysql_stdin(client, sub_sql)
                except Exception as e2:
                    print(f"    sub-batch failed: {e2}")
        n = 0
        for line in raw.splitlines():
            p = line.split('\t')
            if len(p) >= 4:
                mn = p[2].strip() if p[2].strip() not in ('NULL', 'None', 'null', '') else None
                mx = p[3].strip() if p[3].strip() not in ('NULL', 'None', 'null', '') else None
                count_map[p[0]] = {'cnt': p[1], 'mn': mn, 'mx': mx}
                n += 1
        print(f"got {n} results.")

    client.close()

    # ── Step 5: Assemble results ──────────────────────────────────────────────
    results = []
    for t in tables:
        name     = t['name']
        cols     = col_map.get(name, [])
        date_cols = [c['name'] for c in cols if c['dtype'].lower() in DATE_TYPES]
        cm       = count_map.get(name, {})
        size_mb  = int(t['data_bytes'] or 0) / 1024 / 1024
        results.append({
            'table':         name,
            'row_count':     cm.get('cnt', t['approx_rows']),
            'row_count_exact': name not in [s[0] for s in skipped_large],
            'data_mb':       round(size_mb, 1),
            'columns':       cols,
            'date_col_used': date_cols[0] if date_cols else None,
            'earliest_date': cm.get('mn'),
            'latest_date':   cm.get('mx'),
        })

    out_path = '/home/aman/Desktop/echs_analysis/echs_db_metadata.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDone. {len(results)} tables saved to {out_path}")

if __name__ == '__main__':
    main()
