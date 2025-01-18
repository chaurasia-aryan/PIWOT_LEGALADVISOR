from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  
from dotenv import load_dotenv
import base64
import io
import fitz  
import google.generativeai as genai
import os

def remove_asterisks(d):
    if isinstance(d, dict):
        return {k: remove_asterisks(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [remove_asterisks(i) for i in d]
    elif isinstance(d, str):
        return d.replace('*', '')
    else:
        return d

# Load environment variables from a .env file
load_dotenv()


app = Flask(__name__)


CORS(app)  


API_KEY = "AIzaSyDhdn1M1pUaJN9SYosF9HniF6ugtcV6Ff0"

# Configure the Generative AI model with the API key
genai.configure(api_key=API_KEY)

def get_gemini_response(input_text, pdf_content, prompt):
    try:
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return str(e)

def input_pdf_setup(uploaded_file):
    try:
        # Open the PDF file with PyMuPDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype='pdf')
        if pdf_document.page_count == 0:
            raise ValueError("No pages found in the PDF file")

        # Process the first page
        page = pdf_document.load_page(0)
        pix = page.get_pixmap()

        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        img_data = pix.tobytes(output='png')  
        img_byte_arr.write(img_data)
        img_byte_arr.seek(0)  
        img_data = img_byte_arr.getvalue()

        # Return base64 encoded image data
        pdf_parts = [
            {
                "mime_type": "image/png",
                "data": base64.b64encode(img_data).decode()  
        ]
        return pdf_parts
    except Exception as e:
        raise ValueError(f"Error processing PDF file: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        input_text = request.form['input_text']
        prompt = request.form['prompt']
        file = request.files.get('resume')

        if not input_text or not prompt:
            return jsonify({'error': 'Input text and prompt are required'}), 400

        if file and file.filename.lower().endswith('.pdf'):
            pdf_content = input_pdf_setup(file)
            response = get_gemini_response(input_text, pdf_content, prompt)
            response = remove_asterisks(response)
            return jsonify({'response': response})
        else:
            return jsonify({'error': 'Invalid file or no file uploaded'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
