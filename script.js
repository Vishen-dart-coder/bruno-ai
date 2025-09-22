// === Keys ===
const OPENAI_API_KEY = "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"; // required
const GOOGLE_API_KEY = "AIzaSyA_xhJ1bhJGkOSTMtuSD-t0UDXhUyvg7iE"; // required for Search
const GOOGLE_CSE_ID = "87a4b08375d5a4841";// required for Search

const form = document.getElementById("searchForm");
const input = document.getElementById("q");
const resultsEl = document.getElementById("results");

function getMode() {
  const checked = document.querySelector('input[name="mode"]:checked');
  return checked ? checked.value : "ai";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if (!q) return;
  input.value = "";
  resultsEl.innerHTML = `<p>Loading...</p>`;

  const mode = getMode();
  if (mode === "ai") {
    // === OpenAI Mode ===
    try {
      const res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          model: "gpt-4o-mini",
          messages: [{ role: "user", content: q }],
          temperature: 0.2
        })
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error.message);
      const answer = data.choices?.[0]?.message?.content || "No answer.";
      resultsEl.innerHTML = `<div class="ai-answer">${answer.replace(/\n/g,"<br>")}</div>`;
    } catch (err) {
      resultsEl.innerHTML = `<p style="color:red;">AI Error: ${err.message}</p>`;
    }
  } else {
    // === Google Mode ===
    const url = new URL("https://www.googleapis.com/customsearch/v1");
    url.searchParams.set("key", GOOGLE_API_KEY);
    url.searchParams.set("cx", GOOGLE_CSE_ID);
    url.searchParams.set("q", q);
    try {
      const res = await fetch(url);
      const data = await res.json();
      if (!data.items) throw new Error("No results");
      resultsEl.innerHTML = data.items.map(it =>
        `<div class="result">
          <a href="${it.link}" target="_blank">${it.title}</a>
          <p>${it.snippet}</p>
        </div>`).join("");
    } catch (err) {
      resultsEl.innerHTML = `<p style="color:red;">Search Error: ${err.message}</p>`;
    }
  }
});
