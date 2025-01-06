from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# A simple function to dynamically extract key-value pairs
def extract_data(text):
    # Try to identify key-value pairs based on common delimiters like ':' or '-'
    pattern = r"(\w[\w\s]*):?\s?([a-zA-Z0-9\s]+)"
    matches = re.findall(pattern, text)
    
    # Return as a dictionary of key-value pairs
    data = {match[0].strip(): match[1].strip() for match in matches}
    return data

@app.route('/convert', methods=['POST'])
def convert_to_excel():
    data = request.get_json()
    message_data = data.get('data', '')

    if not message_data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Extract key-value pairs from the message
    extracted_data = extract_data(message_data)

    if not extracted_data:
        return jsonify({'error': 'No valid data found'}), 400

    # Convert extracted data to a DataFrame (for Excel)
    df = pd.DataFrame([extracted_data])
    
    # Save to Excel
    file_name = 'dynamic_employee_data.xlsx'
    df.to_excel(file_name, index=False)
    
    return jsonify({'success': True, 'file': file_name})

if __name__ == "__main__":
    app.run(debug=True)
