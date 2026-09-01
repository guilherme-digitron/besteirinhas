#include <Wire.h>

#define MPU6050_ADDR 0x68

int16_t ax, ay, az;
int16_t gx, gy, gz;

const int AX_OFFSET = 1311;
const int AY_OFFSET = -16133;
const int AZ_OFFSET = 2737;

const int GX_OFFSET = 59;
const int GY_OFFSET = -53;
const int GZ_OFFSET = -109;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Acorda o MPU6050
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission(true);

  delay(1000);

  Serial.println("================================");
  Serial.println("TESTE DE MOVIMENTO");
  Serial.println("================================");
  Serial.println("Formato:");
  Serial.println("AX AY AZ | GX GY GZ");
  Serial.println();
}

void loop() {

  lerMPU();

  // Aplica os offsets
  int axCorrigido = ax - AX_OFFSET;
  int ayCorrigido = ay - AY_OFFSET;
  int azCorrigido = az - AZ_OFFSET;

  int gxCorrigido = gx - GX_OFFSET;
  int gyCorrigido = gy - GY_OFFSET;
  int gzCorrigido = gz - GZ_OFFSET;

  Serial.print(axCorrigido);
  Serial.print(" ");
  Serial.print(ayCorrigido);
  Serial.print(" ");
  Serial.print(azCorrigido);

  Serial.print(" | ");

  Serial.print(gxCorrigido);
  Serial.print(" ");
  Serial.print(gyCorrigido);
  Serial.print(" ");
  Serial.println(gzCorrigido);

  delay(50);
}

void lerMPU() {

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);

  Wire.requestFrom(MPU6050_ADDR, 14, true);

  ax = Wire.read() << 8 | Wire.read();
  ay = Wire.read() << 8 | Wire.read();
  az = Wire.read() << 8 | Wire.read();

  // Temperatura
  Wire.read();
  Wire.read();

  gx = Wire.read() << 8 | Wire.read();
  gy = Wire.read() << 8 | Wire.read();
  gz = Wire.read() << 8 | Wire.read();
}
