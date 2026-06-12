import os
import subprocess

def test_11():
    input_pdf = "backup_original_pdfs/Module_11.pdf"
    uncompressed_pdf = "uncompressed_11.pdf"
    edited_pdf = "edited_11.pdf"
    output_pdf = "Module_11_modified.pdf"
    
    # 1. Decompress
    print("Decompressing...")
    subprocess.run([
        "gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
        "-dCompressPages=false", f"-sOutputFile={uncompressed_pdf}", input_pdf
    ], check=True)
    
    # 2. Read and replace
    with open(uncompressed_pdf, "rb") as f:
        data = f.read()
        
    old_seq = b'[(\x16)1(\x1e\\r\x0e\x1f\x0e\x0b)1(\x08)0.998264(\x01\x0c\x11\x0c\x0e\\r !\x08)-0.0145399(\x15)1("#\\n$\x0e\x0b)-0.0118273(\x1e)0.992839("\\n\x08)'
    new_seq = b'[(\x06\x0c\\n\x0b\x0c\\r\x08\x2f\x22\\r\x08\x07\x0c\x34\x0c\x0f\x22\x2e\x1e\\n\\)\x08\x05\\n\x0b\x0c\x0f\x0f\x1e\\)\x0c\\n\x0b\x08\x03\x13\x11\x0b\x0c\\(\x11\x08)'
    
    count = data.count(old_seq)
    print(f"Found {count} occurrences of target glyph sequence")
    
    if count > 0:
        data = data.replace(old_seq, new_seq)
        
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
    test_11()
