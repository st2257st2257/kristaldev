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


// C++ functions
#include <bits/stdc++.h>
#include <vector>

vector<vector<double>> a;

Adafruit_FeatherOLED oled = Adafruit_FeatherOLED();
Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

WiFiMulti wifiMulti;

vector<vector<double>> dev_data;
// 1 - dev_id; 2 - dev_type; 3 - dev_value

void setup() {
	Serial.begin(115200);

	if (!bme.begin(0x76)) {
		Serial.println("Could not find a valid BME280 sensor, check wiring!");
		while (1);
	}

  oled.init();
  oled.setBatteryVisible(true);

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
  a.push_back(res);

	Serial.println();
	delay(1000);

  show_battery();
  delay(1000);

  update_web();

  change_relay();
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
        http.begin("http://kristaldev.online:8090/get_page/get_values/2"); //HTTP

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

    delay(2000);
}


void change_relay(){
  digitalWrite(13, int(dev_data[0][2]));
  digitalWrite(12, int(dev_data[1][2]));
  digitalWrite(14, int(dev_data[2][2]));
  digitalWrite(27, int(dev_data[3][2]));
  delay(100);
}
