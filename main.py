import base64
import pymupdf
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
        
    try:
        print("extract-pdf start",flush=1)
        pdf_bytes = request.data
        if not pdf_bytes or len(pdf_bytes) < 10:
            return jsonify({"success": False, "error": "Nu s-au primit date sau fisierul este gol"}), 400
        
        # Deschidem PDF-ul direct din memoria RAM (fără a scrie pe disc)
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        np = 0
        full_text = ""
        for page in doc:
            full_text += page.get_text()
            np=np+1
            print(f"nr page {np} {len(full_text)}",flush=1)
        doc.close()
        
        return jsonify({
            "success": True,
            "text": full_text.strip(),
            "pages": len(doc)
        })
    except Exception as e:
        if np == 0: 
            return jsonify({"success": False, "error": str(e)+",bytes:"+str(len(pdf_bytes))}), 500
        return jsonify({
            "success": True,
            "text": full_text.strip(),
            "pages": np
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

