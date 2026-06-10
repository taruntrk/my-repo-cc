import pymysql

def get_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="aman",
        password="aman@2026",
        database="ECHS",
        cursorclass=pymysql.cursors.DictCursor
    )

query = """
    SELECT 
        c.CI_INTIMATION_ID as claim_id,
        YEAR(c.CI_ADMISSION_DATE) as claim_year,
        c.CI_HOSPITAL_ID as hospital_id,
        o.OM_OFFICE_NAME as registered_hospital_name,
        o.OM_OFFICE_CITY as hospital_city,
        st.SM_STATE_NAME as hospital_state,
        crm.CRM_CITY_NAME as cghs_region,
        ht.hos_type_description as hospital_type,
        
        pt.PT_TYPE_DESC as patient_type,
        c.CI_ADM_AILMENT as admission_ailment,
        
        cs.CS_GR_CLAIM_AMT as billed_amount,
        cs.CS_UTI_APP_AMT as approved_amount,
        (cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT) as deducted_amount,
        ((cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT) / cs.CS_GR_CLAIM_AMT) * 100 as deduction_percentage
    FROM claim_intimation c
    INNER JOIN claim_submission cs ON c.CI_INTIMATION_ID = cs.CS_INTIMATION_ID
    LEFT JOIN patient_type pt ON c.CI_PATIENT_TYPE = pt.PT_TYPE_ID
    LEFT JOIN user_details ud ON c.CI_HOSPITAL_ID = ud.UD_USER_ID
    LEFT JOIN office_master o ON ud.UD_OFFICE_ID = o.OM_OFFICE_ID
    LEFT JOIN state_master st ON o.OM_OFFICE_STATE_ID = st.SM_STATE_ID
    LEFT JOIN hos_types ht ON o.OM_HOSP_TYPE = ht.hos_type_id
    LEFT JOIN cghs_region_master crm ON o.OM_OFFICE_CGHS_CITY_ID = crm.CRM_CITY_ID
    WHERE cs.CS_GR_CLAIM_AMT > 0
      AND ((cs.CS_GR_CLAIM_AMT - cs.CS_UTI_APP_AMT) / cs.CS_GR_CLAIM_AMT) > 0.50
      AND YEAR(c.CI_ADMISSION_DATE) BETWEEN 2021 AND 2026
    LIMIT 5
"""

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute(query)
        print(cur.fetchall())
