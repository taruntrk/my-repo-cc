import glob
for file in glob.glob('/home/tarun/Downloads/CC/echs_analysis/module_19/require_data/script/*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('ON c.CI_PATIENT_TYPE = pt.PT_TYPE_ID', 'ON c.CI_PATIENT_TYPE = pt.PT_TYPE_CODE')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed patient join in {file}")
