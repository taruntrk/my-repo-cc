import glob
for file in glob.glob('/home/tarun/Downloads/CC/echs_analysis/module_19/require_data/script/*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix hospital_type join condition
    content = content.replace('ON o.OM_HOSP_TYPE = ht.hos_type_code', 'ON o.OM_HOSP_TYPE = ht.hos_type_id')
    
    # Fix select clause for patient_type
    content = content.replace('c.CI_PATIENT_TYPE as patient_type,', 'pt.PT_TYPE_DESC as patient_type,')
    
    # Add patient_type join if not exists
    if 'LEFT JOIN patient_type pt' not in content:
        content = content.replace(
            'LEFT JOIN user_details ud', 
            'LEFT JOIN patient_type pt ON c.CI_PATIENT_TYPE = pt.PT_TYPE_ID\n    LEFT JOIN user_details ud'
        )
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {file}")
