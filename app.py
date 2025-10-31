from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import secrets

app = Flask(__name__)
CORS(app)

DATA_FILE = 'api_keys.json'

@app.route('/')
def home():
    return render_template('index.html')

# ✅ Generate API key
@app.route('/api/generate_key', methods=['POST'])
def generate_key():
    api_key = secrets.token_hex(16)  # random 32-char key

    # Save the key locally
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                keys = json.load(f)
            except json.JSONDecodeError:
                keys = {}
    else:
        keys = {}

    keys[api_key] = {"email": "unknown", "usage": 0}
    with open(DATA_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

    return jsonify({"key": api_key})

# ✅ Optional: View saved keys (admin)
@app.route('/admin', methods=['GET'])
def admin_panel():
    if not os.path.exists(DATA_FILE):
        return jsonify({"message": "No keys found"})
    with open(DATA_FILE, 'r') as f:
        keys = json.load(f)
    return jsonify(keys)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))