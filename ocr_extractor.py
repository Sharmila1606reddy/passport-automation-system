import easyocr
import re

reader = easyocr.Reader(['en'])

def extract_passport_data(image_path):
    result = reader.readtext(image_path, detail=0)
    text = " ".join(result)
    text_lower = text.lower()
    text_no_spaces = "".join(result).replace(" ", "")

    name = "Unknown"
    dob = "0000-00-00"
    id_number = "P9999"

    # 🔹 Extract from MRZ Line 1 (Name)
    # P<AAA SURNAME<<GIVEN<NAMES
    mrz1_match = re.search(r'P<([A-Z<]{3})([A-Z<]+)', text_no_spaces, re.IGNORECASE)
    if mrz1_match:
        name_part = mrz1_match.group(2)
        # Replace `<` with space and clean up
        name = name_part.replace('<', ' ').strip()
        name = re.sub(r'\s+', ' ', name)

    # 🔹 Extract from MRZ Line 2 (ID and DOB)
    # [ID 9 chars] [CheckDigit] [Nationality 3 chars] [DOB YYMMDD]
    mrz2_match = re.search(r'([A-Z0-9]{8,9})<?\d[A-Z<]{3}(\d{6})', text_no_spaces, re.IGNORECASE)
    if mrz2_match:
        id_number = mrz2_match.group(1).replace('<', '').upper()
        dob_raw = mrz2_match.group(2)
        try:
            yy = int(dob_raw[:2])
            year = 1900 + yy if yy > 30 else 2000 + yy
            dob = f"{year:04d}-{dob_raw[2:4]}-{dob_raw[4:6]}"
        except ValueError:
            pass

    # 🔹 Fallbacks if MRZ is not fully found
    if name == "Unknown":
        words = text.split()
        name = " ".join(words[:2]) if len(words) >= 2 else "Unknown"
        
    if id_number == "P9999":
        id_match_old = re.search(r'p\d{4}', text_lower)
        if id_match_old:
            id_number = id_match_old.group().upper()

    if dob == "0000-00-00":
        dob_match = re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', text)
        if dob_match:
            dob = dob_match.group()

    return {
        "name": name,
        "dob": dob,
        "id": id_number
    }