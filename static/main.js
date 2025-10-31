document.getElementById("keyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;

  const res = await fetch("/generate_key", {
    method: "POST",
    body: new URLSearchParams({ email }),
  });

  const data = await res.json();
  const div = document.getElementById("keyResult");

  if (data.success) {
    div.innerHTML = `<div class="alert alert-success">Your key: <b>${data.key}</b></div>`;
  } else {
    div.innerHTML = `<div class="alert alert-danger">Error: ${data.error || "Failed to generate key"}</div>`;
  }
});

document.getElementById("analyzeForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("text").value;

  const res = await fetch("/analyze_text", {
    method: "POST",
    body: new URLSearchParams({ text }),
  });

  const data = await res.json();
  const div = document.getElementById("analysisResult");

  div.innerHTML = `<div class="alert alert-info">Mood: <b>${data.mood}</b> (Score: ${data.score.toFixed(2)})</div>`;
});