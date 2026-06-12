import zlib
import re

def parse_cmap(cmap_text):
    glyph_to_char = {}
    
    # Parse beginbfrange
    ranges = re.findall(r'beginbfrange\s*(.*?)\s*endbfrange', cmap_text, re.DOTALL)
    for r_text in ranges:
        for line in r_text.strip().split('\n'):
            parts = re.findall(r'<([0-9a-fA-F]+)>', line)
            if len(parts) == 3:
                start = int(parts[0], 16)
                end = int(parts[1], 16)
                dest = parts[2]
                if len(dest) == 4:
                    dest_val = int(dest, 16)
                    for val in range(start, end + 1):
                        glyph_to_char[val] = chr(dest_val + (val - start))
                elif len(dest) > 4:
                    dest_str = ''.join(chr(int(dest[j:j+4], 16)) for j in range(0, len(dest), 4))
                    for val in range(start, end + 1):
                        glyph_to_char[val] = dest_str
                        
    # Parse beginbfchar
    chars = re.findall(r'beginbfchar\s*(.*?)\s*endbfchar', cmap_text, re.DOTALL)
    for c_text in chars:
        for line in c_text.strip().split('\n'):
            parts = re.findall(r'<([0-9a-fA-F]+)>', line)
            if len(parts) == 2:
                glyph = int(parts[0], 16)
                dest = parts[1]
                dest_str = ''.join(chr(int(dest[j:j+4], 16)) for j in range(0, len(dest), 4))
                glyph_to_char[glyph] = dest_str
                
    return glyph_to_char

def find_text():
    with open('uncompressed_Module_15.pdf', 'rb') as f:
        content = f.read()

    # 1. Parse CMaps
    idx = 0
    cmaps = {}
    while True:
        idx = content.find(b'stream', idx)
        if idx == -1:
            break
        end_idx = content.find(b'endstream', idx)
        if end_idx == -1:
            idx += 6
            continue
        stream_data = content[idx+6:end_idx].strip(b'\r\n')
        obj_idx = content.rfind(b'obj', 0, idx)
        header = content[obj_idx-30:idx]
        decomp = None
        if b'FlateDecode' in header:
            try:
                decomp = zlib.decompress(stream_data)
            except Exception:
                try:
                    decomp = zlib.decompress(stream_data.strip(b'\r\n'))
                except Exception:
                    pass
        else:
            decomp = stream_data
        if decomp and b'begincmap' in decomp:
            cmap_text = decomp.decode('utf-8', errors='ignore')
            obj_id_parts = content[obj_idx-20:obj_idx].split()
            cmap_name = obj_id_parts[-2].decode('ascii') if len(obj_id_parts) >= 2 else str(obj_idx)
            cmaps[cmap_name] = parse_cmap(cmap_text)
        idx += 6

    print(f"DEBUG: Loaded {len(cmaps)} CMaps: {list(cmaps.keys())}")

    # 2. Scan streams and parse TJ operators
    idx = 0
    while True:
        idx = content.find(b'stream', idx)
        if idx == -1:
            break
        end_idx = content.find(b'endstream', idx)
        if end_idx == -1:
            idx += 6
            continue
        stream_data = content[idx+6:end_idx].strip(b'\r\n')
        obj_idx = content.rfind(b'obj', 0, idx)
        header = content[obj_idx-30:idx]
        obj_id_parts = content[obj_idx-20:obj_idx].split()
        obj_id = obj_id_parts[-2].decode('ascii', errors='ignore') if len(obj_id_parts) >= 2 else '0'
        decomp = None
        if b'FlateDecode' in header:
            try:
                decomp = zlib.decompress(stream_data)
            except Exception:
                try:
                    decomp = zlib.decompress(stream_data.strip(b'\r\n'))
                except Exception:
                    pass
        else:
            decomp = stream_data
            
        if decomp and b'begincmap' not in decomp:
            tj_matches = list(re.finditer(rb'\[(.*?)\]\s*TJ', decomp, re.DOTALL))
            for tj in tj_matches:
                tj_content = tj.group(1)
                literals = []
                i = 0
                while i < len(tj_content):
                    if tj_content[i:i+1] == b'(':
                        start_lit = i + 1
                        esc = False
                        i += 1
                        while i < len(tj_content):
                            if esc:
                                esc = False
                            elif tj_content[i:i+1] == b'\\':
                                esc = True
                            elif tj_content[i:i+1] == b')':
                                literals.append(tj_content[start_lit:i])
                                break
                            i += 1
                    i += 1
                
                for cmap_name, cmap in cmaps.items():
                    decoded = ''
                    for lit in literals:
                        lit_bytes = bytearray()
                        k = 0
                        while k < len(lit):
                            if lit[k:k+1] == b'\\':
                                if k + 1 < len(lit):
                                    nxt = lit[k+1:k+2]
                                    if nxt == b'n': lit_bytes.append(10)
                                    elif nxt == b'r': lit_bytes.append(13)
                                    elif nxt == b't': lit_bytes.append(9)
                                    elif nxt == b'b': lit_bytes.append(8)
                                    elif nxt == b'f': lit_bytes.append(12)
                                    else: lit_bytes.extend(nxt)
                                    k += 2
                                else:
                                    lit_bytes.extend(b'\\')
                                    k += 1
                            else:
                                lit_bytes.extend(lit[k:k+1])
                                k += 1
                                
                        if len(lit_bytes) % 2 == 0:
                            for k in range(0, len(lit_bytes), 2):
                                val = int.from_bytes(lit_bytes[k:k+2], 'big')
                                decoded += cmap.get(val, '?')
                                
                    if 'airawat' in decoded.lower():
                        print(f'Obj {obj_id}, TJ: {tj.group(0).decode("utf-8", errors="ignore")}')
                        print(f'  Decoded using CMap {cmap_name}: "{decoded}"')
        idx += 6

if __name__ == "__main__":
    find_text()
