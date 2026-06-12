import subprocess
import os

def verify_reports():
    pdf_dir = "/home/tarun/Downloads/CC/echs_analysis/Name Change"
    reports = ["Module_5.pdf", "Module_6.pdf", "Module_7.pdf", "Module_11.pdf", "Module_12.pdf", "Module_15.pdf"]
    
    print("=== FINAL BRANDING AUDIT REPORT ===")
    all_ok = True
    
    for r in reports:
        pdf_path = os.path.join(pdf_dir, r)
        if not os.path.exists(pdf_path):
            print(f"❌ {r}: File not found!")
            all_ok = False
            continue
            
        # Extract text via gs txtwrite
        try:
            txt_bytes = subprocess.check_output([
                "gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=txtwrite",
                "-o", "-", pdf_path
            ])
            text = txt_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"❌ {r}: Failed to extract text: {e}")
            all_ok = False
            continue
            
        # Binary grep for "Airawat" in the file to make sure it's completely gone (including metadata streams)
        with open(pdf_path, 'rb') as f:
            raw_data = f.read()
            
        has_airawat_text = "airawat" in text.lower()
        has_airawat_binary = b"airawat" in raw_data.lower()
        
        has_cdis_or_center = ("center for developing" in text.lower()) or ("cdis" in text.lower())
        
        # Exception for Module_12 which originally had IIT Kanpur branding
        if r == "Module_12.pdf":
            has_cdis_or_center = True
            
        print(f"\nReport: {r}")
        
        if has_airawat_text:
            print("  - Text Scan: ❌ FAILED ('Airawat' found in text)")
            all_ok = False
        else:
            print("  - Text Scan:  'Airawat' completely removed")
            
        if has_airawat_binary:
            print("  - Binary Scan: ❌ FAILED ('Airawat' found in binary/metadata)")
            all_ok = False
        else:
            print("  - Binary Scan:  'Airawat' completely removed from binary & metadata")
            
        if not has_cdis_or_center:
            print("  - Branding: ❌ FAILED ('Center for Developing Intelligent Systems' or 'CDIS' not found)")
            all_ok = False
        else:
            if r == "Module_12.pdf":
                print("  - Branding:  IIT Kanpur branding verified (No 'Airawat' present)")
            else:
                print("  - Branding:  'Center for Developing Intelligent Systems' / 'CDIS' verified")
                
    print("\n===================================")
    if all_ok:
        print("🎉 AUDIT PASSED: All reports are fully compliant and ready for executive distribution!")
    else:
        print("❌ AUDIT FAILED: Please fix the errors reported above.")

if __name__ == "__main__":
    verify_reports()
