// ✅ Firebase setup
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import { 
  getAuth, createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, signOut 
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";
import { 
  getFirestore, collection, addDoc, serverTimestamp 
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-firestore.js";

// 🧩 Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyB-fWDSWcJdDsitrQnjsglpFU3XQlwNqIU",
  authDomain: "memos-api.firebaseapp.com",
  projectId: "memos-api",
  storageBucket: "memos-api.firebasestorage.app",
  messagingSenderId: "48119548245",
  appId: "1:48119548245:web:23926bc573ff2fca48c7dc"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// 🧠 Sign Up
window.signUp = async function() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  try {
    await createUserWithEmailAndPassword(auth, email, password);
    document.getElementById("auth-status").innerText = "✅ Account created & logged in!";
  } catch (err) {
    document.getElementById("auth-status").innerText = "❌ " + err.message;
  }
};

// 🔐 Login
window.login = async function() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  try {
    await signInWithEmailAndPassword(auth, email, password);
    document.getElementById("auth-status").innerText = "✅ Logged in!";
  } catch (err) {
    document.getElementById("auth-status").innerText = "❌ " + err.message;
  }
};

// 🚪 Logout
window.logout = async function() {
  await signOut(auth);
  document.getElementById("auth-status").innerText = "👋 Logged out.";
};

// 🔑 Generate API key & save to Firestore + backend
window.generateKey = async function() {
  const user = auth.currentUser;
  if (!user) {
    alert("Please log in first!");
    return;
  }

  try {
    // Replace with your live Render URL if hosted
    const res = await fetch("/api/generate_key", { method: "POST" });
    const data = await res.json();

    const keyDisplay = document.getElementById("key-display");
    keyDisplay.innerHTML = `
      🆕 Your key: <b>${data.key}</b>
      <button id="copyKey">Copy</button>
    `;

    // Copy functionality
    document.getElementById("copyKey").onclick = () => {
      navigator.clipboard.writeText(data.key);
      alert("✅ Key copied to clipboard!");
    };

    // Save in Firestore
    await addDoc(collection(db, "api_keys"), {
      email: user.email,
      key: data.key,
      createdAt: serverTimestamp(),
      usageCount: 0
    });

  } catch (e) {
    console.error("Error generating key:", e);
    alert("⚠️ Error generating key. Check console.");
  }
};