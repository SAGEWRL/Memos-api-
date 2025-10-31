const baseURL = "https://memos-api-ahnh.onrender.com"; // Your backend URL

document.getElementById("generateBtn").addEventListener("click", async () => {
  const status = document.getElementById("status");
  const keyBox = document.getElementById("keyBox");
  const newKey = document.getElementById("newKey");
  const timestamp = document.getElementById("timestamp");

  status.textContent = "Generating key...";
  keyBox.classList.add("hidden");

  try {
    const res = await fetch(${baseURL}/api/generate_key, {
      method: "POST",
    });
    const data = await res.json();

    if (data.key) {
      newKey.textContent = data.key;
      keyBox.classList.remove("hidden");
      status.textContent = "✅ Key generated successfully!";
      timestamp.textContent = `Generated at: ${new Date().toLocaleString()}`;
    } else {
      status.textContent = "⚠️ Failed to generate key.";
    }
  } catch (err) {
    console.error(err);
    status.textContent = "❌ Error connecting to server.";
  }
});

document.getElementById("copyBtn").addEventListener("click", () => {
  const keyText = document.getElementById("newKey").textContent;
  navigator.clipboard.writeText(keyText);
  alert("✅ Key copied to clipboard!");
});