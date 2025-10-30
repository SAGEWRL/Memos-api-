// ==========================
// 🔥 Firebase Configuration
// ==========================
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.3/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/10.12.3/firebase-firestore.js";

// Your Firebase credentials (replace with yours if needed)
const firebaseConfig = {
  apiKey: "AIzaSyB-fWDSWcJdDsitrQnjsglpFU3XQlwNqIU",
  authDomain: "memos-api.firebaseapp.com",
  projectId: "memos-api",
  storageBucket: "memos-api.firebasestorage.app",
  messagingSenderId: "48119548245",
  appId: "1:48119548245:web:23926bc573ff2fca48c7dc"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// ==========================
// ⚙️ Key Generator Function
// ==========================
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("generate-btn");
  const keyDisplay = document.getElementById("key-display");

  btn.addEventListener("click", async () => {
    keyDisplay.textContent = "Generating...";
    try {
      // Call your FastAPI backend to generate the key
      const res = await fetch("/api/generate_key", { method: "POST" });
      const data = await res.json();

      if (data.key) {
        keyDisplay.textContent = data.key;

        // Save the key to Firebase Firestore
        await addDoc(collection(db, "api_keys"), {
          key: data.key,
          created_at: new Date().toISOString()
        });

        console.log("✅ Key saved to Firebase:", data.key);
      } else {
        keyDisplay.textContent = "Error generating key.";
      }
    } catch (err) {
      console.error("Error:", err);
      keyDisplay.textContent = "Failed to connect.";
    }
  });
});