def calculate_risk(duplicate_status, passport_status):
    score = 0

    if duplicate_status == "EXACT_DUPLICATE":
        score += 50
    elif duplicate_status == "POSSIBLE_DUPLICATE":
        score += 30

    if passport_status == "MISMATCH":
        score += 30
    elif passport_status == "NOT_FOUND":
        score += 40

    if score >= 70:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"