async function fetchCards() {
  const res = await fetch("/api/cards");
  const cards = await res.json();
  const tbody = document.getElementById("cardTable");
  tbody.innerHTML = "";

  for (const uid in cards) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${uid}</td><td>${cards[uid]}</td>`;
    tbody.appendChild(tr);
  }
}

// Handle top-up form
document.getElementById("topupBtn").addEventListener("click", async () => {
  const uid = document.getElementById("uidInput").value.trim();
  const amount = parseInt(document.getElementById("amountInput").value);

  if (!uid || isNaN(amount)) {
    alert("Please enter valid UID and amount");
    return;
  }

  const res = await fetch("/api/topup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ uid, amount })
  });

  const data = await res.json();
  if (res.ok) {
    alert(`Top-up successful! New balance: ${data.newBalance}`);
    fetchCards(); // refresh table
  } else {
    alert(`Error: ${data.error}`);
  }
});

// Refresh table every second
setInterval(fetchCards, 1000);
fetchCards();
