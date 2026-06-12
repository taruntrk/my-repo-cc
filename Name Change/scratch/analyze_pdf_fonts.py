import re
import zlib

def parse_cmap(cmap_text):
    glyph_to_char = {}
    # Find all beginbfrange ... endbfrange
    ranges = re.findall(r'(\d+)\s+beginbfrange\s*(.*?)\s*endbfrange', cmap_text, re.DOTALL)
    for num, range_text in ranges:
        for line in range_text.strip().split('\n'):
            parts = line.strip().split()
            if len(parts) == 3:
                # Format: <start> <end> <dest>
                start = int(parts[0].strip('<>'), 16)
                end = int(parts[1].strip('<>'), 16)
                dest = parts[2].strip('<>')
                # If dest is a string
                if len(dest) == 4:
                    dest_val = int(dest, 16)
                    for val in range(start, end + 1):
                        glyph_to_char[val] = chr(dest_val + (val - start))
                elif len(dest) > 4:
                    # Multi-character mapping
                    dest_str = "".join(chr(int(dest[i:i+4], 16)) for i in range(0, len(dest), 4))
                    for val in range(start, end + 1):
                        glyph_to_char[val] = dest_str
            elif len(parts) == 2:
                # Single mapping inside a range
                pass
                
    # Find all beginbfchar ... endbfchar
    chars = re.findall(r'(\d+)\s+beginbfchar\s*(.*?)\s*endbfchar', cmap_text, re.DOTALL)
    for num, char_text in chars:
        for line in char_text.strip().split('\n'):
            parts = line.strip().split()
            if len(parts) == 2:
                glyph = int(parts[0].strip('<>'), 16)
                dest = parts[1].strip('<>')
                dest_str = "".join(chr(int(dest[i:i+4], 16)) for i in range(0, len(dest), 4))
                glyph_to_char[glyph] = dest_str
                
    return glyph_to_char

def analyze_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        content = f.read()
        
    # Find all fonts and ToUnicode objects
    cmaps = {}
    font_to_cmap = {}
    
    # Simple regex to find /ToUnicode references
    font_matches = re.finditer(r'(\d+)\s+\d+\s+obj\s*<<.*?/ToUnicode\s+(\d+)\s+\d+\s+R', content.decode('utf-8', errors='ignore'))
    for m in font_matches:
        font_id = int(m.group(1))
        cmap_id = int(m.group(2))
        font_to_cmap[font_id] = cmap_id
        
    # Extract CMap contents
    cmap_objs = re.findall(rb'(\d+)\s+\d+\s+obj\s*<<.*?>>\s*stream\s*(.*?)\s*endstream', content, re.DOTALL)
    for cid_str, stream_data in cmap_objs:
        cid = int(cid_str)
        # Check if this object is a ToUnicode CMap
        obj_header_start = content.rfind(f"{cid} 0 obj".encode(), 0, content.find(stream_data))
        obj_header = content[obj_header_start:obj_header_start+200]
        
        # Decompress if FlateDecode
        if b'FlateDecode' in obj_header:
            try:
                decompressed = zlib.decompress(stream_data.strip(b'\r\n'))
            except Exception:
                try:
                    decompressed = zlib.decompress(stream_data)
                except Exception:
                    continue
        else:
            decompressed = stream_data
            
        cmap_text = decompressed.decode('utf-8', errors='ignore')
        if "begincmap" in cmap_text:
            cmaps[cid] = parse_cmap(cmap_text)
            
    # Now scan all content streams
    print("Scanning streams...")
    stream_matches = re.finditer(rb'stream\s*(.*?)\s*endstream', content, re.DOTALL)
    for i, m in enumerate(stream_matches):
        stream_data = m.group(1)
        # Check if FlateDecode
        obj_header_start = content.rfind(b'obj', 0, m.start())
        obj_header = content[obj_header_start-50:obj_header_start+100]
        if b'FlateDecode' in obj_header:
            try:
                decompressed = zlib.decompress(stream_data.strip(b'\r\n'))
            except Exception:
                try:
                    decompressed = zlib.decompress(stream_data)
                except Exception:
                    continue
        else:
            decompressed = stream_data
            
        # Search for text drawing operations like Tj or TJ
        # We need to find font settings like /F1 12 Tf or /R11 12 Tf
        current_font = None
        
        # Let's tokenise the stream to find Tj and TJ
        # We'll do a simple scan
        operators = re.split(r'(\s+)', decompressed.decode('utf-8', errors='ignore'))
        
        # Or look for any TJ/Tj lines
        lines = decompressed.split(b'\n')
        for line_num, line in enumerate(lines):
            # Check if this line changes font
            font_change = re.search(rb'/(\w+)\s+\d+(\.\d+)?\s+Tf', line)
            if font_change:
                current_font = font_change.group(1).decode('utf-8')
                
            # If line has TJ or Tj
            if b'Tj' in line or b'TJ' in line:
                # Find all text parts in the line
                # Hex strings like <00010002>
                hex_parts = re.findall(rb'<([0-9a-fA-F]+)>', line)
                decoded_str = ""
                for hp in hex_parts:
                    # Decode hex using all available CMaps to see which one works
                    for cid, cmap in cmaps.items():
                        try:
                            s = ""
                            for j in range(0, len(hp), 4):
                                glyph = int(hp[j:j+4], 16)
                                s += cmap.get(glyph, '?')
                            if "airawat" in s.lower() or "echs" in s.lower():
                                print(f"Stream {i}, Line {line_num}: Font {current_font}, CMap {cid} -> Decoded: '{s}'")
                                print(f"  Raw: {line.decode('utf-8', errors='ignore')}")
                        except Exception:
                            pass

if __name__ == "__main__":
    analyze_pdf("uncompressed_Module_15.pdf")
