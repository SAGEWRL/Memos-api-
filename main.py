from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore
import secrets

app = Flask(__name__)
CORS(app)

# ---- Initialize Firebase ----
cred = credentials.Certificate("serviceAccountKey.json")  # your Firebase key
firebase_admin.initialize_app(cred)
db = firestore.client()


# ---- Home Page ----
@app.route('/')
def home():
    return render_template("index.html")


# ---- Signup ----
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = auth.create_user(email=email, password=password)

        db.collection("users").document(user.uid).set({
            "email": email,
            "api_key": None
        })
        return jsonify({"message": "User created successfully!", "uid": user.uid})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---- Login ----
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        users_ref = db.collection("users").where("email", "==", email).get()
        if not users_ref:
            return jsonify({"error": "User not found"}), 404

        # Firebase Admin doesn’t verify passwords directly — handled by frontend SDK
        return jsonify({"message": "Login simulated for demo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---- Generate API Key ----
@app.route('/generate-key', methods=['POST'])
def generate_key():
    try:
        data = request.get_json()
        email = data['email']

        users_ref = db.collection("users").where("email", "==", email).get()
        if not users_ref:
            return jsonify({"error": "User not found"}), 404

        user_doc = users_ref[0]
        new_key = secrets.token_hex(16)
        db.collection("users").document(user_doc.id).update({"api_key": new_key})
        return jsonify({"key": new_key})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ---- Admin Dashboard ----
@app.route('/admin')
def admin():
    try:
        users = db.collection("users").get()
        data = []
        for user in users:
            user_data = user.to_dict()
            data.append({
                "email": user_data.get("email"),
                "api_key": user_data.get("api_key")
            })
        return render_template("admin.html", users=data)
    except Exception as e:
        return f"Error loading admin dashboard: {e}", 500


# ---- Run App ----
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)