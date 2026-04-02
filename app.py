from flask import Flask, render_template, request, send_from_directory
import os

# Import your modules
from duplicate_check import check_duplicate
from passport_verification import verify_passport
from risk_analysis import calculate_risk
from decision_engine import final_decision
from ocr_extractor import extract_passport_data

app = Flask(__name__)

# Folder to store uploaded passport images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔹 Route to Serve Uploaded Images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# 🔹 Home Page
@app.route("/")
def home():
    return render_template("index.html")


# 🔹 Verification Route (Scanner Simulation)
@app.route("/verify", methods=["POST"])
def verify():
    # Check if file is uploaded
    if "passport" not in request.files:
        return "No file uploaded ❌"

    file = request.files["passport"]

    if file.filename == "":
        return "No file selected ❌"

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 🔹 STEP 1: OCR Extraction (LIVE)
    data = extract_passport_data(filepath)

    name = data.get("name", "Unknown")
    dob = data.get("dob", "0000-00-00")
    id_number = data.get("id", "P9999")

    print("Extracted Data:", data)  # Debugging

    # 🔹 STEP 2: Duplicate Detection
    duplicate_status = check_duplicate(name, dob, id_number)

    # 🔹 STEP 3: Passport Verification (DB match)
    passport_status = verify_passport(data)

    # 🔹 STEP 4: Risk Analysis
    risk = calculate_risk(duplicate_status, passport_status)

    # 🔹 STEP 5: Final Decision
    decision = final_decision(risk, passport_status)

    # 🔹 Return results to UI
    return render_template(
        "index.html",
        result={
            "name": name,
            "dob": dob,
            "id": id_number,
            "duplicate": duplicate_status,
            "passport": passport_status,
            "risk": risk,
            "decision": decision,
            "image_filename": file.filename
        }
    )


# 🔹 Run App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)