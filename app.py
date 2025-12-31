from flask import Flask, request, send_file
from pdf2docx import Converter

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    pdf = request.files["file"]
    pdf.save("input.pdf")

    cv = Converter("input.pdf")
    cv.convert("output.docx")
    cv.close()

    return send_file("output.docx", as_attachment=True)

if __name__ == "__main__":
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
