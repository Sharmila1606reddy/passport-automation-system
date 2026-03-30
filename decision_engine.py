def final_decision(risk, passport_status):
    if passport_status == "NOT_FOUND":
        return "REJECTED"

    if risk == "HIGH":
        return "REJECTED"
    elif risk == "MEDIUM":
        return "MANUAL REVIEW"
    else:
        return "APPROVED"