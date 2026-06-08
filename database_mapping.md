# ECHS Database Schema & Sizing Mapping

This document contains the structural mapping of all tables in the `ECHS` database, including their approximate row counts, storage size on disk, and column definitions.

## Tier 1: Massive Tables (> 100 MB) (Total: 60)
### `claim_remarks`
- **Rows:** 368652560
- **Size:** 93359.97 MB
- **Columns:** `CR_INTIMATION_ID [varchar]`, `CR_USER_ID [varchar]`, `CR_USER_REMARKS [text]`, `CR_UPDATE_DATE [datetime]`, `CR_INT_STAGE [varchar]`, `CR_REMARK_ID [varchar]`, `CR_INT_STATUS [varchar]`, `CR_HISTORY_ID [int]`, `CR_ENHANCE_ID [int]`, `CR_IP_ADDRESS [varchar]`, `CR_AUTO_UPDATE [varchar]`, `CR_CHANGE_ID [int]`, `CR_REQUEST_ID [int]`

### `hosp_exp_det`
- **Rows:** 193941437
- **Size:** 53547.00 MB
- **Columns:** `HED_INTIMATION_ID [varchar]`, `HED_EXP_ID [varchar]`, `HED_CAT_ID [varchar]`, `HED_CAT_SUB_ID [varchar]`, `HED_REGION_ID [varchar]`, `HED_ACT_RATE [decimal]`, `HED_HOS_RATE [decimal]`, `HED_CLAIM_UNITS [decimal]`, `HED_CLAIM_AMOUNT [decimal]`, `HED_PAR_AMOUNT [decimal]`, `HED_SUP_AMOUNT [decimal]`, `HED_APP_AMOUNT [decimal]`, `HED_PAR_DEDUCT [decimal]`, `HED_SUPER_RATE [varchar]`, `HED_RATE_TYPE [varchar]`, `HED_PROC_DESC [text]`, `HED_PROC_TYPE [varchar]`, `HED_CAT_DESC [text]`, `HED_PAR_REMARKS [text]`, `HED_SUPER_REMARKS [text]`, `HED_HOS_REMARKS [text]`, `HED_ID [decimal]`, `HED_ID_SRNO [int]`, `HED_PROC_ID [int]`, `HED_SUP_DEDUCT [decimal]`, `HED_APP_DEDUCT [decimal]`, `HED_APP_REMARKS [text]`, `HED_NORMAL_RATE [decimal]`, `HED_SPEC_RATE [decimal]`, `HED_DED_ID [int]`

### `document_submitted`
- **Rows:** 244434406
- **Size:** 40493.00 MB
- **Columns:** `DS_INTIMATION_ID [varchar]`, `DS_DOCTYPE_ID [varchar]`, `DS_DOC_ID [varchar]`, `DS_REMARK [text]`, `DS_FILENAME [varchar]`, `DS_FILE_SR_NO [int]`, `DS_IS_RECEIVED [varchar]`, `DS_REC_REMARK [text]`, `DS_REC_REMARK_ID [varchar]`, `DS_MUL_DOC [varchar]`, `DS_DOC_SUBMITTED [varchar]`, `DS_DOC_COUNT [int]`, `DS_DOC_SUBMIT_BY [varchar]`, `DS_ENHANCE_ID [int]`, `DS_SUBMIT_TIME [datetime]`, `DS_FILE_SIZE [decimal]`, `DS_SIGNED [int]`

### `audit_remarks`
- **Rows:** 263352880
- **Size:** 28711.00 MB
- **Columns:** `AR_INTIMATION_ID [varchar]`, `AR_REM_TYPE_ID [varchar]`, `AR_HOS_REMARK [text]`, `AR_PAR_REMARK [text]`, `AR_SUP_REMARK [text]`, `AR_APP_REMARK [text]`

### `settlement_details`
- **Rows:** 33450569
- **Size:** 26963.00 MB
- **Columns:** `SD_INTIMATION_ID [varchar]`, `SD_SUB_ENTITY_ID [varchar]`, `SD_SUB_OFFICE_ID [varchar]`, `SD_OFFICE_NAME [varchar]`, `SD_OFFICE_ADD1 [varchar]`, `SD_OFFICE_ADD2 [varchar]`, `SD_OFFICE_ADD3 [varchar]`, `SD_OFFICE_CITY [varchar]`, `SD_OFFICE_STATE_ID [varchar]`, `SD_OFFICE_STATE [varchar]`, `SD_OFFICE_PIN [varchar]`, `SD_OFFICE_PAN [varchar]`, `SD_BANK_ID [varchar]`, `SD_BANK_NAME [varchar]`, `SD_BANK_BRANCH [varchar]`, `SD_BANK_ADD1 [varchar]`, `SD_BANK_ADD2 [varchar]`, `SD_BANK_ADD3 [varchar]`, `SD_BANK_CITY [varchar]`, `SD_BANK_STATE_ID [varchar]`, `SD_BANK_STATE [varchar]`, `SD_BANK_PIN [varchar]`, `SD_BANK_ACTYPE [varchar]`, `SD_BANK_ACNO [varchar]`, `SD_BANK_MICR [varchar]`, `SD_BANK_IFSC [varchar]`, `SD_PAY_MODE [varchar]`, `SD_CLAIM_AMT [decimal]`, `SD_UTI_APP_AMT [decimal]`, `SD_ACCEPT_DATE [datetime]`, `SD_SETTLE_DATE [datetime]`, `SD_CGHS_DIS_PER [decimal]`, `SD_CGHS_DIS_AMT [decimal]`, `SD_RECOUP_CLAIM_AMT [decimal]`, `SD_HOS_SER_RATE [decimal]`, `SD_HOS_SER [decimal]`, `SD_HOS_ECESS [decimal]`, `SD_HOS_HSCESS [decimal]`, `SD_HOS_TOT_TAX [decimal]`, `SD_HOS_UTI_FEE [decimal],`

### `claim_intimation`
- **Rows:** 41923102
- **Size:** 25075.97 MB
- **Columns:** `CI_INTIMATION_ID [varchar]`, `CI_BENF_ID [decimal]`, `CI_DEP_ID [decimal]`, `CI_PATIENT_TYPE [varchar]`, `CI_ADMISSION_NO [varchar]`, `CI_ADMISSION_DATE [datetime]`, `CI_CARD_ID [varchar]`, `CI_CARD_MAKE [int]`, `CI_WHITE_CARD [int]`, `CI_APP_TYPE_ID [int]`, `CI_DIS_TYPE_ID [int]`, `CI_SERV_PERIOD [int]`, `CI_BENEFICIARY_NAME [varchar]`, `CI_CARD_TYPE [varchar]`, `CI_CARD_VALID_DT [date]`, `CI_OFFICE_NAME [varchar]`, `CI_OFFICE_DEPARTMENT [varchar]`, `CI_PATIENT_NAME [varchar]`, `CI_AGE [varchar]`, `CI_SEX [varchar]`, `CI_RELATION_ID [varchar]`, `CI_PHONE_NO [varchar]`, `CI_MOBILE [varchar]`, `CI_EMAIL [varchar]`, `CI_ADDRESS1 [varchar]`, `CI_ADDRESS2 [varchar]`, `CI_ADDRESS3 [varchar]`, `CI_CITY [varchar]`, `CI_STATE_ID [varchar]`, `CI_PIN [varchar]`, `CI_CGHS_REGION_ID [varchar]`, `CI_HOSPITAL_ID [varchar]`, `CI_ROOM_TYPE_ID [varchar]`, `CI_REF_TYPE_ID [varchar]`, `CI_ADM_AILMENT [text]`, `CI_PRE_AILMENT_DUR [varchar]`, `CI_IS_RTA [varchar]`, `CI_RTA_REASON [varchar]`, `CI_RTA_DATE [date]`, `CI_RTA_DOC_ID [varchar]`, `CI_INT_STATUS [varchar]`, `CI_INT_STAGE [varchar]`, `CI_CR_USER_ID [varc`

### `claim_submission`
- **Rows:** 37562952
- **Size:** 21262.97 MB
- **Columns:** `CS_INTIMATION_ID [varchar]`, `CS_ADMISSION_DATE [datetime]`, `CS_ADM_AILMENT [text]`, `CS_PRE_AILMENT_DUR [varchar]`, `CS_AILMENT_HIST [varchar]`, `CS_FIRST_OCC_DATE [date]`, `CS_DOD [datetime]`, `CS_DISCHARGE_TYPE [varchar]`, `CS_TREAT_DOCT [varchar]`, `CS_SUB_DATE [datetime]`, `CS_SUB_USER_ID [varchar]`, `CS_SUB_OFFICE_ID [varchar]`, `CS_SUB_ENTITY_ID [varchar]`, `CS_ACCEPT_DATE [datetime]`, `CS_GR_CLAIM_AMT [decimal]`, `CS_PAT_AMT [decimal]`, `CS_PAT_DISC_AMT [decimal]`, `CS_NET_CLAIM_AMT [decimal]`, `CS_UTI_PAR_AMT [decimal]`, `CS_UTI_SUP_AMT [decimal]`, `CS_UTI_APP_AMT [decimal]`, `CS_ROOM_TYPE [varchar]`, `CS_ROOM_NO [varchar]`, `CS_PAR_IRREV_CHARGES [decimal]`, `CS_PAR_EXCESS_AMT [decimal]`, `CS_SUP_IRREV_CHARGES [decimal]`, `CS_SUP_EXCESS_AMT [decimal]`, `CS_APP_IRREV_CHARGES [decimal]`, `CS_APP_EXCESS_AMT [decimal]`, `CS_PAT_DIS_STATUS [varchar]`, `CS_REC_DATE [datetime]`, `CS_REC_USER_ID [varchar]`, `CS_REC_OFFICE_ID [varchar]`, `CS_REC_ENTITY_ID [varchar]`, `CS_PAR_DATE [datetime]`, `CS_PAR_USER_ID [varchar]`, `CS_PAR_OFFICE_ID [varchar]`, `CS_PAR_ENTITY_ID [varchar]`, `CS`

### `user_allot_archiwe`
- **Rows:** 41505067
- **Size:** 9358.00 MB
- **Columns:** `UAA_TRACKING_ID [bigint]`, `UAA_USER [varchar]`, `UAA_DATE [datetime]`, `UAA_USER_ID [varchar]`, `UAA_PATIENT_TYPE [varchar]`, `UAA_FROM_AMT [decimal]`, `UAA_TO_AMT [decimal]`, `UAA_CLAIM_ID [varchar]`, `UAA_CLAIM_AMT [decimal]`, `UAA_CURRENT_STAGE [varchar]`, `UAA_CURRENT_STATUS [varchar]`, `UAA_ACCEPT_DATE [datetime]`, `UAA_PROCESS_STAGE [varchar]`, `UAA_PROCESS_STATUS [varchar]`, `UAA_START_TIME [datetime]`, `UAA_END_TIME [datetime]`, `UAA_ACTION_MODE [varchar]`, `UAA_ACTION_DATE [date]`, `UAA_NEW_ALLOTEE [varchar]`, `UAA_ACTION_BY [varchar]`, `UAA_CATG_ID [int]`, `UAA_RANGE_ID [int]`

### `diag_details`
- **Rows:** 43667486
- **Size:** 7940.00 MB
- **Columns:** `DD_INTIMATION_ID [varchar]`, `DD_DIAG_SEQ_NO [int]`, `DD_DIAG_TYPE_ID [varchar]`, `DD_DIAG_DETAILS [text]`, `DD_DIAG_ICD_CODE [varchar]`, `DD_DIAG_PAR_DETAILS [text]`, `DD_DIAG_PAR_ICD_CODE [varchar]`, `DD_DIAG_PAR_ACTIVE [varchar]`, `DD_DIAG_SUP_DETAILS [text]`, `DD_DIAG_SUP_ICD_CODE [varchar]`, `DD_DIAG_SUP_ACTIVE [varchar]`, `DD_DIAG_APP_DETAILS [text]`, `DD_DIAG_APP_ICD_CODE [varchar]`, `DD_DIAG_APP_ACTIVE [varchar]`, `DD_ALREADY_SUBMITTED [varchar]`, `DD_ENHANCE_ID [int]`

### `ecs_cr_recs`
- **Rows:** 35176400
- **Size:** 7452.00 MB
- **Columns:** `ECR_TRAN_CODE [varchar]`, `ECR_DES_BNK_BRN_SORT_CD [varchar]`, `ECR_DES_BNK_ACTYPE [varchar]`, `ECR_FOLIO_NO [varchar]`, `ECR_DES_BNK_ACNO [varchar]`, `ECR_DES_BENE_NAME [varchar]`, `ECR_SP_BNK_BRN_SORT_CD [varchar]`, `ECR_USER_NO [varchar]`, `ECR_USER_NAME [varchar]`, `ECR_CR_REF [varchar]`, `ECR_CR_AMOUNT [varchar]`, `ECR_RESV_1 [varchar]`, `ECR_RESV_2 [varchar]`, `ECR_RESV_3 [varchar]`, `ECR_FILLER [varchar]`, `ECR_SETTLEMENT_ID [varchar]`, `ECR_TRAN_NO [int]`

### `referal_details`
- **Rows:** 35814037
- **Size:** 7336.00 MB
- **Columns:** `REF_INTIMATION_ID [varchar]`, `REF_NUMBER [varchar]`, `REF_CGHS_REGION_ID [varchar]`, `REF_CGHS_DISP_ID [varchar]`, `REF_ISS_DATE [date]`, `REF_ADV_BY [varchar]`, `REF_APP_BY [varchar]`, `REF_HOSPITAL_ID [varchar]`, `REF_ROOM_TYPE_ID [varchar]`, `REF_VAL_DATE [date]`, `REF_SESSIONS [int]`, `REF_PROCEDURES [text]`, `REF_ENTRY_BY [varchar]`, `REF_BAL_SESSION [int]`, `REF_ADM_PROCEDURES [text]`, `REF_INV_PROCEDURES [text]`, `REF_CON_PROCEDURES [text]`, `REF_TRAVEL_REIMBURSE [varchar]`, `REF_ATTENDANT_REIMBURSE [varchar]`, `REF_PATIENT_TYPE [varchar]`, `REF_CITY_ID [varchar]`

### `pre_exist_ailment`
- **Rows:** 118224289
- **Size:** 6875.00 MB
- **Columns:** `PEA_INTIMATION_ID [varchar]`, `PEA_AILMENT_ID [varchar]`, `PEA_IS_AILMENT [varchar]`, `PEA_AILMENT_DETAILS [varchar]`, `PEA_ENHANCE_ID [int]`

### `check_list_details`
- **Rows:** 192179307
- **Size:** 6281.00 MB
- **Columns:** `CLD_INTIMATION_ID [varchar]`, `CLD_LIST_ID [varchar]`, `CLD_IS_PRESENT [varchar]`

### `transaction_history`
- **Rows:** 60776027
- **Size:** 6100.00 MB
- **Columns:** `TH_TRAN_NO [int]`, `TH_TIME [datetime]`, `TH_IS_MAIN_MENU [varchar]`, `TH_TRAN_DETAILS [text]`, `TH_ERROR_ID [decimal]`

### `cda_payment_response`
- **Rows:** 21318349
- **Size:** 5659.00 MB
- **Columns:** `CPR_CLAIM_ID [varchar]`, `CPR_SETTLEMENT_ID [varchar]`, `CPR_PAYEE_NAME [varchar]`, `CPR_PAY_REFERENCE [varchar]`, `CPR_AMT_PAID [decimal]`, `CPR_SERVICE_FEES [decimal]`, `CPR_TDS_GST_BPA [decimal]`, `CPR_TDS_HOSP_FEES [decimal]`, `CPR_TDS_BPA_FEES [decimal]`, `CPR_IFSC_CODE [varchar]`, `CPR_ACC_NUM [varchar]`, `CPR_UTR_NO [varchar]`, `CPR_UTR_DATE [datetime]`, `CPR_13_NUM [varchar]`, `CPR_CDA_13_DATE [datetime]`, `CPR_SCROLL_NUM [varchar]`, `CPR_SCROLL_DATE [datetime]`, `CPR_REJ_SCROLL_NUM [varchar]`, `CPR_REJ_SCROLL_DATE [datetime]`, `CPR_CMP_FILE_DATE [date]`, `CPR_CMP_REJ_REASON [varchar]`, `CPR_BPA_FILE_DATE [date]`, `CPR_BPA_PAY_REFNO [varchar]`, `CPR_BPA_UTR_NO [varchar]`, `CPR_BPA_UTR_DATE [date]`, `CPR_BPA_SCROLL_NO [varchar]`, `CPR_BPA_SCROLL_DATE [date]`, `CPR_BPA_CDA13_NO [varchar]`, `CPR_BPA_CDA13_DATE [date]`, `CPR_BPA_REJ_SCROLL_NO [varchar]`, `CPR_BPA_REJ_SCROLL_DATE [date]`, `CPR_BPA_REJ_REASON [text]`

### `clinical_findings_int`
- **Rows:** 88825233
- **Size:** 5248.98 MB
- **Columns:** `CF_INTIMATION_ID [varchar]`, `CF_CLTEST_ID [varchar]`, `CT_IS_CLTEST [varchar]`, `CF_CLTEST_DETAILS [text]`, `CF_ENHANCE_ID [int]`

### `settlement_valdate`
- **Rows:** 37544740
- **Size:** 4501.98 MB
- **Columns:** `SV_INTIMATION_ID [varchar]`, `SV_FIRST_VAL_DATE [datetime]`, `SV_PROV_BPA_FEE [decimal]`, `SV_PROV_BPA_SER_TAX [decimal]`, `SV_USER_ID [varchar]`, `SV_PAID_DT [datetime]`, `SV_VOUCHER_NO [varchar]`

### `audit_status`
- **Rows:** 15658725
- **Size:** 4454.30 MB
- **Columns:** `AS_CLAIM_ID [varchar]`, `AS_AUD_STAGE [varchar]`, `AS_AUD_STATUS [varchar]`, `AS_QUERIES_NOS [int]`, `AS_AUD_NOS [int]`, `AS_AAO_NOS [int]`, `AS_SAO_IN_DATE [datetime]`, `AS_SAO_NOS [int]`, `AS_RC_IN_DATE [datetime]`, `AS_RC_NOS [int]`, `AS_BPA_IN_DATE [datetime]`, `AS_BPA_NOS [int]`, `AS_HOS_IN_DATE [datetime]`, `AS_HOS_NOS [int]`, `AS_CORG_IN_DATE [datetime]`, `AS_CORG_NOS [int]`, `AS_CFA_IN_DATE [datetime]`, `AS_CFA_NOS [int]`, `AS_CDA_AMT [decimal]`, `AS_RECOVER_AMT [decimal]`, `AS_RECOVERED_AMT [decimal]`, `AS_CLOSED [varchar]`, `AS_ACCEPT_NOS [int]`

### `prop_treatment`
- **Rows:** 56861727
- **Size:** 4154.00 MB
- **Columns:** `PT_INTIMATION_ID [varchar]`, `PT_TRTYPE_ID [varchar]`, `PR_IS_TREATMENT [varchar]`, `PR_TR_DETAILS [text]`, `PR_ENHANCE_ID [int]`, `PR_PRE_AUTH_ID [int]`

### `treatment_details`
- **Rows:** 57544304
- **Size:** 3256.00 MB
- **Columns:** `TD_INTIMATION_ID [varchar]`, `TD_TRTYPE_ID [varchar]`, `TD_IS_TREATMENT [varchar]`, `TD_TR_DETAILS [text]`

### `clinical_findings_sub`
- **Rows:** 55564975
- **Size:** 2936.00 MB
- **Columns:** `CF_INTIMATION_ID [varchar]`, `CF_CLTEST_ID [varchar]`, `CT_IS_CLTEST [varchar]`, `CF_CLTEST_DETAILS [text]`

### `opd_ph_answers`
- **Rows:** 53806794
- **Size:** 2910.00 MB
- **Columns:** `opd_ans_id [int]`, `opd_ans_anyhistory [varchar]`, `opd_ans_details [varchar]`, `opd_claim_id [varchar]`

### `cda_remarks`
- **Rows:** 25779102
- **Size:** 2829.00 MB
- **Columns:** `CDR_INTIMATION_ID [varchar]`, `CDA_USER_ID [varchar]`, `CDA_DATE [datetime]`, `CDA_REMARKS [mediumtext]`, `CDA_STAGE [varchar]`, `CDA_STATUS [varchar]`, `CDA_MODE [varchar]`

### `hosp_exp`
- **Rows:** 13054067
- **Size:** 2463.91 MB
- **Columns:** `HE_INTIMATION_ID [varchar]`, `HE_EXP_ID [varchar]`, `HE_CLAIM_AMOUNT [decimal]`, `HE_PAR_AMOUNT [decimal]`, `HE_SUP_AMOUNT [decimal]`, `HE_APP_AMOUNT [decimal]`, `HE_HOS_REMARK [text]`, `HE_PAR_REMARK [text]`, `HE_SUP_REMARK [text]`, `HE_APP_REMARK [text]`, `HE_PAR_EXCESS_AMT [decimal]`, `HE_PAR_IRREV_AMT [decimal]`, `HE_SUP_EXCESS_AMT [decimal]`, `HE_SUP_IRREV_AMT [decimal]`, `HE_APP_EXCESS_AMT [decimal]`, `HE_APP_IRREV_AMT [decimal]`

### `sms_transaction`
- **Rows:** 5549368
- **Size:** 2417.00 MB
- **Columns:** `ST_INTIMATION_ID [varchar]`, `ST_DATE [datetime]`, `ST_ACK_ID [varchar]`, `ST_TRAN_ID [varchar]`, `ST_INT_STAGE [varchar]`, `ST_INT_STATUS [varchar]`, `ST_MOBILE [varchar]`, `ST_MESSAGE [text]`, `ST_MSG_ID [varchar]`, `ST_DLR_TIME [datetime]`, `ST_SMS_STATUS [varchar]`, `ST_ERR_CODE [varchar]`, `ST_SMS_DETAIL [text]`

### `bpa_claim_process`
- **Rows:** 7574266
- **Size:** 1497.41 MB
- **Columns:** `BCP_ID [int]`, `BCP_ALLOT_ID [int]`, `BCP_SETUP_ID [int]`, `BCP_USER_ID [varchar]`, `BCP_CLAIM_ID [varchar]`, `BCP_ALLOT_TYPE [int]`, `BCP_STAGE [varchar]`, `BCP_STATUS [varchar]`, `BCP_FWD [int]`, `BCP_DATE [date]`, `BCP_TIME [time]`, `BCP_FIN_DATE [date]`, `BCP_FIN_TIME [time]`, `BCP_IP_ADDR [varchar]`

### `audit_trail`
- **Rows:** 13234655
- **Size:** 1330.00 MB
- **Columns:** `AT_ENTITY_ID [varchar]`, `AT_OFFICE_ID [varchar]`, `AT_USER_ID [varchar]`, `AT_TRAN_NO [int]`, `AT_IP_ADDRESS [varchar]`, `AT_MAC_ADDRESS [varchar]`, `AT_SESSION_ID [varchar]`, `AT_LOGIN_TIME [datetime]`, `AT_LOGOUT_TIME [datetime]`, `AT_SESSION_EXPIRED [varchar]`, `AT_LOGIN_TYPE [int]`

### `web_referral`
- **Rows:** 13204115
- **Size:** 1081.00 MB
- **Columns:** `WR_REFERENCE_NO [varchar]`, `WR_CLAIM_ID [varchar]`, `WR_HOSPITAL_ID [varchar]`, `WR_POLYCLINIC_ID [varchar]`, `WR_DATE [datetime]`, `WR_USER_ID [varchar]`, `WR_IP_ADDRESS [varchar]`

### `referral_sessions`
- **Rows:** 12491548
- **Size:** 1066.00 MB
- **Columns:** `RS_CLAIM_ID [varchar]`, `RS_REF_CLAIM_ID [varchar]`, `RS_DATE [datetime]`

### `claim_folder`
- **Rows:** 12900956
- **Size:** 1031.00 MB
- **Columns:** `CF_CLAIM_ID [varchar]`, `CF_DATE [datetime]`, `CF_OFFICE_ID [varchar]`, `CF_FOLDER [varchar]`, `CF_FLDR_CRTN_DT [date]`, `CF_FLDR_LCTN [int]`

### `his_hosp_exp_det`
- **Rows:** 6792335
- **Size:** 1022.98 MB
- **Columns:** `HED_INTIMATION_ID [varchar]`, `HED_EXP_ID [varchar]`, `HED_CAT_ID [varchar]`, `HED_CAT_SUB_ID [varchar]`, `HED_REGION_ID [varchar]`, `HED_ACT_RATE [decimal]`, `HED_HOS_RATE [decimal]`, `HED_CLAIM_UNITS [decimal]`, `HED_CLAIM_AMOUNT [decimal]`, `HED_PAR_AMOUNT [decimal]`, `HED_SUP_AMOUNT [decimal]`, `HED_APP_AMOUNT [decimal]`, `HED_HISTORY_ID [int]`

### `his_patient_register`
- **Rows:** 3203940
- **Size:** 859.00 MB
- **Columns:** `PTR_HISTORY_ID [int]`, `PTR_CARD_ID [varchar]`, `PTR_TEMP_SLIP_NO [int]`, `PTR_BEN_ID [bigint]`, `PTR_BENEFICIARY_NAME [varchar]`, `PTR_PATIENT_NAME [varchar]`, `PTR_SERVICE_TYPE [varchar]`, `PTR_SERVICE_RANK [int]`, `PTR_SERVICE_NO [varchar]`, `PTR_UID_NUMBER [varchar]`, `PTR_UID_STATUS [int]`, `PTR_DOB [date]`, `PTR_COMM_DATE [date]`, `PTR_RETIRE_DATE [date]`, `PTR_APP_TYPE_ID [int]`, `PTR_DIS_TYPE_ID [int]`, `PTR_SEX [varchar]`, `PTR_RELATION_ID [varchar]`, `PTR_PHONE_NO [varchar]`, `PTR_MOBILE [varchar]`, `PTR_EMAIL [varchar]`, `PTR_ADDRESS1 [varchar]`, `PTR_ADDRESS2 [varchar]`, `PTR_ADDRESS3 [varchar]`, `PTR_CITY [varchar]`, `PTR_STATE_ID [varchar]`, `PTR_PIN [varchar]`, `PTR_CARD_ROOM_TYPE [varchar]`, `PTR_CR_USER [varchar]`, `PTR_CR_DATE [datetime]`, `PTR_IP_ADDRESS [varchar]`, `PTR_UPDATE_BY [varchar]`, `PTR_UPDATE_ON [datetime]`, `PTR_DOE [date]`

### `echs_64bit_card`
- **Rows:** 2967292
- **Size:** 826.61 MB
- **Columns:** `EBC_CARD_NUMBER [int]`, `EBC_TEMP_SLIP_NO [int]`, `EBC_RC_CARD_ID [varchar]`, `EBC_BEN_ID [int]`, `EBC_BENEFICIARY_NAME [varchar]`, `EBC_PATIENT_NAME [varchar]`, `EBC_SERVICE_TYPE [varchar]`, `EBC_SERVICE_RANK [int]`, `EBC_SERVICE_NO [varchar]`, `EBC_COMM_DATE [date]`, `EBC_RETIRE_DATE [date]`, `EBC_APP_TYPE_ID [int]`, `EBC_DIS_TYPE_ID [int]`, `EBC_BLOOD_GROUP [varchar]`, `EBC_UID_NUMBER [varchar]`, `EBC_UID_STATUS [int]`, `EBC_DOB [date]`, `EBC_DOE [date]`, `EBC_GENDER [varchar]`, `EBC_RELATION_ID [varchar]`, `EBC_PHONE_NO [varchar]`, `EBC_MOBILE [varchar]`, `EBC_EMAIL [varchar]`, `EBC_ADDRESS1 [varchar]`, `EBC_ADDRESS2 [varchar]`, `EBC_ADDRESS3 [varchar]`, `EBC_CITY [varchar]`, `EBC_STATE_ID [varchar]`, `EBC_PIN [varchar]`, `EBC_CARD_ROOM_TYPE [varchar]`, `EBC_CR_USER [varchar]`, `EBC_CR_DATE [datetime]`, `EBC_IP_ADDRESS [varchar]`, `EBC_MAIN_CLINIC_ID [varchar]`, `EBC_FROM_API [int]`

### `his_document_submitted`
- **Rows:** 4287039
- **Size:** 708.91 MB
- **Columns:** `DS_INTIMATION_ID [varchar]`, `DS_DOCTYPE_ID [varchar]`, `DS_DOC_ID [varchar]`, `DS_REMARK [text]`, `DS_FILENAME [varchar]`, `DS_FILE_SR_NO [int]`, `DS_IS_RECEIVED [varchar]`, `DS_REC_REMARK [text]`, `DS_REC_REMARK_ID [varchar]`, `DS_MUL_DOC [varchar]`, `DS_DOC_SUBMITTED [varchar]`, `DS_DOC_COUNT [int]`, `DS_DOC_SUBMIT_BY [varchar]`, `DS_ENHANCE_ID [int]`, `DS_SUBMIT_TIME [datetime]`, `DS_FILE_SIZE [decimal]`, `DS_SIGNED [int]`, `DS_HISTORY_ID [int]`

### `claim_changes`
- **Rows:** 4121675
- **Size:** 645.88 MB
- **Columns:** `cc_intimation_id [varchar]`, `cc_change_id [int]`, `cc_change_type [varchar]`, `cc_change_desc [varchar]`, `cc_prev_value [varchar]`, `cc_curr_value [varchar]`, `cc_user_id [varchar]`, `cc_field_map [varchar]`, `CC_REQUEST_ID [int]`

### `settlement_doc_reco`
- **Rows:** 7539304
- **Size:** 628.80 MB
- **Columns:** `SDR_INTIMATION_ID [varchar]`, `SDR_FINAL_SETTLE_DT [date]`, `SDR_SET_INT_ID [varchar]`, `SDR_SENT_DATE [date]`, `SDR_LIST_NAME [varchar]`, `SDR_FLAG [varchar]`

### `user_over_time`
- **Rows:** 4015006
- **Size:** 596.95 MB
- **Columns:** `UOT_ID [int]`, `UOT_USER [varchar]`, `UOT_DATE [datetime]`, `UOT_RANGE_ID [int]`, `UOT_CLAIM_ID [varchar]`, `UOT_CLAIM_AMT [decimal]`, `UOT_STAGE [varchar]`, `UOT_STATUS [varchar]`, `UOT_START_TIME [datetime]`, `UOT_END_TIME [datetime]`

### `esm_bank_details`
- **Rows:** 4346750
- **Size:** 540.00 MB
- **Columns:** `EBD_CLAIM_ID [varchar]`, `EBD_BANK_NAME [varchar]`, `EBD_BRANCH_NAME [varchar]`, `EBD_IFSC_CODE [varchar]`, `EBD_MICR_CODE [varchar]`, `EBD_ACC_NAME [varchar]`, `EBD_ACC_TYPE [varchar]`, `EBD_ACC_NUMBER [varchar]`, `EBD_UPDATE_DATE [datetime]`, `EBD_IP_ADDRESS [varchar]`, `EBD_USER_ID [varchar]`

### `dependant_master`
- **Rows:** 2768232
- **Size:** 504.86 MB
- **Columns:** `DEP_BENF_ID [decimal]`, `DEP_ID [decimal]`, `DEP_CARD_NO [varchar]`, `DEP_NAME [varchar]`, `DEP_BLOOD_GRP [varchar]`, `DEP_STATUS [varchar]`, `DEP_RELN [varchar]`, `DEP_EMP [varchar]`, `DEP_DOB [date]`, `DEP_HANDICAP [varchar]`, `DEP_POLY [varchar]`, `DEP_CITY [varchar]`, `DEP_STATE [varchar]`, `DEP_PIN [varchar]`, `DEP_WAR_WIDOW [varchar]`, `DEP_GENDER [varchar]`, `DEP_RELATION_ID [varchar]`

### `benf_master_live`
- **Rows:** 1397938
- **Size:** 378.17 MB
- **Columns:** `BM_BEN_ID [decimal]`, `BM_PENSION_TYPE [varchar]`, `BM_PENSIONER_NAME [varchar]`, `BM_GENDER [varchar]`, `BM_FORCE_TYPE [varchar]`, `BM_SERVICE_NO [varchar]`, `BM_CARD_NO [varchar]`, `BM_RANK_CODE [int]`, `BM_ROOM_ID [varchar]`, `BM_FAMILY_RELATION_ID [int]`, `BM_DOB [date]`, `BM_DOR [date]`, `BM_DOE [date]`, `BM_CITY [varchar]`, `BM_STATE_ID [int]`, `BM_PIN [varchar]`, `BM_REGION_ID [int]`, `BM_POLYCLINIC [varchar]`, `BM_POLYCLINIC_ID [varchar]`, `BM_DISTRICT [varchar]`, `BM_DOM [varchar]`, `BM_DISABILITY [varchar]`, `BM_WAR_WIDOW [varchar]`, `BM_DRUG_ALLERGY [varchar]`, `BM_EMPLOYED [varchar]`, `BM_MARITAL_STATUS [varchar]`, `BM_POLYCLINIC_CODE [varchar]`, `BM_CARD_UPGRADE [varchar]`, `BM_NEW_CARD_NO [varchar]`

### `benf_mast_32kb`
- **Rows:** 1139443
- **Size:** 375.05 MB
- **Columns:** `PensionerName [varchar]`, `PenServiceNumber [varchar]`, `PenForceType [varchar]`, `BPA_SERVICE_CODE [varchar]`, `PenRankName [varchar]`, `BPA_RANK_ID [int]`, `PenDOB [varchar]`, `PenDOR [varchar]`, `PenCityName [varchar]`, `FamilyPensionerRelation [varchar]`, `FPenGender [varchar]`, `PenPolyclinic [varchar]`, `PenGender [varchar]`, `PenDOC [varchar]`, `DepName [varchar]`, `DepRelation [varchar]`, `BPA_RELATION_ID [varchar]`, `DepDOB [varchar]`, `CardNo [varchar]`, `Whether32KB [varchar]`, `PenDORAF [varchar]`

### `hosp_stats`
- **Rows:** 8095080
- **Size:** 327.86 MB
- **Columns:** `HS_INTIMATION_ID [varchar]`, `HS_PROC_DATE [datetime]`

### `audit_query`
- **Rows:** 1511343
- **Size:** 322.63 MB
- **Columns:** `AQ_CLAIM_ID [varchar]`, `AQ_QUERY_ID [int]`, `AQ_REQUERY_ID [int]`, `AQ_LEVEL [varchar]`, `AQ_RECOVERY_TYPE [int]`, `AQ_QUERY_NO [int]`, `AQ_QUERY [text]`, `AQ_CDA_AMT [decimal]`, `AQ_RECOVER_AMT [decimal]`, `AQ_CLOSE [varchar]`, `AQ_QUERY_USER [varchar]`, `AQ_QUERY_DATE [datetime]`, `AQ_FORWARD_TO [varchar]`, `AQ_FORWARD_DATE [datetime]`, `AQ_REPLY_ID [int]`

### `dep_master_live`
- **Rows:** 3200177
- **Size:** 297.41 MB
- **Columns:** `DEP_BEN_ID [decimal]`, `DEP_ID [decimal]`, `DEP_NAME [varchar]`, `DEP_GENDER [varchar]`, `DEP_RELN [varchar]`, `DEP_RELATION_ID [int]`, `DEP_DOB [date]`, `DEP_DOE [varchar]`, `DEP_BLOOD_GRP [varchar]`, `DEP_CARD_NO [varchar]`, `DEP_NEW_CARD_NO [varchar]`

### `member_feedback`
- **Rows:** 5025667
- **Size:** 293.89 MB
- **Columns:** `MF_CLAIM_ID [varchar]`, `MF_REF_NUMBER [varchar]`, `MF_GEN_DATE [datetime]`, `MF_REPLY_DATE [datetime]`, `MF_IP_ADDRESS [varchar]`, `MF_MIN_RATE [int]`, `MF_MAX_RATE [int]`

### `daily_office_pendency`
- **Rows:** 3662336
- **Size:** 271.00 MB
- **Columns:** `DOP_DATE_ID [int]`, `DOP_REGION_ID [varchar]`, `DOP_OFFICE_ID [varchar]`, `DOP_PATIENT_TYPE [varchar]`, `DOP_ADM_TYPE [varchar]`, `DOP_STAGE [varchar]`, `DOP_STATUS [varchar]`, `DOP_GROUP_ID [varchar]`, `DOP_CLAIM_COUNT [int]`, `DOP_TOTAL_NET [bigint]`, `DOP_TOTAL_SUP [bigint]`, `DOP_TOTAL_APP [bigint]`

### `settlement_stat`
- **Rows:** 2740880
- **Size:** 232.00 MB
- **Columns:** `SS_YEAR [int]`, `SS_MONTH [int]`, `SS_FY_YEAR [int]`, `SS_PAT_TYPE_ID [varchar]`, `SS_ENTITY_ID [varchar]`, `SS_REF_TYPE_ID [varchar]`, `SS_REGION_ID [varchar]`, `SS_OFFICE_ID [varchar]`, `SS_GENDER [varchar]`, `SS_RELATION_ID [varchar]`, `SS_ROOM_CATG [varchar]`, `SS_CLAIM_CNT [int]`, `SS_CLAIM_AMT [bigint]`, `SS_APPR_AMT [bigint]`, `SS_DED_AMT [bigint]`

### `pend_claims`
- **Rows:** 1537814
- **Size:** 201.33 MB
- **Columns:** `REGION_ID [varchar]`, `OFFICE_ID [varchar]`, `PATIENT_TYPE [varchar]`, `ADM_TYPE [varchar]`, `REIM_TYPE [varchar]`, `CLAIM_STAGE [varchar]`, `CLAIM_STATUS [varchar]`, `MOD_DATE [datetime]`, `ACC_DATE [datetime]`, `ENTITY_ID [varchar]`, `NET_AMT [int]`, `SUP_AMT [int]`, `APP_AMT [int]`, `CURR_RATIO [decimal]`, `DOC_RECD [int]`, `DOC_VERIFY [int]`

### `ifa_events`
- **Rows:** 1017320
- **Size:** 198.33 MB
- **Columns:** `IE_EVENT_ID [int]`, `IE_CLAIM_ID [varchar]`, `IE_PROC_ID [int]`, `IE_ESCLATE [varchar]`, `IE_DATE [datetime]`, `IE_GROUP_ID [varchar]`, `IE_USER_ID [varchar]`, `IE_REMARKS [text]`, `IE_AMOUNT [int]`, `IE_IP_ADDRESS [varchar]`, `IE_REVERT [int]`

### `his_treatment_details`
- **Rows:** 1994592
- **Size:** 194.33 MB
- **Columns:** `TD_INTIMATION_ID [varchar]`, `TD_TRTYPE_ID [varchar]`, `TD_IS_TREATMENT [varchar]`, `TD_TR_DETAILS [text]`, `TD_HISTORY_ID [int]`

### `his_claim_submission`
- **Rows:** 630315
- **Size:** 189.88 MB
- **Columns:** `CS_INTIMATION_ID [varchar]`, `CS_ADMISSION_DATE [datetime]`, `CS_ADM_AILMENT [text]`, `CS_PRE_AILMENT_DUR [varchar]`, `CS_AILMENT_HIST [varchar]`, `CS_FIRST_OCC_DATE [date]`, `CS_DOD [datetime]`, `CS_TREAT_DOCT [varchar]`, `CS_SUB_DATE [datetime]`, `CS_SUB_USER_ID [varchar]`, `CS_SUB_OFFICE_ID [varchar]`, `CS_SUB_ENTITY_ID [varchar]`, `CS_ACCEPT_DATE [datetime]`, `CS_GR_CLAIM_AMT [decimal]`, `CS_PAT_AMT [decimal]`, `CS_PAT_DISC_AMT [decimal]`, `CS_NET_CLAIM_AMT [decimal]`, `CS_UTI_PAR_AMT [decimal]`, `CS_UTI_SUP_AMT [decimal]`, `CS_UTI_APP_AMT [decimal]`, `CS_ROOM_TYPE [varchar]`, `CS_ROOM_NO [varchar]`, `CS_PAR_IRREV_CHARGES [decimal]`, `CS_PAR_EXCESS_AMT [decimal]`, `CS_SUP_IRREV_CHARGES [decimal]`, `CS_SUP_EXCESS_AMT [decimal]`, `CS_APP_IRREV_CHARGES [decimal]`, `CS_APP_EXCESS_AMT [decimal]`, `CS_PAT_DIS_STATUS [varchar]`, `CS_REC_DATE [datetime]`, `CS_REC_USER_ID [varchar]`, `CS_REC_OFFICE_ID [varchar]`, `CS_REC_ENTITY_ID [varchar]`, `CS_PAR_DATE [datetime]`, `CS_PAR_USER_ID [varchar]`, `CS_PAR_OFFICE_ID [varchar]`, `CS_PAR_ENTITY_ID [varchar]`, `CS_SUP_DATE [datetime]`, `CS_SUP_`

### `his_clinical_findings_sub`
- **Rows:** 1968287
- **Size:** 187.33 MB
- **Columns:** `CF_INTIMATION_ID [varchar]`, `CF_CLTEST_ID [varchar]`, `CT_IS_CLTEST [varchar]`, `CF_CLTEST_DETAILS [varchar]`, `CF_HISTORY_ID [int]`

### `daily_region_pendency`
- **Rows:** 1080667
- **Size:** 175.47 MB
- **Columns:** `DP_DATE_ID [int]`, `DP_REGION_ID [varchar]`, `DP_ENTITY_ID [varchar]`, `DP_PATIENT_TYPE [varchar]`, `DP_ADM_TYPE [varchar]`, `DP_STAGE [varchar]`, `DP_STATUS [varchar]`, `DP_GROUP_ID [varchar]`, `DP_CLAIM_COUNT [int]`, `DP_TOTAL_NET [bigint]`, `DP_TOTAL_SUP [bigint]`, `DP_TOTAL_APP [bigint]`

### `error_log`
- **Rows:** 857224
- **Size:** 167.69 MB
- **Columns:** `EL_ERROR_ID [decimal]`, `EL_DATE [datetime]`, `EL_USER_ID [varchar]`, `EL_GROUP_NAME [varchar]`, `EL_STATUS [varchar]`, `EL_CLAIM_ID [varchar]`, `EL_ERROR_TYPE [varchar]`, `EL_ERROR_MESSAGE [text]`, `EL_IP_ADDRESS [varchar]`

### `audit_reply`
- **Rows:** 1102256
- **Size:** 158.20 MB
- **Columns:** `AR_REPLY_ID [int]`, `AR_QUERY_ID [int]`, `AR_REQUERY_ID [int]`, `AR_REPLY [text]`, `AR_RECOVER_AMT [decimal]`, `AR_FORWARD_TO [varchar]`, `AR_USER_ID [varchar]`, `AR_REPLY_DATE [datetime]`, `AR_REPLY_BY [varchar]`

### `error_class`
- **Rows:** 1689169
- **Size:** 150.22 MB
- **Columns:** `EC_ERROR_ID [decimal]`, `EC_FILENAME [varchar]`, `EC_METHODNAME [varchar]`, `EC_LINENUMBER [int]`

### `ifa_process`
- **Rows:** 916342
- **Size:** 149.36 MB
- **Columns:** `IP_CLAIM_ID [varchar]`, `IP_ALLOT_ID [int]`, `IP_PROC_ID [int]`, `IP_DATE [datetime]`, `IP_GROUP_ID [varchar]`, `IP_NMI_BY [varchar]`, `IP_EVENT_ID [int]`, `IP_CFA_CHECK [int]`, `IP_AMOUNT [int]`

### `pend_group_details`
- **Rows:** 1174009
- **Size:** 139.27 MB
- **Columns:** `REGION_ID [varchar]`, `OFFICE_ID [varchar]`, `PATIENT_TYPE [varchar]`, `ADM_TYPE [varchar]`, `REIM_TYPE [varchar]`, `CLAIM_STAGE [varchar]`, `CLAIM_STATUS [varchar]`, `MOD_DATE [datetime]`, `ACC_DATE [datetime]`, `ENTITY_ID [varchar]`, `NET_AMT [int]`, `SUP_AMT [int]`, `APP_AMT [int]`, `GROUP_ID [varchar]`

### `his_diag_details`
- **Rows:** 675416
- **Size:** 128.20 MB
- **Columns:** `DD_INTIMATION_ID [varchar]`, `DD_DIAG_SEQ_NO [int]`, `DD_DIAG_TYPE_ID [varchar]`, `DD_DIAG_DETAILS [text]`, `DD_DIAG_ICD_CODE [varchar]`, `DD_DIAG_PAR_DETAILS [text]`, `DD_DIAG_PAR_ICD_CODE [varchar]`, `DD_DIAG_PAR_ACTIVE [varchar]`, `DD_DIAG_SUP_DETAILS [text]`, `DD_DIAG_SUP_ICD_CODE [varchar]`, `DD_DIAG_SUP_ACTIVE [varchar]`, `DD_DIAG_APP_DETAILS [text]`, `DD_DIAG_APP_ICD_CODE [varchar]`, `DD_DIAG_APP_ACTIVE [varchar]`, `DD_ALREADY_SUBMITTED [varchar]`, `DD_ENHANCE_ID [int]`, `DD_HISTORY_ID [int]`

### `user_password_history`
- **Rows:** 944151
- **Size:** 115.20 MB
- **Columns:** `uph_user_id [varchar]`, `uph_password [varchar]`, `uph_change_on [datetime]`, `uph_updated_by [varchar]`, `uph_update_IP [varchar]`

## Tier 2: Medium Tables (1 MB - 100 MB) (Total: 61)
### `cda_payment_reject`
- **Rows:** 154105
- **Size:** 89.72 MB
- **Columns:** `CPR_SETTLEMENT_ID [varchar]`, `CPR_CLAIM_ID [varchar]`, `CPR_OFFICE_ID [varchar]`, `CPR_ENTITY_ID [varchar]`, `CPR_REASON [text]`, `CPR_REMARKS [text]`, `CPR_ACCEPT_DATE [date]`, `CPR_CARD_ID [varchar]`, `CPR_SERVICE_NO [varchar]`, `CPR_BENF_NAME [varchar]`, `CPR_RANK [varchar]`, `CPR_PATIENT_NAME [varchar]`, `CPR_RELATION [varchar]`, `CPR_ADMIT_DATE [date]`, `CPR_DOD [date]`, `CPR_CLAIM_AMT [decimal]`, `CPR_APP_AMT [decimal]`, `CPR_DISALLOW_AMT [decimal]`, `CPR_BPA_FEES [decimal]`, `CPR_PENALITY [decimal]`, `CPR_HOS_UTI_SER [decimal]`, `CPR_DISC_AMT [decimal]`, `CPR_RECOV_AMT [decimal]`, `CPR_PAYEE_NAME [varchar]`, `CPR_IFSC [varchar]`, `CPR_ACC_NO [varchar]`, `CPR_ACTYPE [varchar]`, `CPR_PAN_NO [varchar]`, `CPR_NEW_SETTLE_ID [varchar]`, `CPR_NEW_SETTLE_DT [date]`, `CPR_REJECT_COUNT [int]`

### `member_claim_waiver`
- **Rows:** 463833
- **Size:** 86.19 MB
- **Columns:** `MCW_CLAIM_ID [varchar]`, `MCW_APPLY_ID [int]`, `MCW_APPLY_DATE [datetime]`, `MCW_ADMISSION_DATE [datetime]`, `MCW_EIR_DATE [datetime]`, `MCW_DOD [date]`, `MCW_WO_REFERRAL [int]`, `MCW_32KB [int]`, `MCW_DOC_SUBMIT_DATE [date]`, `MCW_DELAY_ID [int]`, `MCW_DELAY_REASON [text]`, `MCW_WAIVER_ID [int]`, `MCW_CUR_PROC [int]`, `MCW_PROC_COMMENT [text]`, `MCW_REQUERY_ID [int]`, `MCW_GROUP_ID [varchar]`, `MCW_REQUERY_BY [varchar]`, `MCW_REJ_COUNT [int]`, `MCW_REJ_BY [varchar]`, `MCW_PROCESS_USER [varchar]`, `MCW_PROCESS_DATE [datetime]`, `MCW_IP_ADDRESS [varchar]`, `MCW_BENF_ID [int]`, `MCW_DEP_ID [int]`, `MCW_EVENT_ID [int]`

### `unlisted_process_events`
- **Rows:** 515266
- **Size:** 77.64 MB
- **Columns:** `UPE_APPLY_ID [int]`, `UPE_INTIMATION_ID [varchar]`, `UPE_ID [int]`, `UPE_REQUERY_ID [int]`, `UPE_GROUP_ID [varchar]`, `UPE_USER_ID [varchar]`, `UPE_STATUS [int]`, `UPE_DATE [datetime]`, `UPE_REPLY [text]`, `UPE_REPLY_COST [double]`, `UPE_REPLY_UNIT [int]`, `UPE_REPLY_AMOUNT [double]`, `UPE_PROCESS_REMARKS [text]`, `UPE_IP_ADDRESS [varchar]`, `UPE_REVERT [varchar]`

### `claim_request`
- **Rows:** 417772
- **Size:** 73.59 MB
- **Columns:** `CQ_REQUEST_ID [int]`, `CQ_CLAIM_ID [varchar]`, `CQ_REQ_PROC [varchar]`, `CQ_REQ_DATE [datetime]`, `CQ_REQ_USER_ID [varchar]`, `CQ_REQ_REMARK [text]`, `CQ_REQ_IPADDRESS [varchar]`, `CQ_PROC_STATUS [varchar]`, `CQ_PROC_DATE [datetime]`, `CQ_PROC_USER_ID [varchar]`, `CQ_PROC_REMARK [text]`, `CQ_PROC_ACTIVE [varchar]`

### `bpa_claim_list`
- **Rows:** 265515
- **Size:** 73.20 MB
- **Columns:** `BCL_BPA_ID [int]`, `BCL_CLAIM_ID [varchar]`, `BCL_DATE [datetime]`, `BCL_RANGE_ID [int]`, `BCL_PAT_TYPE [varchar]`, `BCL_ENTITY_ID [int]`, `BCL_REGION_ID [varchar]`, `BCL_REIMB_TYPE [varchar]`, `BCL_HOSP_ID [varchar]`, `BCL_CATG_ID [int]`, `BCL_HOS_PRTY [int]`, `BCL_ACCEPT_DATE [datetime]`, `BCL_TAT [int]`, `BCL_PRIORITY [int]`, `BCL_LAST_BPA [varchar]`, `BCL_CLAIM_AMT [decimal]`, `BCL_SETUP_ID [int]`, `BCL_STAGE [varchar]`, `BCL_STATUS [varchar]`, `BCL_PROC_ID [int]`, `BCL_BPA_USER [varchar]`, `BCL_PROC_DATE [datetime]`, `BCL_BPA_PRTY [int]`, `BCL_FORCE_USER [varchar]`, `BCL_CLAIM_TYPE [varchar]`, `BCL_NO_DOCS [int]`

### `stay_extension_events`
- **Rows:** 479864
- **Size:** 72.63 MB
- **Columns:** `SEE_ID [int]`, `SEE_INTIMATION_ID [varchar]`, `SEE_REQUERY_ID [int]`, `SEE_GROUP_ID [varchar]`, `SEE_USER_ID [varchar]`, `SEE_PROP_DOD [date]`, `SEE_APPR_DOD [date]`, `SEE_STAGE_ID [int]`, `SEE_STATUS [int]`, `SEE_DATE [datetime]`, `SEE_REPLY [text]`, `SEE_HOSP_REMARKS [text]`, `SEE_PROCESS_REMARKS [text]`, `SEE_IP_ADDRESS [varchar]`, `SEE_REVERT [varchar]`

### `member_waiver_events`
- **Rows:** 666702
- **Size:** 68.61 MB
- **Columns:** `MWE_CLAIM_ID [varchar]`, `MWE_APPLY_ID [int]`, `MWE_GROUP_ID [varchar]`, `MWE_DATE [datetime]`, `MWE_REASON [text]`, `MWE_COMMENTS [text]`, `MWE_WAIVER_ID [int]`, `MWE_STATUS [int]`, `MWE_USER_ID [varchar]`, `MWE_EVENT_ID [int]`

### `procdlog`
- **Rows:** 977070
- **Size:** 66.59 MB
- **Columns:** `vseq [int]`, `v_file_name [varchar]`, `v_field_name [varchar]`, `v_field_value [varchar]`

### `unlisted_procedure`
- **Rows:** 299270
- **Size:** 66.59 MB
- **Columns:** `UP_APPLY_ID [int]`, `UP_CLAIM_ID [varchar]`, `UP_ID [int]`, `UP_APPLY_DATE [datetime]`, `UP_PROCEDURE [varchar]`, `UP_REASON [text]`, `UP_UNITS [int]`, `UP_SANC_UNITS [int]`, `UP_ESTIMATE_COST [double]`, `UP_SANC_COST [double]`, `UP_TOTAL_COST [double]`, `UP_SANC_TOTAL [double]`, `UP_REQUERY_ID [int]`, `UP_GROUP_ID [varchar]`, `UP_PROCESS_USER [varchar]`, `UP_PROCESS_STAGE [int]`, `UP_PROCESS_DATE [datetime]`, `UP_RATE_SRNO [int]`, `UP_EXP_SRNO [int]`, `UP_IP_ADDRESS [varchar]`

### `patient_register`
- **Rows:** 211115
- **Size:** 55.16 MB
- **Columns:** `PTR_CARD_ID [varchar]`, `PTR_BEN_ID [bigint]`, `PTR_BENEFICIARY_NAME [varchar]`, `PTR_PATIENT_NAME [varchar]`, `PTR_SERVICE_TYPE [varchar]`, `PTR_SERVICE_RANK [int]`, `PTR_SERVICE_NO [varchar]`, `PTR_UID_NUMBER [varchar]`, `PTR_UID_STATUS [int]`, `PTR_DOB [date]`, `PTR_SEX [varchar]`, `PTR_RELATION_ID [varchar]`, `PTR_PHONE_NO [varchar]`, `PTR_MOBILE [varchar]`, `PTR_EMAIL [varchar]`, `PTR_ADDRESS1 [varchar]`, `PTR_ADDRESS2 [varchar]`, `PTR_ADDRESS3 [varchar]`, `PTR_CITY [varchar]`, `PTR_STATE_ID [varchar]`, `PTR_PIN [varchar]`, `PTR_CARD_ROOM_TYPE [varchar]`, `PTR_CR_USER [varchar]`, `PTR_CR_DATE [datetime]`, `PTR_IP_ADDRESS [varchar]`

### `stay_extension`
- **Rows:** 212284
- **Size:** 47.58 MB
- **Columns:** `SE_APPLY_ID [int]`, `SE_CLAIM_ID [varchar]`, `SE_REQUERY_ID [int]`, `SE_APPLY_DATE [datetime]`, `SE_EXT_ID [int]`, `SE_REASON [text]`, `SE_HOSP_REMARKS [text]`, `SE_PROPOSE_DOD [date]`, `SE_APPROVED_DOD [date]`, `SE_GROUP_ID [varchar]`, `SE_PROCESS_USER [varchar]`, `SE_STAGE_ID [int]`, `SE_PROCESS_STAGE [int]`, `SE_PROCESS_DATE [datetime]`, `SE_FINAL_APP [varchar]`, `SE_REQUERY_BY [varchar]`, `SE_IP_ADDRESS [varchar]`, `SE_ACTIVE [int]`, `SE_FINAL_AUTH [int]`

### `fund_details`
- **Rows:** 323964
- **Size:** 44.09 MB
- **Columns:** `FD_TRAN_ID [int]`, `FD_TRAN_DATE [datetime]`, `FD_TRAN_AMOUNT [decimal]`, `FD_TRAN_COUNT [int]`, `FD_TRAN_TYPE [varchar]`, `FD_SETTLEMENT_ID [int]`, `FD_REMARK [varchar]`, `FD_LAST_UPDATED [datetime]`, `FD_REJECTION_MARK [varchar]`

### `emergency_data_daily`
- **Rows:** 248144
- **Size:** 36.58 MB
- **Columns:** `edd_intimation_id [int]`, `edd_region_id [varchar]`, `edd_cghs_disp_id [varchar]`, `edd_hosp_id [varchar]`, `edd_update_date [datetime]`

### `hosp_audit`
- **Rows:** 775959
- **Size:** 32.56 MB
- **Columns:** `HA_CLAIM_ID [varchar]`, `HA_STAGE [varchar]`, `HA_STATUS [varchar]`, `HA_DATE [date]`

### `bpa_daily_allot`
- **Rows:** 535717
- **Size:** 24.56 MB
- **Columns:** `BDA_ALLOT_ID [int]`, `BDA_SETUP_ID [int]`, `BDA_DATE [date]`, `BDA_FWD [int]`, `BDA_CF_DATE [date]`, `BDA_TARGET [int]`, `BDA_PROCESS [int]`

### `his_hosp_exp`
- **Rows:** 119011
- **Size:** 22.06 MB
- **Columns:** `HE_INTIMATION_ID [varchar]`, `HE_EXP_ID [varchar]`, `HE_CLAIM_AMOUNT [decimal]`, `HE_PAR_AMOUNT [decimal]`, `HE_SUP_AMOUNT [decimal]`, `HE_APP_AMOUNT [decimal]`, `HE_HOS_REMARK [text]`, `HE_PAR_REMARK [text]`, `HE_SUP_REMARK [text]`, `HE_APP_REMARK [text]`, `HE_PAR_EXCESS_AMT [decimal]`, `HE_PAR_IRREV_AMT [decimal]`, `HE_SUP_EXCESS_AMT [decimal]`, `HE_SUP_IRREV_AMT [decimal]`, `HE_APP_EXCESS_AMT [decimal]`, `HE_APP_IRREV_AMT [decimal]`, `HE_HISTORY_ID [int]`

### `ecs_contra`
- **Rows:** 106945
- **Size:** 20.56 MB
- **Columns:** `EC_TRAN_CODE [varchar]`, `EC_USER_NO [varchar]`, `EC_USER_NAME [varchar]`, `EC_CR_REF [varchar]`, `EC_TAPE_NO [varchar]`, `EC_SP_BNK_BRN_SORT_CD [varchar]`, `EC_USER_BNK_ACNO [varchar]`, `EC_FOLIO_NO [varchar]`, `EC_CR_LIMIT [varchar]`, `EC_TOT_AMT [varchar]`, `EC_SETTLE_DT [datetime]`, `EC_RESV_1 [varchar]`, `EC_RESV_2 [varchar]`, `EC_FILLER [varchar]`

### `otp_generator`
- **Rows:** 168468
- **Size:** 19.55 MB
- **Columns:** `OG_ID [int]`, `OG_SECURITY_CODE [varchar]`, `OG_CARD_ID [varchar]`, `OG_MOBILE_NUM [varchar]`, `OG_OTP [varchar]`, `OG_GEN_TIME [datetime]`, `OG_VALID_TIME [datetime]`, `OG_RECV_TIME [datetime]`, `OG_OTP_SUCC [int]`, `OG_IP_ADDRESS [varchar]`

### `unlist_proc_summary`
- **Rows:** 256339
- **Size:** 18.55 MB
- **Columns:** `UPS_ID [int]`, `UPS_CLAIM_ID [varchar]`, `UPS_APPLY_DATE [datetime]`, `UPS_GROUP_ID [varchar]`, `UPS_PROC_DATE [datetime]`, `UPS_NODAL_CLINIC [varchar]`, `UPS_MH [varchar]`, `UPS_IS_TRANSFER [int]`, `UPS_APPX_HOSP [int]`, `UPS_APPX_NODAL [int]`, `UPS_APPX_MH [int]`

### `regionpendency_summary`
- **Rows:** 74119
- **Size:** 18.06 MB
- **Columns:** `rps_rcrd_no [bigint]`, `rps_city_id [varchar]`, `rps_city_name [varchar]`, `rps_HOS_COUNT [int]`, `rps_HOS_AMT [decimal]`, `rps_HOS_NMI_COUNT [int]`, `rps_HOS_NMI_AMT [decimal]`, `rps_VER_COUNT [int]`, `rps_VER_AMT [decimal]`, `rps_BPA_COUNT [int]`, `rps_BPA_AMT [decimal]`, `rps_RC_COUNT [int]`, `rps_RC_AMT [decimal]`, `rps_CORG_COUNT [int]`, `rps_CORG_AMT [decimal]`, `rps_CFA_COUNT [int]`, `rps_CFA_AMT [decimal]`, `rps_DYMD_COUNT [int]`, `rps_DYMD_AMT [decimal]`, `rps_MD_COUNT [int]`, `rps_MD_AMT [decimal]`, `rps_MOD_COUNT [int]`, `rps_MOD_AMT [decimal]`, `rps_ACC_COUNT [int]`, `rps_ACC_AMT [decimal]`, `rps_reprt_dt [date]`, `rps_rp_exctn_dt [timestamp]`

### `bpa_allot_config`
- **Rows:** 125965
- **Size:** 15.55 MB
- **Columns:** `BAC_SETUP_ID [int]`, `BAC_ALLOT_ID [int]`, `BAC_MODE [int]`, `BAC_RANGE_ID [int]`, `BAC_HCF_ID [int]`, `BAC_ENTITY_ID [varchar]`, `BAC_CLAIM_TYPE [varchar]`, `BAC_REGION_ID [varchar]`, `BAC_TARGET [int]`, `BAC_PREV_ID [int]`, `BAC_MAX_AMT [int]`, `BAC_NMI_ENTITY [varchar]`, `BAC_ACTIVE [int]`

### `bpa_serfee_reco`
- **Rows:** 95305
- **Size:** 15.52 MB
- **Columns:** `bsr_settlement_id [decimal]`, `bsr_region_id [varchar]`, `bsr_ser_fee [decimal]`, `bsr_ser_fee_recvd [decimal]`, `bsr_credit_date [datetime]`, `bsr_neft_ref_no [varchar]`, `bsr_neft_amount [decimal]`, `bsr_voucher_no [varchar]`, `bsr_gst_tds [decimal]`, `bsr_diff_fee [decimal]`, `bsr_user_id [varchar]`, `bsr_update_date [datetime]`, `bsr_ip_address [varchar]`

### `budget_forecaster`
- **Rows:** 64386
- **Size:** 14.55 MB
- **Columns:** `bf_crtn_dt [date]`, `bf_office_cghs_city_id [varchar]`, `bf_crm_city_name [varchar]`, `bf_crdramt [decimal]`, `bf_aprpay [decimal]`, `bf_maypay [decimal]`, `bf_junpay [decimal]`, `bf_julpay [decimal]`, `bf_augpay [decimal]`, `bf_seppay [decimal]`, `bf_octpay [decimal]`, `bf_novpay [decimal]`, `bf_decpay [decimal]`, `bf_janpay [decimal]`, `bf_febpay [decimal]`, `bf_marpay [decimal]`, `bf_totpay [decimal]`

### `appr_dealloc`
- **Rows:** 188370
- **Size:** 14.52 MB
- **Columns:** `AD_ID [int]`, `AD_DATE [datetime]`, `AD_COUNTS [int]`, `AD_APP_ID [varchar]`, `AD_REMARKS [text]`, `AD_USER_ID [varchar]`, `AD_IP_ADDRESS [varchar]`

### `user_history`
- **Rows:** 210864
- **Size:** 14.52 MB
- **Columns:** `UH_ID [int]`, `UH_USER_ID [varchar]`, `UH_MODE [int]`, `UH_DONE_BY [varchar]`, `UH_DATE [datetime]`, `UH_PREV_VALUE [varchar]`, `UH_IP_ADDRESS [varchar]`, `UH_UPD_REF [text]`

### `sms_reco`
- **Rows:** 27499
- **Size:** 13.55 MB
- **Columns:** `SBPR_PCODE [varchar]`, `SBPR_ACODE [varchar]`, `SBPR_MOBILE [varchar]`, `SBPR_SENDER_ID [varchar]`, `SBPR_AIR2WEB_ACCEPTED_DATE [datetime]`, `SBPR_CARRIER_ACCEPTED_TIME [datetime]`, `SBPR_STATUS [varchar]`, `SBPR_STATUS_ID [decimal]`, `SBPR_CARRIER_DELVERED_TIME [datetime]`, `SBPR_CARRIER_STATUS [varchar]`, `SBPR_STATUS_DESC [varchar]`, `SBPR_MESSAGE_TEXT [varchar]`, `SBPR_AKN_ID [varchar]`, `SBPR_TRANS_ID [varchar]`

### `ext_stay_summary`
- **Rows:** 215124
- **Size:** 12.52 MB
- **Columns:** `ESU_ID [int]`, `ESU_APPX_HOSP [int]`, `ESU_APPX_OIC [int]`, `ESU_APPX_JDHS [int]`, `ESU_APPX_RCDIR [int]`, `ESU_APPX_MEDDIR [int]`, `ESU_APPX_DYMD [int]`, `ESU_APPX_MD [int]`, `ESU_ACTIVE [int]`

### `his_prop_treatment`
- **Rows:** 115378
- **Size:** 12.03 MB
- **Columns:** `PT_INTIMATION_ID [varchar]`, `PT_TRTYPE_ID [varchar]`, `PR_IS_TREATMENT [varchar]`, `PR_TR_DETAILS [text]`, `PR_ENHANCE_ID [int]`, `PR_PRE_AUTH_ID [int]`, `PT_HISTORY_ID [int]`

### `cda_payment_file`
- **Rows:** 70613
- **Size:** 11.03 MB
- **Columns:** `CPF_UPLOAD_ID [int]`, `CPF_REGION_ID [varchar]`, `CPF_SETTLE_ID [varchar]`, `CPF_SETTLE_DATE [date]`, `CPF_FILE_SIZE [int]`, `CPF_FILE_DATE [datetime]`, `CPF_USER_ID [varchar]`, `CPF_IPADDRESS [varchar]`, `CPF_SETTLED [int]`, `CPF_CLAIM_CNT [int]`, `CPF_PAY_CNT [int]`, `CPF_REJ_CNT [int]`, `CPF_REJ_UPLOAD [int]`, `CPF_ACTIVE [int]`, `CPF_REMARK [text]`

### `empanel_hospital_service`
- **Rows:** 231964
- **Size:** 9.52 MB
- **Columns:** `EHS_OFFICE_ID [varchar]`, `EHS_ID [int]`, `EHS_FACILITY_ID [int]`, `EHS_FROM_DATE [date]`, `EHS_TO_DATE [date]`

### `temp_sett_proc_discard`
- **Rows:** 68437
- **Size:** 9.03 MB
- **Columns:** `SR_NO [int]`, `CLAIM_ID [varchar]`, `CLAIM_AMT [int]`, `OFFICE_NAME [varchar]`, `RUNNING_AMT [int]`

### `bpa_allot_master`
- **Rows:** 23909
- **Size:** 8.58 MB
- **Columns:** `BAM_ALLOT_ID [int]`, `BAM_LEADER_ID [int]`, `BAM_MEMBER_ID [varchar]`, `BAM_ALLOT_DATE [date]`, `BAM_WEEK_DAY [int]`, `BAM_CR_DATE [date]`, `BAM_CR_BY [varchar]`, `BAM_MOD_DATE [date]`, `BAM_MOD_BY [varchar]`, `BAM_SPEC_DAY [int]`, `BAM_SPEC_REASON [text]`, `BAM_CLOSED [int]`

### `new_patient_register`
- **Rows:** 26460
- **Size:** 8.03 MB
- **Columns:** `PTR_CARD_NUMBER [int]`, `PTR_CARD_ID [varchar]`, `PTR_BEN_ID [bigint]`, `PTR_BENEFICIARY_NAME [varchar]`, `PTR_PATIENT_NAME [varchar]`, `PTR_SERVICE_TYPE [varchar]`, `PTR_SERVICE_RANK [int]`, `PTR_SERVICE_NO [varchar]`, `PTR_UID_NUMBER [varchar]`, `PTR_UID_STATUS [int]`, `PTR_DOB [date]`, `PTR_SEX [varchar]`, `PTR_RELATION_ID [varchar]`, `PTR_PHONE_NO [varchar]`, `PTR_MOBILE [varchar]`, `PTR_EMAIL [varchar]`, `PTR_ADDRESS1 [varchar]`, `PTR_ADDRESS2 [varchar]`, `PTR_ADDRESS3 [varchar]`, `PTR_CITY [varchar]`, `PTR_STATE_ID [varchar]`, `PTR_PIN [varchar]`, `PTR_CARD_ROOM_TYPE [varchar]`, `PTR_CR_USER [varchar]`, `PTR_CR_DATE [datetime]`, `PTR_IP_ADDRESS [varchar]`, `PTR_MAIN_CLINIC_ID [varchar]`

### `audit_recovery`
- **Rows:** 132176
- **Size:** 7.52 MB
- **Columns:** `ARV_CLAIM_ID [varchar]`, `ARV_RECOV_FROM [varchar]`, `ARV_SETTLEMENT_ID [varchar]`, `ARV_RECOVER_AMT [decimal]`

### `his_claim_intimation`
- **Rows:** 16250
- **Size:** 6.52 MB
- **Columns:** `CI_INTIMATION_ID [varchar]`, `CI_PATIENT_TYPE [varchar]`, `CI_ADMISSION_NO [varchar]`, `CI_ADMISSION_DATE [datetime]`, `CI_CARD_ID [varchar]`, `CI_BENEFICIARY_NAME [varchar]`, `CI_CARD_TYPE [varchar]`, `CI_CARD_VALID_DT [date]`, `CI_OFFICE_NAME [varchar]`, `CI_OFFICE_DEPARTMENT [varchar]`, `CI_PATIENT_NAME [varchar]`, `CI_AGE [varchar]`, `CI_SEX [varchar]`, `CI_RELATION_ID [varchar]`, `CI_PHONE_NO [varchar]`, `CI_MOBILE [varchar]`, `CI_EMAIL [varchar]`, `CI_ADDRESS1 [varchar]`, `CI_ADDRESS2 [varchar]`, `CI_ADDRESS3 [varchar]`, `CI_CITY [varchar]`, `CI_STATE_ID [varchar]`, `CI_PIN [varchar]`, `CI_CGHS_REGION_ID [varchar]`, `CI_HOSPITAL_ID [varchar]`, `CI_ROOM_TYPE_ID [varchar]`, `CI_REF_TYPE_ID [varchar]`, `CI_ADM_AILMENT [text]`, `CI_PRE_AILMENT_DUR [varchar]`, `CI_IS_RTA [varchar]`, `CI_RTA_REASON [varchar]`, `CI_RTA_DATE [date]`, `CI_RTA_DOC_ID [varchar]`, `CI_INT_STATUS [varchar]`, `CI_INT_STAGE [varchar]`, `CI_CR_USER_ID [varchar]`, `CI_CR_DATE [datetime]`, `CI_CR_OFFICE_ID [varchar]`, `CI_CR_ENTITY_ID [varchar]`, `CI_ROOM_NO [varchar]`, `CI_HOSPITAL_REMARK [text]`, `CI_CARD_ROOM_TYPE `

### `inv_proc_rate_list`
- **Rows:** 71381
- **Size:** 6.52 MB
- **Columns:** `IPRL_REGION_ID [varchar]`, `IPRL_ID [int]`, `IPRL_NABH_RATE [decimal]`, `IPRL_NON_NABH_RATE [decimal]`, `IPRL_SUPER_SPEC_RATE [decimal]`, `IPRL_NC [decimal]`, `IPRL_C [decimal]`, `IPRL_B [decimal]`, `IPRL_A [decimal]`, `IPRL_D [decimal]`, `IPRL_FN [decimal]`, `IPRLREFER [int]`, `IPRL_FROM_DATE [date]`, `IPRL_TO_DATE [date]`, `IPRL_MAIN [int]`

### `bpa_carry_fwd`
- **Rows:** 21609
- **Size:** 6.06 MB
- **Columns:** `BCF_ID [int]`, `BCF_DATE [date]`, `BCF_USER_ID [varchar]`, `BCF_CF_DATE [date]`, `BCF_ACTIVE [int]`

### `cda_reject_history`
- **Rows:** 45325
- **Size:** 5.52 MB
- **Columns:** `CRH_SETTLEMENT_ID [varchar]`, `CRH_NEW_SETTLE_ID [varchar]`, `CRH_CLAIM_ID [varchar]`, `CRH_REJECT_SRNO [int]`, `CRH_REASON [text]`, `CRH_DATE [datetime]`

### `his_clinical_findings_int`
- **Rows:** 36624
- **Size:** 5.03 MB
- **Columns:** `CF_INTIMATION_ID [varchar]`, `CF_CLTEST_ID [varchar]`, `CT_IS_CLTEST [varchar]`, `CF_CLTEST_DETAILS [varchar]`, `CF_ENHANCE_ID [int]`, `CF_HISTORY_ID [int]`

### `his_pre_exist_ailment`
- **Rows:** 41808
- **Size:** 5.03 MB
- **Columns:** `PEA_INTIMATION_ID [varchar]`, `PEA_AILMENT_ID [varchar]`, `PEA_IS_AILMENT [varchar]`, `PEA_AILMENT_DETAILS [varchar]`, `PEA_ENHANCE_ID [int]`, `PEA_HISTORY_ID [int]`

### `user_details`
- **Rows:** 11748
- **Size:** 4.67 MB
- **Columns:** `UD_USER_ID [varchar]`, `UD_ID [int]`, `UD_GROUP_ID [varchar]`, `UD_ENTITY_ID [varchar]`, `UD_PWD [varchar]`, `UD_LOGIN_STATUS [varchar]`, `UD_USER_NAME [varchar]`, `UD_EMAIL_ID [varchar]`, `UD_PHONE_NO [varchar]`, `UD_LOGIN_DATE [datetime]`, `UD_LAST_TRAN_ID [bigint]`, `UD_LOGIN_ATTEMPT [int]`, `UD_PWD_CHANGE [varchar]`, `UD_USER_ACTIVE [varchar]`, `UD_OFFICE_ID [varchar]`, `UD_CERTIFICATE_SERIAL [varchar]`, `UD_ISSUER_ID [varchar]`, `UD_UNIQUE_ID [varchar]`, `UD_PASSWORD_EXPIRY [date]`, `UD_CREATE_DATE [datetime]`, `UD_CLOSED_DATE [datetime]`, `UD_SEC_QUE_ID [varchar]`, `UD_SEC_QUE_ANS [varchar]`, `UD_EMAIL_ID_VER [varchar]`, `UD_EMAIL_VER_TRAN [varchar]`, `UD_EMAIL_VER_CODE [varchar]`, `UD_REG_IP_ADDRESS [varchar]`, `UD_USER_DESIG [varchar]`, `UD_USER_RANK [varchar]`, `UD_MAC_ADDRESS [text]`, `UD_MAC_ADDRESS_2 [text]`, `UD_MAC_MAPPING [int]`, `UD_LOGIN_AFTER [varchar]`, `UD_LOGOUT_BEFORE [varchar]`, `UD_PRE_ALLOTED [varchar]`, `UD_ALREADY_LOGIN [varchar]`, `UD_LOGIN_VERIFY [varchar]`, `UD_SECRET_CODE [varchar]`, `UD_BPA_CENTRE_ID [int]`, `UD_CERT_FILE [varchar]`, `UD_USR_RL [int]`, `UD_U`

### `claim_alert_message`
- **Rows:** 23700
- **Size:** 4.52 MB
- **Columns:** `CAM_ID [int]`, `CAM_CLAIM_ID [varchar]`, `CAM_TOP_PRIOR [int]`, `CAM_MESSAGE [text]`, `CAM_GROUP_ID [varchar]`, `CAM_MESG_DATE [datetime]`, `CAM_MESG_BY [varchar]`, `CAM_POPUP_DATE [datetime]`, `CAM_USER_ID [varchar]`, `CAM_ACTIVE [int]`

### `office_reg_valdate`
- **Rows:** 34782
- **Size:** 4.52 MB
- **Columns:** `ORV_OFFICE_ID [varchar]`, `ORV_VAL_TYPE [varchar]`, `ORV_ID [int]`, `ORV_VAL_FROM [date]`, `ORV_VAL_TO [date]`, `ORV_FULL [int]`, `ORV_TRAN_NO [int]`, `ORV_CREATE_BY [varchar]`, `ORV_CREATE_DATE [datetime]`, `ORV_CREATE_IP [varchar]`, `ORV_UPDATED_BY [varchar]`, `ORV_UPDATE_DATE [datetime]`, `ORV_UPDATE_IP [varchar]`, `ORV_MOU_FILENAME [varchar]`, `ORV_REMARK [text]`

### `temp_claims`
- **Rows:** 95817
- **Size:** 4.52 MB
- **Columns:** `TC_CLAIM_ID [varchar]`, `TC_TIER_ID [int]`, `TC_ACCR [varchar]`, `TC_STAGE [varchar]`, `TC_STATUS [varchar]`, `TC_KEEP [int]`

### `tariff_rates`
- **Rows:** 62522
- **Size:** 3.52 MB
- **Columns:** `TR_CODE [int]`, `TR_REGION_ID [int]`, `TR_CAT_ID [int]`, `TR_RT_TYPE_ID [int]`, `TR_PROC_CODE [int]`, `TR_SUB_CAT_CODE [int]`, `TR_RATE [int]`, `TR_REMARKS [varchar]`

### `office_master`
- **Rows:** 5147
- **Size:** 3.23 MB
- **Columns:** `OM_OFFICE_ID [varchar]`, `OM_OFFICE_NAME [varchar]`, `OM_OFFICE_ADD1 [varchar]`, `OM_OFFICE_ADD2 [varchar]`, `OM_OFFICE_ADD3 [varchar]`, `OM_OFFICE_CITY [varchar]`, `OM_OFFICE_STATE_ID [varchar]`, `OM_OFFICE_PIN [varchar]`, `OM_OFFICE_PHONE [varchar]`, `OM_OFFICE_FAX [varchar]`, `OM_OFFICE_EMAIL [varchar]`, `OM_OFFICE_ALTER_EMAIL [varchar]`, `OM_OFFICE_CONTACT [varchar]`, `OM_OFFICE_CGHS_CITY_ID [varchar]`, `OM_RATE_REGION [varchar]`, `OM_OFFICE_CON_DESG [varchar]`, `OM_OFFICE_PAN [varchar]`, `OM_OFFICE_STAX_NO [varchar]`, `OM_OFFICE_ENTITY_ID [varchar]`, `OM_OFFICE_ACTIVE [varchar]`, `OM_REG_DT [datetime]`, `OM_TAX_EXEMPT [varchar]`, `OM_CGHS_DIS_PERC [decimal]`, `OM_OFFICE_TAN_NO [varchar]`, `OM_OFFICE_STD [varchar]`, `OM_NABH [varchar]`, `OM_NABL [varchar]`, `OM_SUPER [varchar]`, `OM_HOSP_TYPE [varchar]`, `OM_OFFICE_PAOCD [varchar]`, `OM_OFFICE_DDOCD [varchar]`, `OM_OFFICE_PAOREG [varchar]`, `OM_OFFICE_DDOREG [varchar]`, `OM_ACTUAL_REG_DT [datetime]`, `OM_HOSP_TYPES [varchar]`, `OM_CREATED_BY [varchar]`, `OM_IP_ADDRESS [varchar]`, `OM_CATG_ID [int]`, `OM_CONTACT_LEVEL_1 [varchar],`

### `his_referal_details`
- **Rows:** 11234
- **Size:** 2.95 MB
- **Columns:** `REF_INTIMATION_ID [varchar]`, `REF_NUMBER [varchar]`, `REF_CGHS_REGION_ID [varchar]`, `REF_CGHS_DISP_ID [varchar]`, `REF_ISS_DATE [date]`, `REF_ADV_BY [varchar]`, `REF_APP_BY [varchar]`, `REF_HOSPITAL_ID [varchar]`, `REF_ROOM_TYPE_ID [varchar]`, `REF_VAL_DATE [date]`, `REF_SESSIONS [int]`, `REF_PROCEDURES [text]`, `REF_ENTRY_BY [varchar]`, `REF_BAL_SESSION [int]`, `REF_ADM_PROCEDURES [text]`, `REF_INV_PROCEDURES [text]`, `REF_CON_PROCEDURES [text]`, `REF_TRAVEL_REIMBURSE [varchar]`, `REF_ATTENDANT_REIMBURSE [varchar]`, `REF_PATIENT_TYPE [varchar]`, `REF_HISTORY_ID [int]`

### `bpa_cf_setup`
- **Rows:** 37842
- **Size:** 2.52 MB
- **Columns:** `BCS_ID [int]`, `BCS_ALLOT_ID [int]`, `BCS_SETUP_ID [int]`, `BCS_CF_QTY [int]`, `BCS_CF_TARGET [int]`, `BCS_CF_PROCESS [int]`

### `cda_rejection_response`
- **Rows:** 9114
- **Size:** 2.52 MB
- **Columns:** `CRR_CLAIM_ID [varchar]`, `CRR_SETTLEMENT_ID [varchar]`, `CRR_PAYEE_NAME [varchar]`, `CRR_IFSC_CODE [varchar]`, `CRR_ACC_NO [varchar]`, `CRR_PAN [varchar]`, `CRR_ACC_TYPE [varchar]`, `CRR_REASON [text]`, `CRR_REMARK [varchar]`

### `dsc_upload`
- **Rows:** 11112
- **Size:** 2.52 MB
- **Columns:** `DU_OFFICE_ID [varchar]`, `DU_FILE_NAME [varchar]`, `DU_FROM_DATE [date]`, `DU_TO_DATE [date]`, `DU_THUMB_PRINT [varchar]`, `DU_USER_ID [varchar]`, `DU_IP_ADDRESS [varchar]`, `DU_UPLOAD_DATE [datetime]`

### `inv_proc_cert`
- **Rows:** 29808
- **Size:** 2.52 MB
- **Columns:** `IPC_OFFICE_ID [varchar]`, `IPC_VALID_ID [int]`, `IPC_PROC_ID [int]`, `IPC_HOSP_USER [varchar]`, `IPC_ENTRY_DATE [datetime]`, `IPC_CONFIRM [int]`, `IPC_RC_USER [varchar]`, `IPC_CONFIRM_DATE [datetime]`

### `suppliment_process`
- **Rows:** 13946
- **Size:** 2.52 MB
- **Columns:** `SP_ID [int]`, `SP_INTIMATION_ID [varchar]`, `SP_SUPP_ID [int]`, `SP_GROUP_ID [varchar]`, `SP_USER_ID [varchar]`, `SP_PROC_STATUS [varchar]`, `SP_PROC_DATE [datetime]`, `SP_RECOM_AMT [decimal]`, `SP_PROC_REMARKS [text]`, `SP_IN_PROCESS [int]`, `SP_REVERT [varchar]`

### `icd_master`
- **Rows:** 14237
- **Size:** 2.31 MB
- **Columns:** `ICD_CODE [varchar]`, `ICD_DESC [text]`, `ICD_INTERNAL_CODE [int]`, `ICD_LEVEL [int]`, `ICD_PARENT [int]`, `ICD_ACTIVE [varchar]`

### `inv_proc_detail`
- **Rows:** 7888
- **Size:** 1.89 MB
- **Columns:** `IPD_HEADER_ID [int]`, `IPD_ID [int]`, `IPD_RATE_FOR [varchar]`, `IPD_SRNO [varchar]`, `IPD_DESC [varchar]`, `IPD_CODE [varchar]`, `IPD_SUFIX [varchar]`, `IPD_TYPE [varchar]`, `IPD_MODE [varchar]`, `IPD_GENDER [varchar]`, `IPD_PACK_APP [varchar]`

### `bank_master`
- **Rows:** 4492
- **Size:** 1.72 MB
- **Columns:** `BM_BANK_ID [varchar]`, `BM_BANK_NAME [varchar]`, `BM_BANK_BRANCH [varchar]`, `BM_BANK_ADD1 [varchar]`, `BM_BANK_ADD2 [varchar]`, `BM_BANK_ADD3 [varchar]`, `BM_BANK_CITY [varchar]`, `BM_BANK_STATE_ID [varchar]`, `BM_BANK_PIN [varchar]`, `BM_BANK_ACTYPE [varchar]`, `BM_BANK_ACNO [varchar]`, `BM_BANK_MICR [varchar]`, `BM_BANK_IFSC [varchar]`, `BM_OFFICE_ID [varchar]`, `BM_ENTITY_ID [varchar]`, `BM_BANK_STATUS [varchar]`, `BM_PAY_MODE [varchar]`, `BM_PAYEE_NAME [varchar]`

### `pre_auth`
- **Rows:** 2808
- **Size:** 1.63 MB
- **Columns:** `PA_INTIMATION_ID [varchar]`, `PA_DATE [datetime]`, `PA_DIAGNOSIS [text]`, `PA_EST_COST [decimal]`, `PA_CASE_SUMMARY [text]`, `PA_TREAT_MODALITY [text]`, `PA_TREAT_FINALITY [varchar]`, `PA_TREAT_TIME [int]`, `PA_DOCTORS [varchar]`, `PA_PAT_VISIT_DATE [date]`, `PA_TREAT_AUTH [text]`, `PA_TREAT_EFFECT [text]`, `PA_DIAG_RELEVANCE [text]`, `PA_EXT_STAY_REASON [text]`, `PA_EXP_FINALITY_DT [date]`, `PA_REMARK [text]`, `PA_APP_REMARK [text]`, `PA_APPROVED [varchar]`, `PA_APP_BY [varchar]`, `PA_ANY_ATTACHMENT [varchar]`, `PA_AUTH_ID [int]`, `PA_AUTH_FLAG [varchar]`

### `audit_reply_back`
- **Rows:** 3733
- **Size:** 1.52 MB
- **Columns:** `AR_REPLY_ID [int]`, `AR_QUERY_ID [int]`, `AR_REQUERY_ID [int]`, `AR_REPLY [varchar]`, `AR_RECOVER_AMT [decimal]`, `AR_FORWARD_TO [varchar]`, `AR_USER_ID [varchar]`, `AR_REPLY_DATE [datetime]`, `AR_REPLY_BY [varchar]`

### `his_office_reg_valdate`
- **Rows:** 8202
- **Size:** 1.52 MB
- **Columns:** `ORV_OFFICE_ID [varchar]`, `ORV_VAL_FROM [date]`, `ORV_VAL_TO [date]`, `ORV_TRAN_NO [int]`, `ORV_CREATE_BY [varchar]`, `ORV_CREATE_DATE [datetime]`, `ORV_CREATE_IP [varchar]`, `ORV_UPDATED_BY [varchar]`, `ORV_UPDATE_DATE [datetime]`, `ORV_UPDATE_IP [varchar]`, `ORV_MOU_FILENAME [varchar]`, `ORV_VAL_TYPE [varchar]`, `ORV_REMARK [text]`

### `his_web_referral`
- **Rows:** 8786
- **Size:** 1.52 MB
- **Columns:** `WR_TRAN_NO [int]`, `WR_REL_USER_ID [varchar]`, `WR_REL_DATE [datetime]`, `WR_REFERENCE_NO [varchar]`, `WR_CLAIM_ID [varchar]`, `WR_HOSPITAL_ID [varchar]`, `WR_POLYCLINIC_ID [varchar]`, `WR_DATE [datetime]`, `WR_USER_ID [varchar]`, `WR_IP_ADDRESS [varchar]`

### `manual_recovery`
- **Rows:** 1502
- **Size:** 1.52 MB
- **Columns:** `MR_ID [int]`, `MR_HOSPITAL_ID [int]`, `MR_INIT_USER_ID [varchar]`, `MR_DATE [date]`, `MR_REASON [text]`, `MR_AMOUNT [double]`, `MR_RECOVERED [double]`, `MR_STATUS [varchar]`, `MR_STATUS_DATE [datetime]`, `MR_APPR_USER_ID [varchar]`, `MR_CFA_REMARKS [text]`

### `suppliment_claim`
- **Rows:** 2864
- **Size:** 1.52 MB
- **Columns:** `SC_INTIMATION_ID [varchar]`, `SC_SUPP_ID [int]`, `SC_CLAIM_AMT [double]`, `SC_SANCTION_AMT [double]`, `SC_ADDEDUM_AMT [double]`, `SC_JUSTIFY [text]`, `SC_STAGE [varchar]`, `SC_STATUS [varchar]`, `SC_INIT_DATE [datetime]`, `SC_START_APP_DATE [datetime]`, `SC_LAST_USER_ID [varchar]`, `SC_LAST_PROC_DATE [datetime]`, `SC_LAST_RECOM_AMT [double]`, `SC_SETTLEMENT_ID [varchar]`, `SC_FINAL_SETTLE_DT [date]`

## Tier 3: Small/Config Tables (< 1 MB) (Total: 198)
### `bpa_skiped_claim`
- **Rows:** 4189
- **Size:** 0.88 MB
- **Columns:** `BSC_CLAIM_ID [varchar]`, `BSC_ALLOT_ID [int]`, `BSC_SETUP_ID [int]`, `BSC_SKIP_MODE [int]`, `BSC_USER_ID [varchar]`, `BSC_SKIP_DATE [date]`, `BSC_SKIP_TIME [time]`, `BSC_SKIP_TYPE [varchar]`, `BSC_REPLY [int]`, `BSC_SKIP_REASON [text]`, `BSC_PROC_TIME [datetime]`, `BSC_DRAFT_SAVE [int]`, `BSC_FWD [int]`

### `ack_claim_list`
- **Rows:** 7759
- **Size:** 0.83 MB
- **Columns:** `ACL_CLAIM_ID [varchar]`, `ACL_STAGE [varchar]`, `ACL_STATUS [varchar]`, `ACL_INT_DATE [datetime]`, `ACL_ACK_USER [varchar]`, `ACL_ACK_DATE [datetime]`, `ACL_PRIORITY [int]`

### `appr_allot`
- **Rows:** 3056
- **Size:** 0.81 MB
- **Columns:** `AA_CLAIM_ID [varchar]`, `AA_ALLOT_DATE [datetime]`, `AA_ACCEPT_DATE [datetime]`, `AA_CLAIM_AMT [double]`, `AA_SANCTION_AMT [double]`, `AA_AMOUNT [double]`, `AA_STAGE [varchar]`, `AA_STATUS [varchar]`, `AA_REVIEW_CASE [int]`, `AA_BPA_REVIEW_CASE [int]`, `AA_USER_ID [varchar]`, `AA_MANDATORY [int]`

### `his_esm_bank_details`
- **Rows:** 3188
- **Size:** 0.58 MB
- **Columns:** `EBD_HISTORY_ID [int]`, `EBD_CLAIM_ID [varchar]`, `EBD_BANK_NAME [varchar]`, `EBD_BRANCH_NAME [varchar]`, `EBD_IFSC_CODE [varchar]`, `EBD_MICR_CODE [varchar]`, `EBD_ACC_NAME [varchar]`, `EBD_ACC_TYPE [varchar]`, `EBD_ACC_NUMBER [varchar]`, `EBD_UPDATE_DATE [datetime]`, `EBD_IP_ADDRESS [varchar]`, `EBD_USER_ID [varchar]`, `EBD_CHANGE_BY [varchar]`, `EBD_CHANGE_DATE [datetime]`

### `daily_pendency`
- **Rows:** 5712
- **Size:** 0.42 MB
- **Columns:** `DP_DATE [date]`, `DP_REGION_ID [varchar]`, `DP_ENTITY_ID [varchar]`, `DP_PATIENT_TYPE [varchar]`, `DP_ADM_TYPE [varchar]`, `DP_STAGE [varchar]`, `DP_STATUS [varchar]`, `DP_GROUP_ID [varchar]`, `DP_CLAIM_COUNT [int]`, `DP_TOTAL_NET [bigint]`, `DP_TOTAL_SUP [bigint]`, `DP_TOTAL_APP [bigint]`

### `neft_details`
- **Rows:** 2525
- **Size:** 0.41 MB
- **Columns:** `nd_settlement_id [varchar]`, `nd_region_id [varchar]`, `nd_micr_no [varchar]`, `nd_neft_ref_no [varchar]`, `nd_neft_amount [decimal]`, `nd_neft_date [datetime]`, `nd_remarks [text]`, `nd_ip_address [varchar]`, `nd_user_id [varchar]`, `nd_tran_date [datetime]`, `nd_chq_date [datetime]`, `nd_settled_claims [int]`, `nd_settlement_amount [decimal]`, `nd_settlement_UTIFees [decimal]`, `nd_settlement_date [datetime]`

### `his_claim_remarks`
- **Rows:** 1062
- **Size:** 0.36 MB
- **Columns:** `CR_INTIMATION_ID [varchar]`, `CR_USER_ID [varchar]`, `CR_USER_REMARKS [text]`, `CR_UPDATE_DATE [datetime]`, `CR_INT_STAGE [varchar]`, `CR_REMARK_ID [varchar]`, `CR_INT_STATUS [varchar]`, `CR_HISTORY_ID [int]`, `CR_ENHANCE_ID [int]`, `CR_IP_ADDRESS [varchar]`, `CR_AUTO_UPDATE [varchar]`, `CR_CHANGE_ID [int]`, `CR_REQUEST_ID [int]`

### `web_direct_access`
- **Rows:** 5368
- **Size:** 0.33 MB
- **Columns:** `WDA_ID [int]`, `WDA_USER_ID [varchar]`, `WDA_MAC_ADDRESS [varchar]`, `WDA_CHECK_IN [datetime]`

### `sub_district_master`
- **Rows:** 6858
- **Size:** 0.30 MB
- **Columns:** `SDM_CODE [varchar]`, `SDM_NAME [varchar]`, `SDM_DIST_CODE [varchar]`

### `user_allot_tracking`
- **Rows:** 1144
- **Size:** 0.23 MB
- **Columns:** `UAT_TRACKING_ID [bigint]`, `UAT_USER [varchar]`, `UAT_DATE [datetime]`, `UAT_PATIENT_TYPE [varchar]`, `UAT_FROM_AMT [decimal]`, `UAT_TO_AMT [decimal]`, `UAT_CLAIM_ID [varchar]`, `UAT_CLAIM_AMT [decimal]`, `UAT_CURRENT_STAGE [varchar]`, `UAT_CURRENT_STATUS [varchar]`, `UAT_ACCEPT_DATE [datetime]`, `UAT_PROC_STATUS [varchar]`, `UAT_START_TIME [datetime]`, `UAT_END_TIME [datetime]`, `UAT_TRANSFER_ON [datetime]`, `UAT_TRANSFER_BY [varchar]`, `UAT_RANGE_ID [int]`, `UAT_CATG_ID [int]`, `UAT_PRIORITY [int]`, `UAT_PROC_MODE [int]`

### `manual_settlement`
- **Rows:** 657
- **Size:** 0.20 MB
- **Columns:** `MS_CLAIM_ID [varchar]`, `MS_DATE [date]`, `MS_HOSPITAL_ID [int]`, `MS_HOSPITAL_NAME [varchar]`, `MS_HOSP_ADD1 [varchar]`, `MS_HOSP_ADD2 [varchar]`, `MS_HOSP_ADD3 [varchar]`, `MS_HOSP_CITY [varchar]`, `MS_HOSP_STATE_ID [varchar]`, `MS_HOSP_STATE [varchar]`, `MS_HOSP_PIN [varchar]`, `MS_HOSP_PAN [varchar]`, `MS_REGION_ID [varchar]`, `MS_BANK_NAME [varchar]`, `MS_BANK_BRANCH [varchar]`, `MS_IFSC_CODE [varchar]`, `MS_MICR_CODE [varchar]`, `MS_ACC_NUMBER [varchar]`, `MS_CLAIM_AMT [double]`, `MS_APPROVED_AMT [double]`, `MS_ENTRY_USERID [varchar]`, `MS_APPROVAL_STATUS [varchar]`, `MS_APPROVAL_REMARKS [text]`, `MS_APPROVAL_TIME [datetime]`, `MS_APP_USER_ID [varchar]`, `MS_SETTLMENT_ID [decimal]`, `MS_SETTLE_DATE [datetime]`, `MS_FINAL_SETTLE_DT [datetime]`

### `bpa_leave_master`
- **Rows:** 3675
- **Size:** 0.19 MB
- **Columns:** `BLM_USER_ID [varchar]`, `BLM_FROM_DATE [date]`, `BLM_TO_DATE [date]`, `BLM_LEAVE_ID [int]`, `BLM_ACTIVE [int]`

### `tds_challan_det`
- **Rows:** 883
- **Size:** 0.19 MB
- **Columns:** `TCD_TRAN_ID [int]`, `TCD_CGHS_CITY_ID [varchar]`, `TCD_MONTH [int]`, `TCD_YEAR [int]`, `TCD_FY [varchar]`, `TCD_INSTR_TYPE [varchar]`, `TCD_INSTR_NO [varchar]`, `TCD_INSTR_DT [date]`, `TCD_INSTR_AMOUNT [decimal]`, `TCD_DRAWEE_BANK [varchar]`, `TCD_BSR_CODE [varchar]`, `TCD_DEPOSITED_DATE [date]`, `TCD_CHALLAN_NO [varchar]`, `TCD_DEDUCTEE_TYPE [varchar]`, `TCD_SUB_ENTITY_ID [varchar]`

### `red_tax_rate`
- **Rows:** 754
- **Size:** 0.17 MB
- **Columns:** `RTR_RATE_ID [varchar]`, `RTR_PERIOD_FR [date]`, `RTR_PERIOD_TO [date]`, `RTR_SER_TAX [decimal]`, `RTR_ECESS [decimal]`, `RTR_HSCESS [decimal]`, `RTR_SBCESS [decimal]`, `RTR_KKCESS [decimal]`, `RTR_TAX_TYPE [varchar]`, `RTR_OFFICE_ID [varchar]`, `RTR_USER_ID [varchar]`, `RTR_UPDATE_DATE [datetime]`, `RTR_IP_ADDRESS [varchar]`, `RTR_AMT_LIMIT [decimal]`

### `nmi_summary`
- **Rows:** 1199
- **Size:** 0.16 MB
- **Columns:** `NS_OFFICE_ID [varchar]`, `NS_STAGE [varchar]`, `1_COUNT [int]`, `1_AMT [double]`, `2_COUNT [int]`, `2_AMT [double]`, `3_COUNT [int]`, `3_AMT [double]`, `4_COUNT [int]`, `4_AMT [double]`, `5_COUNT [int]`, `5_AMT [double]`, `6_COUNT [int]`, `6_AMT [double]`

### `rates_master`
- **Rows:** 1902
- **Size:** 0.16 MB
- **Columns:** `RM_CAT_ID [varchar]`, `RM_CAT_SUB_ID [varchar]`, `RM_CAT_DESC [varchar]`, `RM_RATE [decimal]`, `RM_CAT_ACTIVE [varchar]`, `RM_REGION_ID [varchar]`, `RM_RATE_TYPE [varchar]`

### `manual_recovery_details`
- **Rows:** 2388
- **Size:** 0.14 MB
- **Columns:** `MRD_ID [int]`, `MRD_RECOV_FROM [varchar]`, `MRD_SETTLEMENT_ID [varchar]`, `MRD_RECOVER_AMT [decimal]`

### `user_allot_setup`
- **Rows:** 1732
- **Size:** 0.14 MB
- **Columns:** `UAS_USER_ID [varchar]`, `UAS_IP_CASE [varchar]`, `UAS_OPD_CASE [varchar]`, `UAS_FROM_DATE [date]`, `UAS_TO_DATE [date]`, `UAS_IPD_RANGE [int]`, `UAS_OPD_RANGE [int]`, `UAS_TIME_START [varchar]`, `UAS_TIME_END [varchar]`, `UAS_PER_DAY_ALLOCATE [int]`, `UAS_MAC_ADDR [varchar]`, `UAS_UPDATE_ON [datetime]`, `UAS_UPDATE_BY [varchar]`

### `pendency_master`
- **Rows:** 160
- **Size:** 0.13 MB
- **Columns:** `PM_ID [int]`, `PM_ENTITY_ID [varchar]`, `PM_STAGE [varchar]`, `PM_STATUS [varchar]`, `PM_DESP_ID [int]`, `PM_GROUP_ID [varchar]`, `PM_BPA_ZERO [int]`, `PM_FROM_AMT [int]`, `PM_TO_AMT [int]`, `PM_NXT_GROUP_ID [varchar]`, `PM_IS_FINAL [int]`, `PM_IS_ACCEPT [int]`, `PM_IS_NMI [int]`, `PM_IS_REVIEW [int]`, `PM_IS_REPLY [int]`, `PM_NMI_LIMIT [int]`, `PM_DISPLAY [int]`, `PM_ORDER [int]`, `PM_DOC_RECD [int]`, `PM_DOC_VERIFY [int]`

### `event_messages`
- **Rows:** 209
- **Size:** 0.11 MB
- **Columns:** `EM_EVENT_ID [int]`, `EM_FROM_DATE [datetime]`, `EM_TO_DATE [datetime]`, `EM_MESSAGE_TEXT [text]`, `EM_USER_ID [varchar]`, `EM_IP_ADDRESS [varchar]`, `EM_STATUS [varchar]`

### `ifa_allot_summary`
- **Rows:** 926
- **Size:** 0.09 MB
- **Columns:** `IAS_ID [int]`, `IAS_USER_ID [varchar]`, `IAS_DATE [datetime]`, `IAS_PAT_TYPE [varchar]`, `IAS_STATUS [varchar]`, `IAS_CLAIM_TYPE [varchar]`, `IAS_ALLOTED [int]`, `IAS_PERC [int]`, `IAS_PROC [int]`, `IAS_ESCLATE [int]`, `IAS_FWD_CFA [int]`

### `ifa_setting`
- **Rows:** 34
- **Size:** 0.09 MB
- **Columns:** `IFS_ID [int]`, `IFS_PERIOD_ID [int]`, `IFS_GROUP_ID [varchar]`, `IFS_STATUS_ID [int]`, `IFS_NEXT_GROUP_ID [varchar]`, `IFS_ESCLATE_NUM [int]`, `IFS_ESCLATE_MODE [int]`, `IFS_IS_FINAL [int]`, `IFS_ACCEPT [int]`, `IFS_ORDER_ID [int]`, `IFS_START [int]`, `IFS_NMI [int]`, `IFS_REPLY [int]`, `IFS_MODE [varchar]`

### `region_budget_details`
- **Rows:** 528
- **Size:** 0.09 MB
- **Columns:** `RBD_TRAN_NO [int]`, `RBD_REGION_ID [varchar]`, `RBD_TRAN_DATE [date]`, `RBD_TRAN_AMOUNT [decimal]`, `RBD_TRAN_TYPE [varchar]`, `RBD_REMARK [text]`, `RBD_UPDATE_DATE [datetime]`, `RBD_USER_ID [varchar]`, `RBD_IP_ADDRESS [varchar]`

### `service_fees`
- **Rows:** 10
- **Size:** 0.09 MB
- **Columns:** `SF_FEES_ID [varchar]`, `SF_PERIOD_FR [date]`, `SF_PERIOD_TO [date]`, `SF_BILL_AMT_FR [decimal]`, `SF_BILL_AMT_TO [decimal]`, `SF_SER_FEES [decimal]`, `SF_SOURCE_ENTITY_ID [varchar]`

### `suppliment_remarks`
- **Rows:** 0
- **Size:** 0.09 MB
- **Columns:** `SR_INTIMATION_ID [varchar]`, `SR_SUPP_ID [int]`, `SR_USER_ID [varchar]`, `SR_USER_REMARKS [text]`, `SR_UPDATE_DATE [datetime]`, `SR_INT_STAGE [varchar]`, `SR_INT_STATUS [varchar]`, `SR_IP_ADDRESS [varchar]`, `SR_AUTO_UPDATE [varchar]`, `SR_CHANGE_ID [int]`, `SR_REQUEST_ID [int]`

### `bpa_allot_stage`
- **Rows:** 13
- **Size:** 0.08 MB
- **Columns:** `BAS_GROUP_ID [varchar]`, `BAS_ID [int]`, `BAS_STAGE [varchar]`, `BAS_STATUS [varchar]`, `BAS_TYPE [varchar]`

### `bpa_allot_status`
- **Rows:** 9
- **Size:** 0.08 MB
- **Columns:** `BAS_GROUP_ID [varchar]`, `BAS_ID [int]`, `BAS_STAGE [varchar]`, `BAS_STATUS [varchar]`, `BAS_TYPE [varchar]`

### `claim_lock`
- **Rows:** 141
- **Size:** 0.08 MB
- **Columns:** `cl_claim_id [varchar]`, `cl_session_id [varchar]`, `cl_user_id [varchar]`, `cl_ip_address [varchar]`, `cl_lock_date [datetime]`

### `daily_allot_summary`
- **Rows:** 1009
- **Size:** 0.08 MB
- **Columns:** `DAS_USER_ID [varchar]`, `DAS_DATE [date]`, `DAS_ALLOT_TYPE [int]`, `DAS_SETUP_ID [int]`, `DAS_TARGET [int]`, `DAS_DONE [int]`

### `his_office_master`
- **Rows:** 74
- **Size:** 0.08 MB
- **Columns:** `OM_OFFICE_ID [varchar]`, `OM_OFFICE_NAME [varchar]`, `OM_OFFICE_ADD1 [varchar]`, `OM_OFFICE_ADD2 [varchar]`, `OM_OFFICE_ADD3 [varchar]`, `OM_OFFICE_CITY [varchar]`, `OM_OFFICE_STATE_ID [varchar]`, `OM_OFFICE_PIN [varchar]`, `OM_OFFICE_PHONE [varchar]`, `OM_OFFICE_FAX [varchar]`, `OM_OFFICE_EMAIL [varchar]`, `OM_OFFICE_ALTER_EMAIL [varchar]`, `OM_OFFICE_CONTACT [varchar]`, `OM_OFFICE_CGHS_CITY_ID [varchar]`, `OM_OFFICE_CON_DESG [varchar]`, `OM_OFFICE_PAN [varchar]`, `OM_OFFICE_STAX_NO [varchar]`, `OM_OFFICE_ENTITY_ID [varchar]`, `OM_OFFICE_ACTIVE [varchar]`, `OM_REG_DT [datetime]`, `OM_TAX_EXEMPT [varchar]`, `OM_CGHS_DIS_PERC [decimal]`, `OM_NABH [varchar]`, `OM_HISTORY_ID [varchar]`, `OM_USER_ID [varchar]`, `OM_UPDATE_DATE [datetime]`, `OM_IP_ADDRESS [varchar]`

### `pend_schd`
- **Rows:** 520
- **Size:** 0.08 MB
- **Columns:** `PS_ID [int]`, `PS_DATE [date]`, `PS_START_TIME [datetime]`, `PS_END_TIME [datetime]`, `PS_RC_REC [int]`, `PS_OFF_REC [int]`

### `reimb_recovery`
- **Rows:** 273
- **Size:** 0.08 MB
- **Columns:** `RR_RECOVERY_ID [int]`, `RR_CLAIM_ID [varchar]`, `RR_SERVICE_NO [varchar]`, `RR_RECOVERY_AMT [decimal]`, `RR_RECOVERED_AMT [decimal]`, `RR_BALANCE_AMT [decimal]`, `RR_REMARK [text]`

### `cghs_holiday`
- **Rows:** 241
- **Size:** 0.06 MB
- **Columns:** `CH_HOL_ID [decimal]`, `CH_HOL_DATE [date]`, `CH_HOL_REASON [varchar]`, `CH_NOT_TAT [int]`, `CH_HOL_ACTIVE [varchar]`, `CH_USER_ID [varchar]`, `CH_IP_ADDRESS [varchar]`, `CH_UPDATE_DATE [datetime]`

### `district_master`
- **Rows:** 731
- **Size:** 0.06 MB
- **Columns:** `DM_CODE [varchar]`, `DM_NAME [varchar]`, `DM_STATE_CODE [varchar]`

### `district_state`
- **Rows:** 644
- **Size:** 0.06 MB
- **Columns:** `DM_DISTRICT_CODE [varchar]`, `DM_DISTRICT_NAME [varchar]`, `DM_STATE_CODE [varchar]`, `DM_STATE_NAME [varchar]`

### `mm_menu_master`
- **Rows:** 362
- **Size:** 0.06 MB
- **Columns:** `MM_LEVEL_1 [int]`, `MM_LEVEL_2 [int]`, `MM_LEVEL_3 [int]`, `MM_LEVEL_4 [int]`, `MM_MENU_ITEM [varchar]`, `MM_MENU_LINK [varchar]`, `MM_ALWAYS_DISPLAY [varchar]`, `MM_ITEM_DESCRIPTION [varchar]`, `MM_HEAD_ID [int]`, `MM_ORDER_ID [int]`, `MM_MENU_ACTION [varchar]`, `MM_DAYS_LIMIT [int]`

### `parameter_range`
- **Rows:** 51
- **Size:** 0.06 MB
- **Columns:** `PS_RANGE_ID [int]`, `PS_ID [int]`, `PS_FROM_DATE [date]`, `PS_TO_DATE [date]`, `PS_FROM_RANGE [decimal]`, `PS_TO_RANGE [decimal]`, `PS_SHORT_CODE [varchar]`, `PS_MIN_LIMIT [int]`, `PS_MAX_LIMIT [int]`

### `referal_city`
- **Rows:** 466
- **Size:** 0.06 MB
- **Columns:** `rc_region_id [varchar]`, `rc_city_id [varchar]`, `rc_city_name [varchar]`, `rc_city_active [varchar]`

### `reimb_recovery_details`
- **Rows:** 557
- **Size:** 0.06 MB
- **Columns:** `RRD_ID [int]`, `RRD_RECOV_FROM [varchar]`, `RRD_SETTLEMENT_ID [int]`, `RRD_RECOVER_AMT [decimal]`

### `state_district_master`
- **Rows:** 0
- **Size:** 0.06 MB
- **Columns:** `DSM_STATE_CODE [varchar]`, `DSM_STATE_NAME [varchar]`, `DSM_DIST_CODE [varchar]`, `DSM_DIST_NAME [varchar]`, `DSM_SUB_DIST_CODE [varchar]`, `DSM_SUB_DIST_VER [varchar]`, `DSM_SUB_DIST_NAME [varchar]`, `DSM_SUB_DIST_NAME_LOCAL [varchar]`, `DSM_CENSUS_2001_CODE [varchar]`, `DSM_CENSUS_2011_CODE [varchar]`

### `tax_rate`
- **Rows:** 8
- **Size:** 0.06 MB
- **Columns:** `TR_RATE_ID [varchar]`, `TR_PERIOD_FR [date]`, `TR_PERIOD_TO [date]`, `TR_SER_TAX [decimal]`, `TR_ECESS [decimal]`, `TR_HSCESS [decimal]`, `TR_SBCESS [decimal]`, `TR_KKCESS [decimal]`, `TR_GSTTDS [decimal]`, `TR_TAX_TYPE [varchar]`

### `ur_user_rights`
- **Rows:** 645
- **Size:** 0.06 MB
- **Columns:** `UR_USER_TYPE [varchar]`, `UR_LEVEL_1 [int]`, `UR_LEVEL_2 [int]`, `UR_LEVEL_3 [int]`, `UR_LEVEL_4 [int]`, `UR_GRP_ID [varchar]`, `UR_RESTRICTED_USER [varchar]`, `UR_NOTVALID_USER [varchar]`, `UR_PILOT_REGION [varchar]`, `UR_PILOT_OFFICE [varchar]`

### `approval_documents`
- **Rows:** 0
- **Size:** 0.05 MB
- **Columns:** `AD_ID [int]`, `AD_APP_ID [int]`, `AD_DOC_ID [varchar]`, `AD_REMARK [text]`, `AD_FILENAME [varchar]`, `AD_RECEIVED [varchar]`, `AD_REC_REMARK [text]`, `AD_REC_REMARK_ID [varchar]`, `AD_SUBMIT_TIME [datetime]`, `AD_FILE_SRNO [int]`, `AD_FILE_SIZE [decimal]`, `AD_SIGNED [int]`

### `audit_questionare`
- **Rows:** 45
- **Size:** 0.05 MB
- **Columns:** `AQ_QUE_ID [int]`, `AQ_INTIMATION_ID [varchar]`, `AQ_QUESTION_1 [varchar]`, `AQ_AUDITOR_STATUS [varchar]`, `AQ_QUESTION_2 [varchar]`, `AQ_AAO_STATUS [varchar]`, `AQ_QUESTION_3 [varchar]`, `AQ_SAO_STATUS [varchar]`, `AQ_REPLY [varchar]`, `AQ_STATUS [varchar]`, `AQ_DATE_1 [datetime]`, `AQ_DATE_2 [datetime]`, `AQ_DATE_3 [datetime]`, `AQ_REPLY_DATE [datetime]`

### `auto_allot_users`
- **Rows:** 657
- **Size:** 0.05 MB
- **Columns:** `AAU_USER_ID [varchar]`, `AAU_LAST_DATE [datetime]`, `AAU_LAST_CLAIM [varchar]`, `AAU_ACTIVE [int]`

### `calendar_year`
- **Rows:** 15
- **Size:** 0.05 MB
- **Columns:** `CY_YEAR [int]`, `CY_START_DATE [date]`, `CY_END_DATE [date]`, `CY_DESC [varchar]`

### `cghs_region_master`
- **Rows:** 34
- **Size:** 0.05 MB
- **Columns:** `CRM_CITY_ID [varchar]`, `CRM_CITY_NAME [varchar]`, `CRM_CITY_CODE [varchar]`, `CRM_RC_CODE [varchar]`, `CRM_CDA_CODE [varchar]`, `CRM_STATE_ID [varchar]`, `CRM_ACTIVE [varchar]`, `CRM_PROC_RATE [varchar]`, `CRM_LAB_RATE [varchar]`, `CRM_CDA_REGION_ID [varchar]`, `CRM_RATE_REMARK [text]`, `CRM_EXP_BREAK [varchar]`, `CRM_UID_CHECK [varchar]`, `CRM_GSTTDS [varchar]`, `CRM_CURR_RATIO [decimal]`, `CRM_SAME_REGION [int]`

### `dashboard_det`
- **Rows:** 97
- **Size:** 0.05 MB
- **Columns:** `dash_group [varchar]`, `dash_stage [varchar]`, `dash_status [varchar]`, `dash_desp [varchar]`, `dash_history [varchar]`, `dash_enhance [varchar]`, `dash_short_desc [varchar]`, `dash_srno [int]`, `dash_group_id [varchar]`, `dash_entity_id [varchar]`, `dash_que [varchar]`

### `financial_year`
- **Rows:** 14
- **Size:** 0.05 MB
- **Columns:** `FY_YEAR [int]`, `FY_START_DATE [date]`, `FY_END_DATE [date]`, `FY_DESC [varchar]`

### `temp_bpa_serfee_reco`
- **Rows:** 123
- **Size:** 0.05 MB
- **Columns:** `bsr_settlement_id [decimal]`, `bsr_region_id [varchar]`, `bsr_ser_fee [decimal]`, `bsr_ser_fee_recvd [decimal]`, `bsr_credit_date [datetime]`, `bsr_neft_ref_no [varchar]`, `bsr_neft_amount [decimal]`, `bsr_voucher_no [varchar]`, `bsr_gst_tds [decimal]`, `bsr_diff_fee [decimal]`, `bsr_user_id [varchar]`, `bsr_update_date [datetime]`, `bsr_ip_address [varchar]`

### `user_group`
- **Rows:** 44
- **Size:** 0.05 MB
- **Columns:** `UG_GROUP_ID [varchar]`, `UG_GROUP_NAME [varchar]`, `UG_SHORT_CODE [varchar]`, `UG_GROUP_ENTITY_ID [varchar]`, `UG_GROUP_LEVEL [int]`, `UG_GROUP_ACTIVE [varchar]`, `UG_AMT_LOWER_LIMIT [decimal]`, `UG_AMT_UPPER_LIMIT [decimal]`, `UG_INT_STAGE_CODE [varchar]`, `UG_REGION_MODE [varchar]`, `UG_SESSION_LIMIT [int]`, `UG_MULTIPLE_LOGIN [varchar]`

### `adv_paym_cheque`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `APC_APPLY_ID [int]`, `APC_BANK_NAME [varchar]`, `APC_BANK_BRANCH [varchar]`, `APC_ACC_NO [varchar]`, `APC_CHQ_NO [varchar]`, `APC_CHQ_DT [date]`, `APC_CHQ_AMT [int]`, `APC_CLAIM_ID [varchar]`, `APC_USER_ID [varchar]`, `APC_DATE [datetime]`

### `advance_payment`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `AP_APPLY_ID [int]`, `AP_PAT_TYPE [varchar]`, `AP_INIT_BY [varchar]`, `AP_APPLY_DATE [datetime]`, `AP_ADV_REQ_ID [int]`, `AP_CLAIM_ID [varchar]`, `AP_BENF_ID [int]`, `AP_PARENT_OIC [varchar]`, `AP_LIST_HOSP_ID [int]`, `AP_HOSP_NAME [varchar]`, `AP_ADMIT_DATE [date]`, `AP_AILMENT [text]`, `AP_TREATMENT [text]`, `AP_AMT_EST [int]`, `AP_COMMENTS [text]`, `AP_PROC_ID [int]`, `AP_GROUP_ID [varchar]`, `AP_PROC_USER [varchar]`, `AP_PROC_DATE [datetime]`, `AP_PROC_REMARK [text]`, `AP_REQUERY_BY [varchar]`, `AP_AMT_SANC [int]`, `AP_ACTIVE [int]`

### `application_settings`
- **Rows:** 64
- **Size:** 0.03 MB
- **Columns:** `AS_ID [int]`, `AS_CODE [varchar]`, `AS_VALUE [text]`, `AS_IP [varchar]`, `AS_ACTIVE [int]`

### `city_tier_master`
- **Rows:** 4
- **Size:** 0.03 MB
- **Columns:** `CTM_ID [int]`, `CTM_NAME [varchar]`, `CTM_ACTIVE [int]`

### `claim_in_progress`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `CIP_CLAIM_ID [int]`, `CIP_USER_ID [varchar]`, `CIP_ALLOT_ID [int]`, `CIP_SETUP_ID [int]`, `CIP_DATE [datetime]`, `CIP_SKIP_LIST [int]`, `CIP_NMI_LIST [int]`

### `consult_map`
- **Rows:** 59
- **Size:** 0.03 MB
- **Columns:** `CM_ID [int]`, `CM_FROM_DATE [date]`, `CM_TO_DATE [date]`, `CM_PROC_ID [int]`

### `daily_allot_changes`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `DAC_ID [int]`, `DAC_SETUP_ID [int]`, `DAC_DATE [date]`, `DAC_CHANGES [int]`

### `diag_type`
- **Rows:** 4
- **Size:** 0.03 MB
- **Columns:** `DT_DIAG_TYPE_ID [varchar]`, `DT_DIAG_TYPE_CODE [varchar]`, `DT_DIAG_TYPE_DESC [varchar]`, `DT_DIAG_TYPE_ACTIVE [varchar]`, `DT_DIAG_STAGE [varchar]`

### `ecs_region`
- **Rows:** 13
- **Size:** 0.03 MB
- **Columns:** `ER_REGION_ID [varchar]`, `ER_REGION_CODE [varchar]`, `ER_REGION_NAME [varchar]`, `ER_REGION_ACIVE [varchar]`

### `his_bank_master`
- **Rows:** 56
- **Size:** 0.03 MB
- **Columns:** `BM_BANK_ID [varchar]`, `BM_BANK_NAME [varchar]`, `BM_BANK_BRANCH [varchar]`, `BM_BANK_ADD1 [varchar]`, `BM_BANK_ADD2 [varchar]`, `BM_BANK_ADD3 [varchar]`, `BM_BANK_CITY [varchar]`, `BM_BANK_STATE_ID [varchar]`, `BM_BANK_PIN [varchar]`, `BM_BANK_ACTYPE [varchar]`, `BM_BANK_ACNO [varchar]`, `BM_BANK_MICR [varchar]`, `BM_BANK_IFSC [varchar]`, `BM_OFFICE_ID [varchar]`, `BM_ENTITY_ID [varchar]`, `BM_BANK_STATUS [varchar]`, `BM_PAY_MODE [varchar]`, `BM_PAYEE_NAME [varchar]`, `BM_HISTORY_ID [int]`, `BM_USER_ID [varchar]`, `BM_UPDATE_DATE [datetime]`, `BM_IP_ADDRESS [varchar]`

### `his_opd_ph_answers`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `opd_ans_id [int]`, `opd_ans_anyhistory [varchar]`, `opd_ans_details [varchar]`, `opd_claim_id [varchar]`, `opd_history_ID [int]`

### `ifa_allot`
- **Rows:** 121
- **Size:** 0.03 MB
- **Columns:** `IA_CLAIM_ID [varchar]`, `IA_ALLOT_ID [int]`, `IA_STAGE [varchar]`, `IA_STATUS [varchar]`, `IA_ACCEPT_DATE [datetime]`, `IA_CLAIM_AMT [double]`, `IA_SANCTION_AMT [double]`, `IA_AMOUNT [double]`

### `inv_proc_header`
- **Rows:** 223
- **Size:** 0.03 MB
- **Columns:** `IPH_ID [int]`, `IPH_HEADER [varchar]`, `IPH_START [int]`, `IPH_END [int]`, `IPH_HEAD_TYPE [varchar]`, `IPH_GROUP [varchar]`, `IPH_PRIORITY [int]`

### `member_request`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `MR_ID [int]`, `MR_REQUERY_ID [int]`, `MR_BENF_ID [int]`, `MR_PARENT_OIC [varchar]`, `MR_CLAIM_ID [varchar]`, `MR_REQ_DATE [datetime]`, `MR_HOSP_NAME [varchar]`, `MR_INIT_BY [varchar]`, `MR_PAT_TYPE [varchar]`, `MR_ADMIT_DATE [date]`, `MR_CATG_ID [int]`, `MR_TREATMENT [text]`, `MR_VISIT_REASON [text]`, `MR_PROC_REM [text]`, `MR_COMMENTS [text]`, `MR_PROC_DATE [datetime]`, `MR_GROUP_ID [varchar]`, `MR_PERMIT_ID [int]`, `MR_NMI_BY [varchar]`, `MR_DRAFT_SAVE [int]`, `MR_ACTIVE [int]`

### `notice_list`
- **Rows:** 83
- **Size:** 0.03 MB
- **Columns:** `NL_NOT_TYPE_ID [varchar]`, `NL_NOT_ID [varchar]`, `NL_NOT_SHORT_DESC [varchar]`, `NL_NOT_FILE_NAME [varchar]`, `NL_ACTIVE [varchar]`, `NL_NOT_DESC [text]`

### `notice_type`
- **Rows:** 10
- **Size:** 0.03 MB
- **Columns:** `NT_NOT_TYPE_ID [varchar]`, `NT_NOT_TYPE_DESC [varchar]`, `NT_NOT_TYPE_ACTIVE [varchar]`

### `offc_bed_typ_mstr`
- **Rows:** 6
- **Size:** 0.03 MB
- **Columns:** `obtm_typ_id [int]`, `obtm_typ_descp [varchar]`, `obtm_typ_status [int]`, `obtm_typ_crt_dt [date]`, `obtm_lstupdt_usr [varchar]`, `obtm_lstupdt_dt [datetime]`, `obtm_order [int]`

### `offc_bsc_info`
- **Rows:** 119
- **Size:** 0.03 MB
- **Columns:** `OBI_ID [int]`, `obi_OFFC_ID [varchar]`, `obi_bsc_inf_typ [int]`, `obi_CNT [int]`, `obi_actv_frm_dt [date]`, `obi_actv_to_dt [date]`, `obi_lstupdt_usr [varchar]`, `obi_lstupdt_dt [datetime]`

### `patient_type`
- **Rows:** 2
- **Size:** 0.03 MB
- **Columns:** `PT_TYPE_ID [varchar]`, `PT_TYPE_DESC [varchar]`, `PT_TYPE_CODE [varchar]`, `PT_TYPE_ACTIVE [varchar]`

### `pay_mode`
- **Rows:** 4
- **Size:** 0.03 MB
- **Columns:** `PM_PAY_MODE_ID [varchar]`, `PM_PAY_MODE_DESC [varchar]`, `PM_PAY_MODE_CODE [varchar]`, `PM_PAY_MODE_ACTIVE [varchar]`

### `phy_instr_mode`
- **Rows:** 2
- **Size:** 0.03 MB
- **Columns:** `PIM_INSTR_MODE_ID [varchar]`, `PIM_INSTR_MODE_DESC [varchar]`, `PIM_INSTR_MODE_CODE [varchar]`, `PIM_INSTR_MODE_ACTIVE [varchar]`

### `rank_master`
- **Rows:** 146
- **Size:** 0.03 MB
- **Columns:** `rm_service_code [varchar]`, `rm_rank_id [int]`, `rm_rank_def [varchar]`, `RM_SINFO_ID [int]`, `rm_active [varchar]`, `rm_room_type_id [varchar]`

### `room_type`
- **Rows:** 6
- **Size:** 0.03 MB
- **Columns:** `RT_TYPE_ID [varchar]`, `RT_TYPE_DESC [varchar]`, `RT_TYPE_CODE [varchar]`, `RT_ACTIVE [varchar]`, `RR_DISPLAY_ORDER [int]`, `RT_ENTITLE [int]`

### `seq_mem_req`
- **Rows:** 0
- **Size:** 0.03 MB
- **Columns:** `SQ_REQ_ID [int]`, `SQ_KEY [int]`

### `waiver_criteria`
- **Rows:** 12
- **Size:** 0.03 MB
- **Columns:** `WC_ID [int]`, `WC_TYPE_ID [int]`, `WC_START_DATE [date]`, `WC_END_DATE [date]`, `WC_FROM [int]`, `WC_TO [int]`, `WC_UNIT [varchar]`, `WC_DISCHARED [int]`, `WC_WO_REFERRAL [int]`, `WC_CLAIM_SUBMIT [int]`, `WC_WAIVER_REQD [int]`, `WC_NOT_ALLOW [int]`, `WC_REASON [varchar]`, `WC_IP [int]`, `WC_OP [int]`, `WC_PH [int]`

### `account_type_master`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `ATM_ID [int]`, `ATM_NAME [varchar]`, `ATM_ECS_CODE [varchar]`, `ATM_ACTIVE [int]`

### `adv_paym_event`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `APE_EVENT_ID [int]`, `APE_APPLY_ID [int]`, `APE_GROUP_ID [varchar]`, `APE_NMI_COUNT [int]`, `APE_PROC_ID [int]`, `APE_DATE [datetime]`, `APE_AMT_EST [int]`, `APE_BENF_REMARK [text]`, `APE_AMT_SANC [int]`, `APE_PROC_REMARK [text]`, `APE_USER_ID [varchar]`, `APE_IP_ADDR [varchar]`, `APE_IS_REVERTED [int]`

### `adv_paym_process`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `APP_PROC_ID [int]`, `APP_GROUP_ID [varchar]`, `APP_STATUS_ID [int]`, `APP_NEXT_GROUP_ID [varchar]`, `APP_IS_APPLY [int]`, `APP_IS_NMI [int]`, `APP_IS_REPLY [int]`, `APP_IS_ACCEPT [int]`, `APP_IS_FINAL [int]`, `APP_APPR_LIMIT [int]`, `APP_ORDER [int]`

### `adv_paym_status`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `APS_ID [int]`, `APS_STATUS [varchar]`

### `adv_payment_setting`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `APS_ID [int]`, `APS_FROM_DATE [date]`, `APS_TO_DATE [date]`, `APS_LUMPSUM [int]`, `APS_PERCENT [decimal]`

### `ailment_code`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `AC_AILMENT_ID [varchar]`, `AC_AILMENT_DESC [varchar]`, `AC_AILMENT_ACTIVE [varchar]`

### `amt_ded_reason`
- **Rows:** 12
- **Size:** 0.02 MB
- **Columns:** `ADR_ID [int]`, `ADR_PAT_TYPE [varchar]`, `ADR_EXP_ID [int]`, `ADR_DESC [varchar]`, `ADR_ACTIVE [int]`

### `app_property`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `AP_KEY [varchar]`, `AP_VALUE [varchar]`, `AP_FROM_DATE [datetime]`, `AP_TO_DATE [datetime]`, `AP_ACTIVE [int]`

### `applicant_master`
- **Rows:** 15
- **Size:** 0.02 MB
- **Columns:** `AM_ID [int]`, `AM_DESC [varchar]`

### `appr_allot_setting`
- **Rows:** 4
- **Size:** 0.02 MB
- **Columns:** `AAS_FROM_DATE [date]`, `AAS_TO_DATE [date]`, `AAS_FROM_AMT [double]`, `AAS_TO_AMT [double]`, `AAS_MAND_PERC [double]`

### `bank_actype`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `BA_ACTYPE_ID [varchar]`, `BA_ACTYPE_DESC [varchar]`, `BA_ACTYPE_CODE [varchar]`, `BA_ACTYPE_ACTIVE [varchar]`

### `bpa_allot_type`
- **Rows:** 5
- **Size:** 0.02 MB
- **Columns:** `BAT_ID [int]`, `BAT_DESC [varchar]`, `BAT_ALLOW_SKIP [int]`, `BAT_PRIORITY [int]`, `BAT_TAR_PRIORITY [int]`, `BAT_STATUS [varchar]`, `BAT_SAME_USER [int]`, `BAT_PROC_MODE [int]`, `BAT_ADD_TARGET [int]`, `BAT_CNT_TARGET [int]`, `BAT_ACTIVE [int]`, `BAT_FRESH [int]`, `BAT_OWN [int]`, `BAT_RESIGNED [int]`, `BAT_OTHERS [int]`, `BAT_ABSENT [int]`

### `bpa_sites`
- **Rows:** 4
- **Size:** 0.02 MB
- **Columns:** `BS_ID [int]`, `BS_NAME [varchar]`, `BS_HOSTS [text]`, `BS_ACTIVE [int]`

### `category_master`
- **Rows:** 25
- **Size:** 0.02 MB
- **Columns:** `CM_CAT_ID [varchar]`, `CM_CAT_DESC [varchar]`, `CM_ACTIVE [varchar]`

### `cghs_card_type`
- **Rows:** 3
- **Size:** 0.02 MB
- **Columns:** `CT_TYPE_ID [varchar]`, `CT_TYPE_DESC [varchar]`, `CT_ACTIVE [varchar]`

### `check_list`
- **Rows:** 13
- **Size:** 0.02 MB
- **Columns:** `CL_TYPE_ID [varchar]`, `CL_TYPE_DESC [varchar]`, `CL_TYPE_ACTIVE [varchar]`

### `city_master`
- **Rows:** 2
- **Size:** 0.02 MB
- **Columns:** `CM_CITY_ID [varchar]`, `CM_CITY_NAME [varchar]`, `CM_STATE_ID [varchar]`, `CM_ACTIVE [varchar]`

### `claim_category`
- **Rows:** 40
- **Size:** 0.02 MB
- **Columns:** `CC_CAT_ID [int]`, `CC_HEAD_ID [int]`, `CC_CAT_DESC [varchar]`, `CC_ACTIVE [int]`

### `claim_catg_header`
- **Rows:** 3
- **Size:** 0.02 MB
- **Columns:** `CCH_ID [int]`, `CCH_DESC [varchar]`

### `claim_enhancement`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `CE_INTIMATION_ID [varchar]`, `CE_ENHANCE_ID [int]`, `CE_ENHANCE_DATE [datetime]`, `CE_AILMENT [varchar]`, `CE_STAGE [varchar]`, `CE_STATUS [varchar]`, `CE_USERID [varchar]`

### `claim_sequence`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `ID [bigint]`, `MIN_VALUE [int]`, `MAX_VALUE [bigint]`, `RESET_ON_MAX [varchar]`, `RESET_FREQUENCY [varchar]`, `LAST_ACCESS_ON [datetime]`

### `claim_work_sheet`
- **Rows:** 312
- **Size:** 0.02 MB
- **Columns:** `cws_intimation_id [varchar]`, `cws_work_sheet [varchar]`

### `claimstage_description`
- **Rows:** 26
- **Size:** 0.02 MB
- **Columns:** `CSD_STAGE [varchar]`, `CSD_STATUS [varchar]`, `CSD_DESCP [varchar]`, `CSD_DESCP_DASHBOARD [varchar]`, `CSD_LIST_TITLE [varchar]`, `CSD_LIST_TITLE_DB [varchar]`, `CSD_PAGE_TITLE [varchar]`, `CSD_PAGE_TITLE_DB [varchar]`

### `clinical_test_type`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `CFT_CLTEST_ID [varchar]`, `CFT_CLTEST_DESC [varchar]`, `CFT_CLTEST_ACTIVE [varchar]`

### `consult_types`
- **Rows:** 31
- **Size:** 0.02 MB
- **Columns:** `CT_ID [int]`, `CT_NAME [varchar]`, `CT_ACTIVE [int]`

### `country_master`
- **Rows:** 2
- **Size:** 0.02 MB
- **Columns:** `CM_ID [int]`, `CM_NAME [varchar]`, `CM_CNTRY_CODE [varchar]`, `CM_NORTH_LAT [decimal]`, `CM_SOUTH_LAT [decimal]`, `CM_EAST_LON [decimal]`, `CM_WEST_LON [decimal]`

### `dash_group_master`
- **Rows:** 27
- **Size:** 0.02 MB
- **Columns:** `dash_grp_id [varchar]`, `dash_grp_desc [varchar]`, `dash_grp_srno [decimal]`

### `dbt_xml_detail`
- **Rows:** 50
- **Size:** 0.02 MB
- **Columns:** `DXD_HEADER_ID [int]`, `DXD_ID [int]`, `DXD_ORDER_NUM [int]`, `DXD_XML_TAG [text]`, `DXD_XML_DESP [text]`, `DXD_BPA_SOURCE [int]`, `DXD_BPA_FIELD [varchar]`, `DXD_DEF_VALUE [varchar]`, `DXD_ACTIVE [int]`

### `dbt_xml_header`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `DXH_ID [int]`, `DXH_XML_TAG [varchar]`, `DXH_XML_TEXT [text]`

### `dbt_xml_transaction`
- **Rows:** 88
- **Size:** 0.02 MB
- **Columns:** `DXT_YEAR [int]`, `DXT_MONTH [int]`, `DXT_ID [int]`, `DXT_DATE [date]`, `DXT_VALUE [varchar]`

### `deduction_reasons`
- **Rows:** 3
- **Size:** 0.02 MB
- **Columns:** `DR_ID [int]`, `DR_NAME [varchar]`, `DR_ACTIVE [int]`

### `del_prop_treatment`
- **Rows:** 126
- **Size:** 0.02 MB
- **Columns:** `PT_INTIMATION_ID [varchar]`, `PT_TRTYPE_ID [varchar]`, `PR_IS_TREATMENT [varchar]`, `PR_TR_DETAILS [text]`, `PR_ENHANCE_ID [int]`, `PR_PRE_AUTH_ID [int]`

### `disability_master`
- **Rows:** 25
- **Size:** 0.02 MB
- **Columns:** `DM_ID [int]`, `DM_DESC [varchar]`, `DM_WHITE_CARD [int]`

### `discharge_type`
- **Rows:** 5
- **Size:** 0.02 MB
- **Columns:** `DT_TYPE_ID [varchar]`, `DT_TYPE_DESC [varchar]`, `DT_TYPE_ACTIVE [varchar]`, `DT_TYPE_CODE [varchar]`

### `doc_check_list`
- **Rows:** 9
- **Size:** 0.02 MB
- **Columns:** `DCL_DOC_ID [varchar]`, `DCL_DOC_DESC [varchar]`, `DCL_DOC_NAME [varchar]`, `DCL_ACTIVE [varchar]`

### `doc_mgrt_ngc_list2`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `dmnl_id [int]`, `dmnl_fld1 [varchar]`, `dmnl_fld2 [varchar]`, `dmnl_fld3 [varchar]`, `dmnl_fld4 [varchar]`, `dmnl_doc_sz [varchar]`, `dmnl_doc_mnth [varchar]`, `dmnl_doc_dt [varchar]`, `dmnl_doc_yr [varchar]`, `dmnl_doc_clmid [varchar]`, `dmnl_doc_upld_tm [datetime]`

### `document_list`
- **Rows:** 45
- **Size:** 0.02 MB
- **Columns:** `DL_DOC_ID [varchar]`, `DL_DOC_DESC [varchar]`, `DL_DOC_TYPE_ID [varchar]`, `DL_DOC_ACTIVE [varchar]`, `DL_DOC_NAME_CONV [varchar]`, `DL_IS_MULT_DOC [varchar]`, `DL_MUL_DOC_NAME_CONV [varchar]`, `DL_SRNO [int]`, `DL_DISPLAY_ORDER [int]`, `DL_FOR_IP [int]`, `DL_FOR_OPD [int]`, `DL_IP_STAGE [int]`, `DL_OPD_STAGE [int]`, `DL_FOR_MEMBILL [int]`, `DL_IP_MANDATORY [int]`, `DL_OP_MANDATORY [int]`, `DL_REF [int]`, `DL_EMER [int]`

### `document_require`
- **Rows:** 57
- **Size:** 0.02 MB
- **Columns:** `DR_DOC_ID [varchar]`, `DR_CLAIM_TYPE [varchar]`, `DR_PT_TYPE [varchar]`, `DR_IS_REQ [int]`, `DR_IS_MAND [int]`, `DR_IS_REF [int]`, `DR_IS_EMER [int]`, `DR_INT_STAGE [int]`, `DR_SUB_STAGE [int]`, `DR_ORDER [int]`, `DR_CONDITION [text]`

### `document_type`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `DT_DOCTYPE_ID [varchar]`, `DT_DOCTYPE_DESC [varchar]`, `DT_DOCTYPE_ACTIVE [varchar]`, `DT_SUBMIT_BY [varchar]`, `DT_SRNO [int]`

### `ecs_control`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `EC_USER_NO [varchar]`, `EC_USER_NAME [varchar]`, `EC_SP_BNK_BRN_SORT_CD [varchar]`, `EC_USER_BNK_ACNO [varchar]`, `EC_CR_LIMIT [varchar]`, `EC_ACTIVE [varchar]`, `EC_CGHS_CITY_ID [varchar]`, `EC_PAY_MODE [varchar]`

### `empanel_facility`
- **Rows:** 300
- **Size:** 0.02 MB
- **Columns:** `EF_HEADER_ID [int]`, `EF_FACILITY_ID [int]`, `EF_FACILITY [varchar]`

### `empanel_header`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `EH_ID [int]`, `EH_NAME [varchar]`

### `exp_category`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `EC_ID [int]`, `EC_DESC [varchar]`, `EC_ACTIVE [int]`

### `expense_group`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `EG_GROUP_ID [int]`, `EG_GROUP_NAME [varchar]`, `EG_ADD_COL [varchar]`

### `expense_header`
- **Rows:** 12
- **Size:** 0.02 MB
- **Columns:** `EH_EXP_ID [varchar]`, `EH_EXP_SUBID [varchar]`, `EH_EXP_DESC [varchar]`, `EH_EXP_ACTIVE [varchar]`, `EH_DISP_ORDER [int]`

### `expense_type`
- **Rows:** 12
- **Size:** 0.02 MB
- **Columns:** `ET_EXPTYPE_ID [int]`, `ET_EXPTYPE_DESC [varchar]`, `ET_RATE_TYPE [varchar]`, `ET_RATE_CATG [varchar]`, `ET_ORDER [int]`, `ET_CATEGORY [varchar]`, `ET_NEW_ORDER [int]`

### `ext_stay_process`
- **Rows:** 37
- **Size:** 0.02 MB
- **Columns:** `ESP_ID [int]`, `ESP_SET_ID [int]`, `ESP_GROUP_ID [varchar]`, `ESP_ACTION [varchar]`, `ESP_STATUS_ID [int]`, `ESP_NEXT_GROUP_ID [varchar]`, `ESP_IS_FINAL [int]`, `ESP_IS_ACCEPT [int]`, `ESP_ORDER_ID [int]`, `ESP_NMI [int]`, `ESP_REPLY_NMI [int]`, `ESP_DOC_REQ [int]`, `ESP_DOC_ID [int]`

### `extended_stay_setting`
- **Rows:** 4
- **Size:** 0.02 MB
- **Columns:** `ESS_ID [int]`, `ESS_FROM_DATE [date]`, `ESS_TO_DATE [date]`, `ESS_FROM_DAYS [int]`, `ESS_TO_DAYS [int]`, `ESS_GROUP_LEVEL_1 [varchar]`, `ESS_GROUP_LEVEL_2 [varchar]`, `ESS_GROUP_LEVEL_3 [varchar]`, `ESS_PERM_REQ [int]`, `ESS_APPX_CODE [varchar]`

### `feedback_query`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `FQ_ID [int]`, `FQ_QUERY [varchar]`, `FQ_ACTIVE [int]`

### `feedback_rating`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `FR_CLAIM_ID [varchar]`, `FR_QUERY_ID [int]`, `FR_RATING [int]`

### `gender_type`
- **Rows:** 2
- **Size:** 0.02 MB
- **Columns:** `gender_ID [varchar]`, `gender_desc [varchar]`

### `group_sanction_limit`
- **Rows:** 28
- **Size:** 0.02 MB
- **Columns:** `GSL_GROUP_ID [varchar]`, `GSL_LOWER_LIMIT [decimal]`, `GSL_UPPER_LIMIT [decimal]`

### `groupwise_status`
- **Rows:** 60
- **Size:** 0.02 MB
- **Columns:** `GS_GROUP_ID [varchar]`, `GS_INT_STAGE [varchar]`, `GS_INT_STATUS [varchar]`, `GS_REMARK_ID [varchar]`, `GS_REMARK_DESC [varchar]`, `GS_REMARK_ACTIVE [varchar]`, `GS_INOUT_TYPE [varchar]`, `GS_DE_LIST_TITLE [varchar]`, `GS_DB_LIST_TITLE [varchar]`, `GS_DB_PAGE_TITLE [varchar]`, `GS_DE_PAGE_TITLE [varchar]`

### `health_care_facility`
- **Rows:** 11
- **Size:** 0.02 MB
- **Columns:** `HCF_ID [int]`, `HCF_CATEGORY [varchar]`, `HCF_DISP_ORDER [int]`, `HCF_PRIORITY [int]`

### `his_audit_remarks`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `AR_INTIMATION_ID [varchar]`, `AR_REM_TYPE_ID [varchar]`, `AR_HOS_REMARK [text]`, `AR_PAR_REMARK [text]`, `AR_SUP_REMARK [text]`, `AR_APP_REMARK [text]`, `AR_HISTORY_ID [int]`

### `hos_types`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `hos_type_id [int]`, `hos_type_description [varchar]`, `hos_type_code [varchar]`

### `hosp_exp_head`
- **Rows:** 11
- **Size:** 0.02 MB
- **Columns:** `HEH_EXP_ID [varchar]`, `HEH_EXP_DESC [varchar]`, `HEH_EXP_ACTIVE [varchar]`, `HEH_DISP_ORDER [int]`, `HEH_FOR_IP [int]`, `HEH_FOR_OPD [int]`, `HEH_DISP_MEMBER [int]`

### `hosp_revenue_dtls`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `hrd_office_id [varchar]`, `hrd_rev_fy [int]`, `hrd_rev_amt [decimal]`, `hrd_mrk_dt [date]`, `hrd_lstupdt_dt [datetime]`, `hrd_lstupdt_usr [varchar]`

### `ifa_period`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `IP_ID [int]`, `IP_FROM_DATE [date]`, `IP_TO_DATE [date]`, `IP_ACTIVE [int]`

### `ifa_status`
- **Rows:** 9
- **Size:** 0.02 MB
- **Columns:** `IS_ID [int]`, `IS_DESC [varchar]`, `IS_DISPLAY [int]`

### `ifa_timing`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `IT_ID [int]`, `IP_ESC_DATE [date]`, `IP_MODE [varchar]`, `IT_START_TIME [datetime]`, `IT_END_TIME [datetime]`, `IT_COUNT [int]`, `IT_EXCEP [text]`

### `last_tran_details`
- **Rows:** 57
- **Size:** 0.02 MB
- **Columns:** `LTD_TRAN_TYPE_ID [varchar]`, `LTD_LAST_NO [int]`, `LTD_TRAN_DESC [varchar]`, `LTD_TRAN_TYPE_ACTIVE [varchar]`

### `leave_master`
- **Rows:** 3
- **Size:** 0.02 MB
- **Columns:** `LM_ID [int]`, `LM_NAME [varchar]`, `LM_AT_WORK [int]`, `LM_ACTIVE [int]`

### `login_type`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `LT_ID [int]`, `LT_TYPE [varchar]`

### `member_permit_process`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `MPP_ID [int]`, `MPP_MAJOR [int]`, `MPP_GROUP_ID [varchar]`, `MPP_STATUS_ID [int]`, `MPP_NEXT_GROUP_ID [varchar]`, `MPP_IS_START [int]`, `MPP_IS_NMI [int]`, `MPP_IS_REPLY [int]`, `MPP_IS_ACCEPT [int]`, `MPP_IS_FINAL [int]`

### `member_permit_status`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `MPS_ID [int]`, `MPS_DESC [varchar]`

### `member_request_events`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `MRE_APPLY_ID [int]`, `MRE_REQUERY_ID [int]`, `MRE_GROUP_ID [varchar]`, `MRE_DATE [datetime]`, `MRE_REASON [text]`, `MRE_COMMENTS [text]`, `MRE_PERMIT_ID [int]`, `MRE_USER_ID [varchar]`

### `menu_header`
- **Rows:** 25
- **Size:** 0.02 MB
- **Columns:** `mh_group_id [int]`, `mh_header [varchar]`

### `office_emp_purpose`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `OEP_OFFICE_ID [varchar]`, `OEP_ID [int]`, `OEP_PURPOSE [text]`

### `office_holiday`
- **Rows:** 283
- **Size:** 0.02 MB
- **Columns:** `OH_ID [int]`, `OH_OFFICE_ID [varchar]`

### `opd_ph_question`
- **Rows:** 2
- **Size:** 0.02 MB
- **Columns:** `opd_question_id [int]`, `opd_questions [varchar]`, `opd_active [varchar]`

### `ot_setup`
- **Rows:** 27
- **Size:** 0.02 MB
- **Columns:** `OT_ID [int]`, `OT_EMPTYPE [int]`, `OT_DAY [int]`, `OT_FULLDAY [int]`, `OT_FROM_TIME [time]`, `OT_TO_TIME [time]`, `OT_FINISH_REG [int]`, `OT_SCH_TIME [int]`, `OT_ACTIVE [int]`

### `other_last_tran_details`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `LTD_TRAN_TYPE_ID [varchar]`, `LTD_LAST_NO [int]`, `LTD_TRAN_DESC [varchar]`, `LTD_TRAN_TYPE_ACTIVE [varchar]`

### `other_recovery`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `OR_CLAIM_ID [varchar]`, `OR_RECOV_FROM [varchar]`, `OR_SETTLEMENT_ID [varchar]`, `OR_RECOVER_AMT [decimal]`, `OR_REMARK [text]`

### `par_ext_duration`
- **Rows:** 3
- **Size:** 0.02 MB
- **Columns:** `PED_DAYS [int]`, `PED_ACTIVE [varchar]`

### `parameter_master`
- **Rows:** 2
- **Size:** 0.02 MB
- **Columns:** `PM_ID [int]`, `PM_DESC [varchar]`, `PM_UNIT [varchar]`

### `parametric_attributes`
- **Rows:** 15
- **Size:** 0.02 MB
- **Columns:** `PA_ID [int]`, `PA_ATTRIBUTE [varchar]`, `PA_TYPE [varchar]`

### `parametric_values`
- **Rows:** 30
- **Size:** 0.02 MB
- **Columns:** `PV_ID [int]`, `PV_GROUP_ID [varchar]`, `PV_FROM_DATE [date]`, `PV_TO_DATE [date]`, `PV_VALUE [varchar]`

### `passwordpolicy`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `pw_expiry [int]`, `pw_history [int]`, `ps_min_length [int]`, `pw_man_special [varchar]`, `pw_special_chars [varchar]`, `pw_man_numeric [varchar]`, `pw_man_upper [varchar]`, `pw_change_before [int]`, `pw_login_attempts [int]`, `pw_from_date [date]`, `pw_to_date [date]`

### `payment_instruction`
- **Rows:** 46
- **Size:** 0.02 MB
- **Columns:** `PI_REC_ID [varchar]`, `PI_PAY_VAL_DT [datetime]`, `PI_PROD_CODE [varchar]`, `PI_DEB_AC_NO [varchar]`, `PI_BEN_CODE [varchar]`, `PI_BEN_NAME [varchar]`, `PI_INSTR_REF_NO [varchar]`, `PI_INSTR_AMT [varchar]`, `PI_PAY_LOC_CODE [varchar]`, `PI_PAY_BRANCH_CODE [varchar]`, `PI_BEN_BANK_CODE [varchar]`, `PI_BEN_BANK_BRC_CODE [varchar]`, `PI_BEN_AC_NO [varchar]`, `PI_BEN_AC_TYPE [varchar]`, `PI_BEN_ADD1 [varchar]`, `PI_BEN_ADD2 [varchar]`, `PI_BEN_ADD3 [varchar]`, `PI_BEN_ADD4 [varchar]`, `PI_BEN_ZIP_CODE [varchar]`, `PI_DEL_MODE [varchar]`, `PI_OTC_PER [varchar]`, `PI_DISP_TO [varchar]`, `PI_DISP_TO_BRC_CODE [varchar]`, `PI_DISP_LOC_CODE [varchar]`, `PI_DISP_TO_ADD1 [varchar]`, `PI_DISP_TO_ADD2 [varchar]`, `PI_DISP_TO_ADD3 [varchar]`, `PI_DISP_TO_ADD4 [varchar]`, `PI_DISP_TO_ZIP_CODE [varchar]`, `PI_CHQ_NO [varchar]`, `PI_ISSUE_REF_NO [varchar]`, `PI_WAR_NO [varchar]`, `PI_FOLIO_NO [varchar]`, `PI_ENRC_TXT1 [varchar]`, `PI_ENCR_TXT2 [varchar]`, `PI_ENCR_TXT3 [varchar]`, `PI_ENCR_TXT4 [varchar]`, `PI_ENCR_TXT5 [varchar]`, `PI_ENCR_TXT6 [varchar]`, `PI_ENCR_TXT7 [varchar]`, `PI_ENCR_TXT8 [varchar`

### `phy_instr_det`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `PID_TRAN_NO [decimal]`, `PID_INSTR_NO [varchar]`, `PID_INSTR_DT [date]`, `PID_INSTR_TYPE [varchar]`, `PID_INSTR_AMOUNT [decimal]`, `PID_DRAWEE_BANK [varchar]`, `PID_INSTR_REMARK [text]`, `PID_USER_ID [varchar]`, `PID_TRAN_DATE [datetime]`, `PID_IP_ADDRESS [varchar]`

### `pndgrprt`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `clm_id [varchar]`, `bnfry_nm [varchar]`, `ptnt_nm [varchar]`, `card_no [varchar]`, `srvc_no [varchar]`, `pty_typ [varchar]`, `loc [varchar]`, `hosp_nm [varchar]`, `admtn_dt [datetime]`, `submtn_dt [datetime]`, `clm_amt [decimal]`, `submt_to [varchar]`, `rcpt_dt [datetime]`, `rcpt_frm [varchar]`, `stg [varchar]`

### `prior_app_setting`
- **Rows:** 9
- **Size:** 0.02 MB
- **Columns:** `PAS_GROUP_ID [varchar]`, `PAS_STAGE [int]`, `PAS_NEXT_GROUP [varchar]`, `PAS_FINAL [int]`

### `prior_approval`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `PA_CLAIM_ID [varchar]`, `PA_APPLY_DATE [datetime]`, `PA_HOSPITAL [varchar]`, `PA_REASON [varchar]`, `PA_REIM_TYPE [varchar]`, `PA_ESTIMATE_COST [double]`, `PA_REQUERY_ID [int]`, `PA_GROUP_ID [varchar]`, `PA_REQUERY_BY [varchar]`, `PA_PROCESS_USER [varchar]`, `PA_PROCESS_STAGE [int]`, `PA_PROCESS_DATE [datetime]`, `PA_FINAL_STAGE [int]`, `PA_IP_ADDRESS [varchar]`

### `prior_approval_events`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `PAE_CLAIM_ID [varchar]`, `PAE_REQUERY_ID [int]`, `PAE_GROUP_ID [varchar]`, `PAE_USER_ID [varchar]`, `PAE_STATUS [int]`, `PAE_DATE [datetime]`, `PAE_REPLY [text]`, `PAE_PROCESS_REMARKS [text]`, `PAE_IP_ADDRESS [varchar]`

### `process_alert`
- **Rows:** 5
- **Size:** 0.02 MB
- **Columns:** `PA_GROUP_ID [varchar]`, `PA_FROM_DATE [date]`, `PA_TO_DATE [date]`, `PA_PATIENT_TYPE [varchar]`, `PA_STAGE [varchar]`, `PA_LIMIT [int]`, `PA_DIFF_TYPE [varchar]`, `PA_DAYS_TYPE [varchar]`

### `recovery_type`
- **Rows:** 9
- **Size:** 0.02 MB
- **Columns:** `RT_ID [int]`, `RT_DESC [varchar]`, `RT_FINANCE [varchar]`, `RT_ACTIVE [varchar]`

### `referal_type`
- **Rows:** 2
- **Size:** 0.02 MB
- **Columns:** `RT_TYPE_ID [varchar]`, `RT_TYPE_DESC [varchar]`, `RT_TYPE_ACTIVE [varchar]`, `RT_TYPE_CODE [varchar]`

### `region_budget_allocate`
- **Rows:** 28
- **Size:** 0.02 MB
- **Columns:** `RBA_REGION_ID [varchar]`, `RBA_BUDGET_AMOUNT [decimal]`

### `reimb_type`
- **Rows:** 12
- **Size:** 0.02 MB
- **Columns:** `RT_TYPE_ID [varchar]`, `RT_TYPE_DESC [varchar]`, `RT_TYPE_ACTIVE [varchar]`, `RT_EIR_REQ [int]`

### `rej_settle_history`
- **Rows:** 119
- **Size:** 0.02 MB
- **Columns:** `RSH_SETTLEMENT_ID [varchar]`, `RSH_ENTITY_ID [varchar]`, `RSH_DATE [date]`, `RSH_REGION_ID [varchar]`

### `relation_master`
- **Rows:** 13
- **Size:** 0.02 MB
- **Columns:** `RM_RELATION_ID [varchar]`, `RM_RELATION_NAME [varchar]`, `RM_SINFO_ID [int]`, `RM_SINFO_RELATION_NAME [varchar]`, `RM_RELATION_ACTIVE [varchar]`

### `remark_type`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `RT_REM_TYPE_ID [varchar]`, `RT_REM_TYPE_DESC [varchar]`, `RT_REM_TYPE_ACTIVE [varchar]`, `RT_DISP_ORDER [int]`

### `report_param`
- **Rows:** 36
- **Size:** 0.02 MB
- **Columns:** `RP_REP_ID [varchar]`, `RP_RANGE_FR [decimal]`, `RP_RANGE_TO [decimal]`, `RP_RANGE_AGE_FR [int]`, `RP_RANGE_AGE_TO [int]`, `RP_TRAN_ID [int]`

### `room_rates`
- **Rows:** 18
- **Size:** 0.02 MB
- **Columns:** `RR_TYPE [varchar]`, `RR_FROM_DATE [date]`, `RR_TO_DATE [date]`, `RR_RATE [decimal]`, `RR_NABH [decimal]`, `RR_NON_NABH [decimal]`, `RR_CGHS_CODE [varchar]`, `RR_TYPE_ID [int]`, `RR_REGION_ID [varchar]`

### `service_master`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `sm_code [varchar]`, `sm_desc [varchar]`, `SM_SINFO_ID [int]`, `sm_active [varchar]`

### `settlement_last_tran_details`
- **Rows:** 6
- **Size:** 0.02 MB
- **Columns:** `LTD_TRAN_TYPE_ID [varchar]`, `LTD_LAST_NO [int]`, `LTD_TRAN_DESC [varchar]`, `LTD_TRAN_TYPE_ACTIVE [varchar]`

### `standard_remarks`
- **Rows:** 9
- **Size:** 0.02 MB
- **Columns:** `SR_REM_TYPE_ID [varchar]`, `SR_REM_DESC [varchar]`, `SR_REM_TEXT [text]`, `VR_REM_ACTIVE [varchar]`

### `state_master`
- **Rows:** 49
- **Size:** 0.02 MB
- **Columns:** `SM_STATE_ID [varchar]`, `SM_STATE_NAME [varchar]`, `ST_SINFO_ID [int]`, `SM_COUNTRY_ID [int]`, `SM_ISO_CODE [varchar]`, `SM_IS_UT [int]`, `SM_IT_CODE [varchar]`, `SM_TIN_NUM [int]`, `SM_ACTIVE [varchar]`

### `status_master`
- **Rows:** 13
- **Size:** 0.02 MB
- **Columns:** `SM_STATUS_ID [varchar]`, `SM_STATUS_NAME [varchar]`, `SM_STATUS_ACTIVE [varchar]`

### `statuswise_remarks`
- **Rows:** 34
- **Size:** 0.02 MB
- **Columns:** `SR_STATUS_ID [varchar]`, `SR_REMARK_ID [varchar]`, `SR_REMARK_DESC [varchar]`, `SR_REMARK_ACTIVE [varchar]`, `SR_TO_STAGE [varchar]`, `SR_TO_STATUS [varchar]`, `SR_DASHBOARD [varchar]`, `SR_INOUT_TYPE [varchar]`, `SR_STAGE_STATUS_REMARK [varchar]`

### `stayext_status_master`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `SSM_ID [int]`, `SSM_STATUS [varchar]`

### `sub_category`
- **Rows:** 13
- **Size:** 0.02 MB
- **Columns:** `sub_cat_id [int]`, `sub_cat_desc [varchar]`, `sub_cat_active [varchar]`

### `tat_monitor`
- **Rows:** 59
- **Size:** 0.02 MB
- **Columns:** `tm_scheme [varchar]`, `tm_date [date]`, `tm_ip_cnt [int]`, `tm_ip_amt [decimal]`, `tm_op_cnt [int]`, `tm_op_amt [decimal]`

### `temp_extra_exp`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `TXP_OFFICE_ID [varchar]`, `TXP_CLAIM_ID [varchar]`, `TXP_ID [decimal]`, `TXP_SRNO [int]`, `TXP_PROC_ID [int]`, `TXP_CAT_ID [varchar]`, `TXP_HOS_RATE [decimal]`, `TXP_NON_ACCR_RATE [decimal]`, `TXP_DIFF_RATE [decimal]`, `TXP_DIFF_AMT [decimal]`, `TXP_STAGE [varchar]`, `TXP_STATUS [varchar]`

### `temp_extra_rates`
- **Rows:** 159
- **Size:** 0.02 MB
- **Columns:** `TER_CLAIM_ID [varchar]`, `TER_OFFICE_ID [varchar]`, `TER_ACCR [varchar]`, `TER_DIFF_AMT [int]`, `TER_DIFF_CNT [int]`, `TER_TIER_ID [int]`, `TER_STAGE [varchar]`, `TER_STATUS [varchar]`

### `treatment_type`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `TT_TRTYPE_ID [varchar]`, `TT_TRTYPE_DESC [varchar]`, `TT_TRTYPE_ACTIVE [varchar]`

### `treatment_waiver`
- **Rows:** 8
- **Size:** 0.02 MB
- **Columns:** `TW_ID [int]`, `TW_DESC [varchar]`, `TW_MAJOR [int]`, `TW_ACTIVE [int]`, `TW_ORDER [int]`

### `uid_status`
- **Rows:** 5
- **Size:** 0.02 MB
- **Columns:** `US_ID [int]`, `US_DESC [varchar]`, `US_ACTIVE [varchar]`, `US_DISP_ORDER [int]`

### `user_allot_weekly_off`
- **Rows:** 6
- **Size:** 0.02 MB
- **Columns:** `UAW_SETUP_ID [int]`, `UAW_MON [int]`, `UAW_TUE [int]`, `UAW_WED [int]`, `UAW_THUS [int]`, `UAW_FRI [int]`, `UAW_SAT [int]`, `UAW_SUN [int]`

### `user_entity`
- **Rows:** 11
- **Size:** 0.02 MB
- **Columns:** `UE_ENTITY_ID [varchar]`, `UE_ENTITY_DESC [varchar]`, `UE_ACTIVE [varchar]`

### `user_group_queue`
- **Rows:** 37
- **Size:** 0.02 MB
- **Columns:** `UGQ_GROUP_ID [varchar]`, `UGQ_INT_STAGE [varchar]`, `UGQ_INT_STATUS [varchar]`, `UGQ_PENDING_AT [varchar]`

### `user_profile_parameter`
- **Rows:** 17
- **Size:** 0.02 MB
- **Columns:** `UPP_ID [int]`, `UPP_VALUE [varchar]`, `UPP_STORE_PREV [int]`

### `user_security_question`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `USQ_QUE_ID [varchar]`, `USQ_QUESTION [varchar]`, `USQ_QUE_ACTIVE [varchar]`

### `user_sequence`
- **Rows:** 0
- **Size:** 0.02 MB
- **Columns:** `ID [bigint]`, `MIN_VALUE [int]`, `MAX_VALUE [bigint]`, `RESET_ON_MAX [varchar]`, `RESET_FREQUENCY [varchar]`, `LAST_ACCESS_ON [datetime]`

### `verifier_remarks`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `VR_REM_TYPE_ID [varchar]`, `VR_REM_DESC [varchar]`, `VR_REM_ACTIVE [varchar]`

### `waiver_appr_process`
- **Rows:** 72
- **Size:** 0.02 MB
- **Columns:** `WAP_ID [int]`, `WAP_CRITERIA_ID [int]`, `WAP_GROUP_ID [varchar]`, `WAP_STATUS_ID [int]`, `WAP_NEXT_GROUP_ID [varchar]`, `WAP_IS_FINAL [int]`, `WAP_ACCEPT [int]`, `WAP_ORDER_ID [int]`, `WAP_REPLY_NMI [int]`, `WAP_APPLY_STAGE [int]`, `WAP_NMI [int]`, `WAP_REPLY_REJECT [int]`

### `waiver_status_master`
- **Rows:** 10
- **Size:** 0.02 MB
- **Columns:** `WSM_ID [int]`, `WSM_STATUS [varchar]`, `WSM_ACTIVE [int]`

### `waiver_types`
- **Rows:** 7
- **Size:** 0.02 MB
- **Columns:** `WT_ID [int]`, `WT_NAME [varchar]`, `WT_PRIORITY [int]`, `WT_ACTIVE [int]`

### `benf_claim_status_query`
- **Rows:** NULL
- **Size:** NULL MB
- **Columns:** `ci_intimation_id [int]`, `ci_service_no [int]`, `ci_card_id [int]`, `CI_ADMISSION_DATE [int]`, `ci_beneficiary_name [int]`, `CI_PATIENT_NAME [int]`, `CI_NONEMPANELLED_HOSPITAL [int]`, `cs_net_claim_amt [int]`, `cs_uti_sup_amt [int]`, `cs_uti_app_amt [int]`, `cs_sub_entity_id [int]`, `ci_int_stage [int]`, `ci_int_status [int]`, `Remark [int]`, `CurrentClaimStatus [int]`, `LastUpdDate [int]`, `cs_pat_amt [int]`, `cs_pat_disc_amt [int]`

### `bpa_recomm_view`
- **Rows:** NULL
- **Size:** NULL MB
- **Columns:** `Region [int]`, `Claim_Id [int]`, `BPA_Date [int]`, `SID [int]`, `Settle_Date [int]`, `Final_Settle_Date [int]`, `Claim_Amt [int]`, `App_Amt [int]`, `Prov_BPA_Fee [int]`, `Prov_Ser_Tax [int]`, `BPA_Fee [int]`, `Ser_Tax [int]`, `BPA_TDS [int]`, `BPA_Net [int]`, `Claim_Status [int]`

### `bpa_serfee_reco_view`
- **Rows:** NULL
- **Size:** NULL MB
- **Columns:** `Region [int]`, `SID [int]`, `Final_Settle_Date [int]`, `Claims [int]`, `BPA_Fee [int]`, `Ser_Tax [int]`, `BPA_TDS [int]`, `BPA_Net [int]`, `BPA_Recvd [int]`, `Credit_Date [int]`, `NEFT_Ref_No [int]`, `NEFT_Amount [int]`, `Voucher_No [int]`
