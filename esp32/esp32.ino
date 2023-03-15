// Servo
//#include "ESP32_ISR_Servo.h"
#include <pwmWrite.h>
#define PIN_X 23
#define PIN_Y 19

// BME280
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <vector>
using namespace std;
#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BME280 bme;

// OLED
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_FeatherOLED.h>

// Accel
#include <Adafruit_MPU6050.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>


// Wi-Fi
#include <Arduino.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <string>
#include <HTTPClient.h>
#define USE_SERIAL Serial


// GPS
#include <TinyGPSPlus.h>


// C++ functions
#include <bits/stdc++.h>
#include <vector>
#include <algorithm>


#define PIN_D3            3         // Pin D3 mapped to pin GPIO3/RX0 of ESP32
#define PIN_D4            4         // Pin D4 mapped to pin GPIO4/ADC10/TOUCH0 of ESP32

//int servoIndex1 = -1;
//int servoIndex2 = -1;
Pwm pwm = Pwm();

// vector<vector<double>> a;

Adafruit_FeatherOLED oled = Adafruit_FeatherOLED();
Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

WiFiMulti wifiMulti;

vector<vector<double>> dev_data;
// 1 - dev_id; 2 - dev_type; 3 - dev_value

vector<double> joystick_data;

vector<float> sensor_data;

TinyGPSPlus gps;

void setup() {
	Serial.begin(115200);
  Serial2.begin(9600);
  
  // Servo
  //delay(1000);
	//ESP32_ISR_Servos.setupServo(32);
  //delay(1000);

  // BME280
	if (!bme.begin(0x76)) {
		Serial.println("Could not find a valid BME280 sensor, check wiring!");
		while (1);
	}

  // OLED
  oled.init();
  oled.setBatteryVisible(true);

  // Wi-fi
  if (!mpu.begin()) {
    Serial.println("Sensor init failed");
    while (1)
      yield();
  }

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();

    for(uint8_t t = 4; t > 0; t--) {
        USE_SERIAL.printf("[SETUP] WAIT %d...\n", t);
        USE_SERIAL.flush();
        delay(1000);
    }

    wifiMulti.addAP("Mi 11", "askristal");

  // Digital - BOOL
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(27, OUTPUT);
}

void loop() {
	Serial.print("Temperature = ");
	Serial.print(bme.readTemperature());
	Serial.println("*C");

  vector<double> res = {bme.readTemperature(),bme.readPressure() / 100.0F, bme.readAltitude(SEALEVELPRESSURE_HPA), bme.readHumidity()};
  // a.push_back(res);

	Serial.println();
	delay(100);

  show_battery();
  delay(100);

  update_web();

  change_relay();
  
  // servo_f(90,90);
  set_joystick();

  show_gps();

  update_all_data();
}


vector<float> get_GPS(){
  vector<float> res;
  if (gps.location.isValid()){
    res.push_back(gps.location.lat());
    res.push_back(gps.location.lng());
  }  
  else
  {
    Serial.print(F("INVALID"));
  }
  return res;
}


void update_all_data(){
  vector<float> data_gps = get_GPS();
  vector<float> data_bme = {bme.readTemperature(),bme.readPressure() / 100.0F, bme.readAltitude(SEALEVELPRESSURE_HPA), bme.readHumidity()};
  // ACCELEROMETR
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  vector<float> data_accel = {a.acceleration.x, a.acceleration.y, a.acceleration.z};
  // wait for WiFi connection
    if((wifiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        USE_SERIAL.print("[HTTP] begin...\n" + String(data_gps[0]));

        http.begin("http://kristaldev.online:8092/functions/sensors/set_all/" + String(2) + "/" + String(data_gps[0], 6) + "/" + String(data_gps[1], 6) + 
                   "/" + String(data_accel[0]) + "/" + String(data_accel[1]) + "/" + String(data_accel[2]) + "/" +
                    String(data_bme[0]) + "/" + String(data_bme[1]) + "/" + String(data_bme[2]) + "/" + String(data_bme[3])); //HTTP

        USE_SERIAL.print("[HTTP] GET...\n");
        int httpCode = http.GET();

        http.end();
    }

    delay(500);
}

void show_gps(){
  while (Serial2.available() > 0)
    if (gps.encode(Serial2.read()))
      displayInfo();
  if (millis() > 1000 && gps.charsProcessed() < 10)
  {
    Serial.println(F("No GPS detected: check wiring."));
    while (true);
  }
}


void show_battery(){
  // clear the current count
  oled.clearDisplay();

  // get the current voltage of the battery
  float battery = oled.getBatteryVoltage();

  // update the battery icon
  oled.setBattery(battery);
  oled.renderBattery();


  // TEMPERATURE
  oled.print("T: ");
  oled.print(bme.readTemperature());

  oled.print("  P: ");
  oled.print(bme.readPressure() / 100.0F);

  oled.print("  H: ");
  oled.print(bme.readHumidity());


  // ACCELEROMETR
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  
  oled.print(" x:");
  oled.println(a.acceleration.x, 1);
  oled.print("y: ");
  oled.print(a.acceleration.y, 1);
  oled.print(" z: ");
  oled.print(a.acceleration.z, 1);
  oled.println("");

  oled.display();
}


void create_data(vector<String> vect){
  // dev_data.pop_back();
  // dev_data.erase(dev_data.begin()+dev_data.size());
  int dev_number = int(vect.size()/6);
  for (int i = 0; i < dev_number; i++){
    if (dev_data.size() < dev_number){
      vector<double> res;
      res.push_back(vect[1+7*i].toInt());
      res.push_back(vect[3+7*i].toInt());
      res.push_back(vect[5+7*i].toInt());
      dev_data.push_back(res);
    }
    else{
      vector<double> res;
      res.push_back(vect[1+7*i].toInt());
      res.push_back(vect[3+7*i].toInt());
      res.push_back(vect[5+7*i].toInt());
      dev_data[i] = res;      
    }      
  }
}

void create_data_joystick(vector<String> vect){
  // dev_data.pop_back();
  // dev_data.erase(dev_data.begin()+dev_data.size());
  int dev_number = int(vect.size());
  for (int i = 0; i < dev_number; i++){
    joystick_data.push_back(vect[i].toInt());
  }
}


void show_data(){
  for (int i = 0; i < dev_data.size(); i++){
    USE_SERIAL.print("device: ");
    USE_SERIAL.print(dev_data[i][0]);
    USE_SERIAL.print(" ");
    USE_SERIAL.print(dev_data[i][1]);
    USE_SERIAL.print(" ");
    USE_SERIAL.println(dev_data[i][2]);
  }
}


void update_web(){
      // wait for WiFi connection
    if((wifiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        USE_SERIAL.print("[HTTP] begin...\n");
        // configure traged server and url
        //http.begin("https://www.howsmyssl.com/a/check", ca); //HTTPS
        http.begin("http://kristaldev.online:8092/get_page/get_values/2"); //HTTP

        USE_SERIAL.print("[HTTP] GET...\n");
        // start connection and send HTTP header
        int httpCode = http.GET();

        // httpCode will be negative on error
        if(httpCode > 0) {
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);
            if(httpCode == HTTP_CODE_OK) {
                String d_data = http.getString();
                // USE_SERIAL.println(d_data);
                vector<String> res;
                int j = 0;
                for (int i = 0; i < d_data.length(); i++){
                  if ((d_data.charAt(i) == ' ') or (d_data.charAt(i) == '\n')){
                    res.push_back(d_data.substring(j, i));
                    j = i;
                  }
                }
                create_data(res);
                show_data();
            }
        } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }

        http.end();
    }

    delay(500);
}


void change_relay(){
  digitalWrite(13, int(dev_data[0][2]));
  digitalWrite(12, int(dev_data[1][2]));
  digitalWrite(14, int(dev_data[2][2]));
  digitalWrite(27, int(dev_data[3][2]));
  delay(100);
}


void set_joystick(){
        // wait for WiFi connection
    if((wifiMulti.run() == WL_CONNECTED)) {

        HTTPClient http;

        USE_SERIAL.print("[HTTP] begin...\n");
        // configure traged server and url
        //http.begin("https://www.howsmyssl.com/a/check", ca); //HTTPS
        http.begin("http://kristaldev.online:8092/functions/joystick/get/2"); //HTTP

        USE_SERIAL.print("[HTTP] GET...\n");
        // start connection and send HTTP header
        int httpCode = http.GET();

        // httpCode will be negative on error
        if(httpCode > 0) {
            USE_SERIAL.printf("[HTTP] GET... code: %d\n", httpCode);
            if(httpCode == HTTP_CODE_OK) {
                String d_data = http.getString();
                // USE_SERIAL.println(d_data);
                vector<String> res;
                Serial.println(d_data);
                int j = 0;
                for (int i = 0; i < d_data.length(); i++){
                  if ((d_data.charAt(i) == ' ') or (d_data.charAt(i) == '\n')){
                    res.push_back(d_data.substring(j, i));
                    j = i;
                  }
                }
                create_data_joystick(res);
                servo_f(res[1].toInt(),res[2].toInt());
                Serial.print(joystick_data[1]);
                Serial.print(" ");
                Serial.println(joystick_data[2]);
            }
        } else {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        }
        http.end();
    }
    delay(50);
}


void servo_f(int x, int y){
  int joystick_x = min(180,x);
  int joystick_y = min(180,y);
  pwm.writeServo(PIN_X, joystick_x);
  pwm.writeServo(PIN_Y, joystick_y);
  delay(50);
}


void displayInfo(){
  Serial.print(F("Location: "));
  if (gps.location.isValid()){
    Serial.print("Lat: ");
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print("Lng: ");
    Serial.print(gps.location.lng(), 6);
    Serial.println();
  }  
  else
  {
    Serial.print(F("INVALID"));
  }
}

