from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # allows requests from your frontend (Render/static site)

# Path to JSON file that stores API keys
DATA_FILE = 'api_keys.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save-key', methods=['POST'])
def save_key():
    data = request.get_json(force=True)
    key_name = data.get('key_name')
    key_value = data.get('key_value')

    if not key_name or not key_value:
        return jsonify({'success': False, 'message': 'Missing key name or value!'}), 400

    # Load existing keys or create a new dict
    keys = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                keys = json.load(f)
        except json.JSONDecodeError:
            keys = {}

    # Add/update key
    keys[key_name] = key_value

    # Save
    with open(DATA_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

    return jsonify({'success': True, 'message': f'Key "{key_name}" saved successfully!'})

# ---- ADMIN PANEL (optional, safe placeholder) ----
@app.route('/admin', methods=['GET'])
def admin_panel():
    if not os.path.exists(DATA_FILE):
        return jsonify({'message': 'No keys found yet.'})
    with open(DATA_FILE, 'r') as f:
        keys = json.load(f)
    return jsonify({'saved_keys': keys})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))