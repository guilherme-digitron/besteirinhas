#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <WiFiManager.h> // Biblioteca do Portal de Configuração

const int udpPort = 12345;
WiFiUDP udp;
bool wifiConectado = false;
Adafruit_MPU6050 mpu;

float zero_X = 0;
float zero_Y = 0;

void calibrar() {
  float soma_x = 0, soma_y = 0;
  for(int i = 0; i < 30; i++) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    soma_x += a.acceleration.x;
    soma_y += a.acceleration.y;
    delay(20);
  }
  zero_X = soma_x / 30.0;
  zero_Y = soma_y / 30.0;
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!mpu.begin()) {
    while (1) { delay(10); }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // --- GERENCIADOR DE WI-FI ---
  WiFiManager wm;
  
  // Define o tempo limite de busca do Wi-Fi antes de ligar apenas no cabo (30 seg)
  wm.setConfigPortalTimeout(30);

  // Tenta conectar no último Wi-Fi conhecido.
  // Se não encontrar, cria o Ponto de Acesso "MouseCabeca-Config"
  bool res = wm.autoConnect("MouseCabeca-Config");

  if (res) {
    wifiConectado = true;
    udp.begin(udpPort);
    Serial.println("Wi-Fi Conectado!");
  } else {
    Serial.println("Modo sem Wi-Fi (Operando apenas no Cabo USB).");
  }

  delay(500);
  calibrar();
}

void loop() {
  // Recalibração via Serial (Cabo)
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'R' || cmd == 'r') calibrar();
  }

  // Recalibração via Wi-Fi (UDP)
  if (wifiConectado) {
    int packetSize = udp.parsePacket();
    if (packetSize) {
      char buffer[10];
      int len = udp.read(buffer, 10);
      if (len > 0 && (buffer[0] == 'R' || buffer[0] == 'r')) calibrar();
    }
  }

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float inclinacao_X = a.acceleration.x - zero_X;
  float inclinacao_Y = a.acceleration.y - zero_Y;

  int vx = 0, vy = 0;
  float limite_zona_morta = 0.8;

  if (abs(inclinacao_X) > limite_zona_morta) vx = (int)(inclinacao_X * -5.0);
  if (abs(inclinacao_Y) > limite_zona_morta) vy = (int)(inclinacao_Y * -5.0);

  if (vx != 0 || vy != 0) {
    String payload = String(vx) + "," + String(vy);

    // 1. Envia via Cabo USB
    Serial.println(payload);

    // 2. Envia via Wi-Fi em Broadcast (sem precisar saber o IP do PC)
    if (wifiConectado) {
      udp.beginPacket(IPAddress(255, 255, 255, 255), udpPort);
      udp.print(payload);
      udp.endPacket();
    }
  }

  delay(20); 
}
