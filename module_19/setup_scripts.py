import os
import glob

source_dir = 'scripts'
target_dir = 'require_data/script'

os.makedirs(target_dir, exist_ok=True)

for file in glob.glob(os.path.join(source_dir, '*.py')):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change DATA_DIR
    content = content.replace("DATA_DIR = os.path.join(BASE_DIR, 'new_data')", 
                              "DATA_DIR = os.path.join(BASE_DIR, 'require_data', 'data')")
    
    # Inject date filter into the SQL query
    # Find the query string by looking for the second triple quote block which is the query
    # A safer way is to just find `    """` that follows `WHERE` or `GROUP BY`
    # Let's just do a regex replace to insert before the ending triple quote of the query
    
    import re
    # The query is typically ending with a where clause and then `    """`
    # We can replace the specific `    """` that comes right before `with get_connection() as conn:`
    
    content = re.sub(r'(\s+)"""(\s+with get_connection\(\) as conn:)', 
                     r'\1  AND YEAR(c.CI_ADMISSION_DATE) BETWEEN 2021 AND 2026\n\1"""\2', 
                     content)
                     
    # For Pattern 6 CTE: we can also inject it inside the CTE if we want, but injecting at the end is sufficient.
    
    basename = os.path.basename(file)
    target_file = os.path.join(target_dir, basename)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Patched {basename}")
