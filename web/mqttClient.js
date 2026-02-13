const mqtt = require("mqtt");
const cardService = require("./services/cardService");

// MQTT broker URL
const MQTT_BROKER = "mqtt://broker.benax.rw";
const TOPIC_STATUS = "rfid/y2c_team0125/card/status";
const TOPIC_TOPUP = "rfid/y2c_team0125/card/topup";
const TOPIC_BALANCE = "rfid/y2c_team0125/card/balance";

// Connect to MQTT
const client = mqtt.connect(MQTT_BROKER);

client.on("connect", () => {
  console.log("Connected to MQTT broker");
  client.subscribe([TOPIC_STATUS, TOPIC_BALANCE], (err) => {
    if (err) console.error("MQTT subscribe error:", err);
  });
});

// Handle incoming messages
client.on("message", (topic, message) => {
  const payload = JSON.parse(message.toString());

  if (topic === TOPIC_STATUS) {
    cardService.updateCard(payload.uid, payload.balance);
    console.log(`Card detected: ${payload.uid}, Balance: ${payload.balance}`);
  }

  if (topic === TOPIC_BALANCE) {
    cardService.updateCard(payload.uid, payload.new_balance);
    console.log(`Balance updated: ${payload.uid} → ${payload.new_balance}`);
  }
});

// Publish topup command to ESP
function sendTopup(uid, amount) {
  const payload = { uid, amount };
  client.publish(TOPIC_TOPUP, JSON.stringify(payload));
}

module.exports = { client, sendTopup };
