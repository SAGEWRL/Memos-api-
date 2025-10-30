// ===== Firebase Setup =====
const firebaseConfig = {
  apiKey: "AIzaSyB-fWDSWcJdDsitrQnjsglpFU3XQlwNqIU",
  authDomain: "memos-api.firebaseapp.com",
  projectId: "memos-api",
  storageBucket: "memos-api.firebasestorage.app",
  messagingSenderId: "48119548245",
  appId: "1:48119548245:web:23926bc573ff2fca48c7dc"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

let currentUser = null;

// ===== Auth Section =====
async function signUp() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  try {
    await auth.createUserWithEmailAndPassword(email, password);
    alert("✅ Account created successfully!");
  } catch (err) {
    alert("⚠️ " + err.message);
  }
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  try {
    await auth.signInWithEmailAndPassword(email, password);
    alert("✅ Logged in successfully!");
  } catch (err) {
    alert("⚠️ " + err.message);
  }
}

function logout() {
  auth.signOut();
  alert("👋 Logged out!");
}

auth.onAuthStateChanged(user => {
  currentUser = user;
  document.getElementById("auth-status").innerText = user
    ? `Logged in as ${user.email}`
    : "Not logged in";
});

// ===== API Key Generation =====
async function generateKey() {
  if (!currentUser) {
    alert("⚠️ Please log in first.");
    return;
  }

  const res = await fetch("/api/generate_key", {
    method: "POST",
  });

  const data = await res.json();
  const keyDisplay = document.getElementById("key-display");
  keyDisplay.innerHTML = `
    🔑 <b>Your new API Key:</b><br>
    <code>${data.key}</code>
    <br><br>
    <button onclick="copyKey('${data.key}')">Copy Key</button>
  `;
}

function copyKey(key) {
  navigator.clipboard.writeText(key);
  alert("📋 Key copied to clipboard!");
}