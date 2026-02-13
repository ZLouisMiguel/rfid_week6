#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>

// ---------------- WIFI ----------------
#define WIFI_SSID "Miguel"
#define WIFI_PASS "123456789"

// ---------------- MQTT ----------------
#define MQTT_HOST "broker.benax.rw"
#define MQTT_PORT 1883

#define TEAM_ID "y2c_team0125"

#define TOPIC_STATUS   "rfid/y2c_team0125/card/status"
#define TOPIC_TOPUP    "rfid/y2c_team0125/card/topup"
#define TOPIC_BALANCE  "rfid/y2c_team0125/card/balance"

// ---------------- RFID ----------------
#define SS_PIN 2   // D4 on NodeMCU
#define RST_PIN 0  // D3 on NodeMCU

MFRC522 rfid(SS_PIN, RST_PIN);

// ---------------- LED (optional) ----------------
#define LED_PIN 2  // NodeMCU onboard LED

// ---------------- GLOBALS ----------------
WiFiClient espClient;
PubSubClient client(espClient);

String lastUID = "";
int balance = 0;

// ---------------- WIFI ----------------
void connectWiFi() {
  Serial.print("Connecting WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

// ---------------- MQTT CALLBACK ----------------
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++)
    message += (char)payload[i];

  StaticJsonDocument<200> doc;
  deserializeJson(doc, message);

  String uid = doc["uid"];
  int amount = doc["amount"];

  if (uid == lastUID) {
    balance += amount;

    StaticJsonDocument<200> out;
    out["uid"] = uid;
    out["new_balance"] = balance;

    char buffer[256];
    serializeJson(out, buffer);

    client.publish(TOPIC_BALANCE, buffer);
    Serial.println("Balance updated via topup");
  }
}

// ---------------- MQTT ----------------
void connectMQTT() {
  client.setServer(MQTT_HOST, MQTT_PORT);
  client.setCallback(mqttCallback);

  while (!client.connected()) {
    Serial.print("Connecting MQTT...");
    if (client.connect("rfid_device_y2c_team0125")) {
      Serial.println("connected");
      client.subscribe(TOPIC_TOPUP);
    } else {
      Serial.println("retry...");
      delay(2000);
    }
  }
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  SPI.begin();
  rfid.PCD_Init();

  Serial.println("Initializing...");
  connectWiFi();
  connectMQTT();

  Serial.println("RFID Reader Ready! Place a card near the reader.");
}

// ---------------- LOOP ----------------
void loop() {
  if (!client.connected())
    connectMQTT();

  client.loop();

  // Check for card presence
  if (rfid.PICC_IsNewCardPresent()) {
    if (rfid.PICC_ReadCardSerial()) {
      String uid = "";
      for (byte i = 0; i < rfid.uid.size; i++) {
        if (rfid.uid.uidByte[i] < 0x10) uid += "0";
        uid += String(rfid.uid.uidByte[i], HEX);
      }
      uid.toUpperCase();
      lastUID = uid;

      // Publish card status
      StaticJsonDocument<200> doc;
      doc["uid"] = uid;
      doc["balance"] = balance;
      char buffer[256];
      serializeJson(doc, buffer);
      client.publish(TOPIC_STATUS, buffer);

      // Indicate card read
      Serial.print("Card detected: ");
      Serial.println(uid);
      digitalWrite(LED_PIN, HIGH);
      delay(500);
      digitalWrite(LED_PIN, LOW);
    }
  } else {
    Serial.println("Waiting for card...");
    delay(1000);  // slow down printing
  }
}
