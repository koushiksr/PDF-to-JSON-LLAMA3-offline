from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
import json
from pdfminer.high_level import extract_text

app = Flask(__name__)
llama = Ollama(model="llama3")

def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF file using pdfminer.six.
    """
    text = extract_text(pdf_path)
    return text

def extract_json(text):
    start_index = text.find("```") + 3
    end_index = text.rfind("```")
    return text[start_index:end_index].strip()

@app.route('/pd', methods=['POST'])
def process_pdf():
    try:
        if not request.files:
            return jsonify({"error": "No file uploaded"})
        pdf_file = request.files['pdf']
        if not pdf_file:
            return jsonify({"error": "No file uploaded"})
        pdf_path = 'pdf.pdf'

        pdf_file.save(pdf_path)
        pdf_data = extract_pdf_text(pdf_path)
        if not pdf_data:
            return jsonify({"error": "No text found in PDF"})
        prompt = pdf_data + " heres is my data i need all fields and values in json format"
        response = llama.invoke(prompt)
        if not response:
            return jsonify({"error": "No response from LLM"})
        json_result = extract_json(response)
        if not json_result:
            return jsonify({"error": "No JSON found in response"})
        parsed_json = json.loads(json_result)
        if not parsed_json:
            return jsonify({"error": "Invalid JSON"})
        a= jsonify(parsed_json)
        if not a:
            return jsonify({"error": "Invalid JSON"})
        return a
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
