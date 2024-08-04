# FLASK APP - Run the app using flask --app app.py run
import os, sys
from flask import Flask, request, render_template
from pypdf import PdfReader 
import json
from resumeparser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def ats():
    doc = request.files['pdf_doc']
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    data = _read_file_from_path(doc_path)
    json_string = ats_extractor(data)

    if json_string.startswith('```json'):
        json_string = json_string[7:]
    if json_string.endswith('```'):
        json_string = json_string[:-3]
    json_string = json_string.strip()

    json_file_path = os.path.join(UPLOAD_PATH, "cleaned_data.json")
    with open(json_file_path, 'w') as json_file:
        json_file.write(json_string)

    try:
        data_dict = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return render_template('error.html', error="Invalid JSON data")

    return render_template('index.html', data=data_dict)
 
def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no] 
        data += page.extract_text()

    return data 


if __name__ == "__main__":
    app.run(port=8000, debug=True)

