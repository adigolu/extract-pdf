import base64
import fitz  # PyMuPDF
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    data = request.get_json()
    if not data or 'pdf_base64' not in data:
        return jsonify({"success": False, "error": "Lipseste fisierul PDF (pdf_base64)"}), 400
        
    try:
        pdf_base64_string = data['pdf_base64']
        # Decodificăm fișierul din formatul Base64 primit de la Make
        pdf_bytes = base64.b64decode(pdf_base64_string)
        
        # Deschidem PDF-ul direct din memoria RAM (fără a scrie pe disc)
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        
        return jsonify({
            "success": True,
            "text": full_text.strip(),
            "pages": len(doc)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

