const API_URL = "http://127.0.0.1:8000"; // FastAPI server URL

// Handle Add Fruit Form
document.getElementById("fruitForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fruitData = {
    fruit_id: document.getElementById("fruit_id").value,
    location: document.getElementById("location").value,
    status: document.getElementById("status").value
  };

  const response = await fetch(`${API_URL}/add_fruit/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(fruitData)
  });

  const data = await response.json();
  alert(data.message);
});

// Fetch Fruit History
async function getFruitHistory() {
  const fruitId = document.getElementById("historyFruitId").value;
  const response = await fetch(`${API_URL}/get_fruit_history/${fruitId}`);
  const data = await response.json();
  document.getElementById("historyResult").textContent = JSON.stringify(data, null, 2);
}

// Fetch Full Blockchain
async function getChain() {
  const response = await fetch(`${API_URL}/get_chain/`);
  const data = await response.json();
  document.getElementById("chainResult").textContent = JSON.stringify(data, null, 2);
}
