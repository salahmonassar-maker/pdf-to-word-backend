from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
from docx import Document
import pdfplumber

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "PDF to Word server is running"})

@app.route("/convert", methods=["POST"])
def convert_pdf_to_word():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    doc = Document()

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    doc.add_paragraph(line)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        file.filename.replace(".pdf", ".docx")
    )
    doc.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
