from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"  # Change this to something strong & private

DATA_FILE = 'api_keys.json'
USERS_FILE = 'users.json'

# 🔹 Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"  # Change this before deployment

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

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            keys = json.load(f)
    else:
        keys = {}

    keys[key_name] = key_value

    with open(DATA_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

    return jsonify({'success': True, 'message': f'Key \"{key_name}\" saved successfully!'})

# 🔐 Admin login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# 🚪 Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# 🧠 Admin dashboard (protected)
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            keys = json.load(f)
    else:
        keys = {}

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {}

    return render_template('admin.html', keys=keys, users=users)

if __name__ == '__main__':
    app.run(debug=True)