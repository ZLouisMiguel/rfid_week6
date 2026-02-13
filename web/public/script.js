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

// Refresh every second
setInterval(fetchCards, 1000);
fetchCards();
