from flask import Flask, request, send_file
from pdf2docx import Converter
import pytesseract
from pdf2image import convert_from_path
from docx import Document

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    pdf = request.files["file"]
    pdf.save("input.pdf")

    try:
        cv = Converter("input.pdf")
        cv.convert("output.docx")
        cv.close()
    except:
        images = convert_from_path("input.pdf", dpi=300)
        doc = Document()
        for img in images:
            text = pytesseract.image_to_string(img, lang="ara+eng")
            doc.add_paragraph(text)
        doc.save("output.docx")

    return send_file("output.docx", as_attachment=True)

if __name__ == "__main__":
    app.run()
