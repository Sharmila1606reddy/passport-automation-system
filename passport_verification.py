import json
from Levenshtein import ratio
from datetime import datetime

def parse_date(date_str):
    if not date_str:
        return None
    # Handle both common database and OCR date formats
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    return None

def load_passport_db():
    with open("data/passport_db.json", "r") as f:
        return json.load(f)

def verify_passport(form_data):
    db = load_passport_db()
    
    form_dob = parse_date(form_data.get("dob", ""))
    form_id = form_data.get("id", "").upper()
    form_name = form_data.get("name", "").lower()

    for record in db:
        if record["id"].upper() == form_id:
            record_dob = parse_date(record.get("dob", ""))
            
            # Fuzzy string match for name (allow minor OCR errors, e.g. 70% threshold)
            name_similarity = ratio(record["name"].lower(), form_name)
            
            # Date must match exactly if both are parsed, OR handle missing dates gracefully
            dob_match = (form_dob == record_dob) if (form_dob and record_dob) else True
            
            if name_similarity > 0.7 and dob_match:
                return "VALID"
            else:
                return "MISMATCH"

    return "NOT_FOUND"