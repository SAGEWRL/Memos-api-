from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the file where we’ll save API keys
DATA_FILE = 'api_keys.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-key', methods=['POST'])
def save_key():
    data = request.json
    key_name = data.get('key_name')
    key_value = data.get('key_value')

    if not key_name or not key_value:
        return jsonify({'success': False, 'message': 'Missing key name or value!'})

    # Read existing keys
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            keys = json.load(f)
    else:
        keys = {}

    # Add or update key
    keys[key_name] = key_value

    # Save back to file
    with open(DATA_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

    return jsonify({'success': True, 'message': f'Key "{key_name}" saved successfully!'})

if __name__ == '__main__':
    app.run(debug=True)