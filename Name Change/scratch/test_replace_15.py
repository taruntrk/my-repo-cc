import os
import subprocess

def test_15():
    input_pdf = "backup_original_pdfs/Module_15.pdf"
    uncompressed_pdf = "uncompressed_15.pdf"
    edited_pdf = "edited_15.pdf"
    output_pdf = "Module_15_modified.pdf"
    
    # 1. Decompress
    print("Decompressing...")
    subprocess.run([
        "gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
        "-dCompressPages=false", f"-sOutputFile={uncompressed_pdf}", input_pdf
    ], check=True)
    
    # 2. Read and replace
    with open(uncompressed_pdf, "rb") as f:
        data = f.read()
        
    old_seq = b'[(\x00&)19.009(\x00$)-0.991385(\x00\\)\x004)-36.0142(\x00\x0e)3.00642(\x00\"\x00J\x00S)-5.00139(\x00B)7.00509(\x00X)7.99386(\x00B)2.01067(\x00U\x00\x01\x003\x00F)-3.01165(\x00T\x00F)-4.99268(\x00B\x00S\x00D)2.01067(\x00I\x00\x01\x00\')14.0137(\x00P\x00V\x00O\x00E)-2.00195(\x00B)2.01067(\x00U)0.997489(\x00J\x00P\x00O)]TJ'
    new_seq = b'[(\x00&\x00$\x00\\)\x004\x00\x0e\x00$\x00F\x00O\x00U\x00F\x00S\x00\x01\x00G\x00P\x00S\x00\x01\x00%\x00F\x00W\x00F\x00M\x00P\x00Q\x00J\x00O\x00H\x00\x01\x00*\x00O\x00U\x00F\x00M\x00M\x00J\x00H\x00F\x00O\x00U\x00\x01\x004\x00Z\x00T\x00U\x00F\x00N\x00T)]TJ'
    
    count = data.count(old_seq)
    print(f"Found {count} occurrences of target glyph sequence")
    
    if count > 0:
        data = data.replace(old_seq, new_seq)
        
    # Also replace in the title metadata (which is ASCII)
    old_title = b'/Title(ECHS-Airawat Research Foundation)'
    new_title = b'/Title(ECHS-Center for Developing Intelligent Systems)'
    title_count = data.count(old_title)
    print(f"Found {title_count} occurrences of title metadata")
    if title_count > 0:
        data = data.replace(old_title, new_title)
        
    with open(edited_pdf, "wb") as f:
        f.write(data)
        
    # 3. Compress and repair
    print("Re-compressing...")
    subprocess.run([
        "gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
        f"-sOutputFile={output_pdf}", edited_pdf
    ], check=True)
    
    # 4. Verify text
    print("Verifying text with txtwrite...")
    txt_out = subprocess.check_output([
        "gs", "-sDEVICE=txtwrite", "-o", "-", output_pdf
    ])
    
    if b"Airawat" in txt_out:
        print("❌ FAILED: 'Airawat' still in text!")
    else:
        print("✅ SUCCESS: 'Airawat' is gone!")
        
    if b"Center for Developing Intelligent Systems" in txt_out:
        print("✅ SUCCESS: 'Center for Developing Intelligent Systems' is present!")
    else:
        print("❌ FAILED: 'Center for Developing Intelligent Systems' is NOT present!")
        print("Extracted text sample:")
        print(txt_out[:1000].decode('utf-8', errors='ignore'))

if __name__ == "__main__":
    test_15()
