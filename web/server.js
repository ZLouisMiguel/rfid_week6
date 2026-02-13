const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");
const cardService = require("./services/cardService");
const mqttClient = require("./mqttClient");

const app = express();
const PORT = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

// Route: Get all cards and balances
app.get("/api/cards", (req, res) => {
  res.json(cardService.getCards());
});

// Route: Topup a card
app.post("/api/topup", (req, res) => {
  const { uid, amount } = req.body;
  if (!uid || !amount) return res.status(400).json({ error: "uid and amount required" });

  const newBalance = cardService.topupCard(uid, amount);
  mqttClient.sendTopup(uid, amount);
  res.json({ uid, newBalance });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
