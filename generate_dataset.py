import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('dataset', exist_ok=True)

try:
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 40)
    font_large = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 32)
    font_mrz = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 36)
except IOError:
    font_title = ImageFont.load_default()
    font_large = ImageFont.load_default()
    font_mrz = ImageFont.load_default()

passports = [
    # 1. REAL (Valid in DB)
    {
        "filename": "1_real_alex",
        "id": "Z12345678",
        "name_printed": "Alex Johnson",
        "dob_printed": "1990-05-15",
        "country": "USA",
        "mrz1": "P<USAJOHNSON<<ALEX<<<<<<<<<<<<<<<<<<<<<<<<<<",
        "mrz2": "Z12345678<0USA9005152M2501016<<<<<<<<<<<<<<0"
    },
    # 2. REAL / DUPLICATE (Valid in DB, but has scanned already)
    {
        "filename": "2_real_duplicate_maria",
        "id": "A98765432",
        "name_printed": "Maria Garcia",
        "dob_printed": "1985-11-20",
        "country": "ESP",
        "mrz1": "P<ESPGARCIA<<MARIA<<<<<<<<<<<<<<<<<<<<<<<<<<",
        "mrz2": "A98765432<2ESP8511204F2801016<<<<<<<<<<<<<<0"
    },
    # 3. SYNTHETIC (Not in DB -> Rejected/Not Found)
    {
        "filename": "3_synthetic_not_in_db",
        "id": "B55544433",
        "name_printed": "Wei Chen",
        "dob_printed": "1992-08-08",
        "country": "CHN",
        "mrz1": "P<CHNCHEN<<WEI<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",
        "mrz2": "B55544433<5CHN9208081M3001016<<<<<<<<<<<<<<0"
    },
    # 4. FAKE / FORGED (MRZ Name does not match printed Name -> Mismatch)
    {
        "filename": "4_fake_name_mismatch",
        "id": "X99887766",
        "name_printed": "James Smith", 
        "dob_printed": "1978-02-14",
        "country": "GBR",
        # MRZ says HACKER<<JOHN (forged)
        "mrz1": "P<GBRHACKER<<JOHN<<<<<<<<<<<<<<<<<<<<<<<<<<<",
        "mrz2": "X99887766<1GBR7802146M2901016<<<<<<<<<<<<<<0"
    }
]

for p in passports:
    img = Image.new('RGB', (1000, 650), color=(240, 248, 255))
    d = ImageDraw.Draw(img)
    
    # Draw headers
    d.rectangle([0, 0, 1000, 80], fill=(15, 23, 42))
    d.text((400, 20), "PASSPORT", fill=(255,255,255), font=font_title)
    
    # Draw photo placeholder
    d.rectangle([50, 120, 280, 420], fill=(200, 200, 200), outline=(50,50,50), width=2)
    d.text((100, 250), "[PHOTO]", fill=(100,100,100), font=font_large)
    
    # Draw Text Data
    parts = p['name_printed'].split()
    surname = parts[-1]
    given = " ".join(parts[:-1])
    d.text((320, 130), f"Surname: {surname}", fill=(0,0,0), font=font_large)
    d.text((320, 190), f"Given Names: {given}", fill=(0,0,0), font=font_large)
    d.text((320, 250), f"Passport No: {p['id']}", fill=(0,0,0), font=font_title)
    d.text((320, 310), f"Nationality: {p['country']}", fill=(0,0,0), font=font_large)
    d.text((320, 370), f"Date of Birth: {p['dob_printed']}", fill=(0,0,0), font=font_large)
    
    # Background for MRZ
    d.rectangle([0, 480, 1000, 650], fill=(255, 255, 255))
    d.text((30, 510), p["mrz1"], fill=(0,0,0), font=font_mrz)
    d.text((30, 570), p["mrz2"], fill=(0,0,0), font=font_mrz)
    
    img.save(f"dataset/{p['filename']}.png")

print("Dataset generation complete.")
