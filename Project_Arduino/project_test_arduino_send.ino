#include <SoftwareSerial.h>
#include <Adafruit_NeoPixel.h>

const int bluetoothTx = 2;  // TX pin of Bluetooth module connected to Arduino's RX pin
const int bluetoothRx = 3;  // RX pin of Bluetooth module connected to Arduino's TX pin

#define BUTTON1 4 
#define BUTTON2 5

#define PIN_LED_1      6  // Define the pin to which the data line is connected
#define PIN_LED_2      7  // Define the pin to which the data line is connected
#define NUMPIXELS      12  // Define the number of pixels in your strip

Adafruit_NeoPixel strip_1 = Adafruit_NeoPixel(NUMPIXELS, PIN_LED_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip_2 = Adafruit_NeoPixel(NUMPIXELS, PIN_LED_2, NEO_GRB + NEO_KHZ800);

SoftwareSerial bluetoothSerial(bluetoothTx, bluetoothRx);
bool firstRun = true;
bool menuPage = true;

int choice ;

uint32_t colors_1[] = {
  strip_1.Color(130, 0, 153),   // 
  strip_1.Color(255, 255, 255),   // 
  strip_1.Color(255, 0, 0),    // 
  strip_1.Color(0, 0, 255),   // 
  strip_1.Color(0, 255, 0),    // 
  strip_1.Color(0, 0, 0)    // 
};

uint32_t colors_2[] = {
  strip_2.Color(153, 0, 153),   // 
  strip_2.Color(255, 255, 255),   // 
  strip_2.Color(255, 0, 0),    // 
  strip_2.Color(0, 0, 255),   // 
  strip_2.Color(0, 255, 0),    // 
  strip_2.Color(0, 0, 0)    //
};

void setup() {
  Serial.begin(9600);
  bluetoothSerial.begin(9600);

  pinMode(BUTTON1, INPUT);
  pinMode(BUTTON2, INPUT);

  strip_1.begin();  // Initialize the strip
  strip_2.begin();  // Initialize the strip
  strip_1.setBrightness(100);  // Set brightness to 50 (adjust as needed)
  strip_2.setBrightness(100);  // Set brightness to 50 (adjust as needed)
  strip_1.show();   // Initialize all pixels to 'off'
  strip_2.show();   // Initialize all pixels to 'off'
}

void colorWipe_1(uint32_t color) {
  for(int pixelIndex = 0; pixelIndex < strip_1.numPixels(); pixelIndex++) {
    strip_1.setPixelColor(pixelIndex, color);
  }
  strip_1.show();
}

void colorWipe_2(uint32_t color) {
  for(int pixelIndex = 0; pixelIndex < strip_2.numPixels(); pixelIndex++) {
    strip_2.setPixelColor(pixelIndex, color);
  }
  strip_2.show();
}

void ClearRGB(){
  for(int pixelIndex = 0; pixelIndex < strip_1.numPixels(); pixelIndex++) {
    strip_1.setPixelColor(pixelIndex, 0);
  }
  for(int pixelIndex = 0; pixelIndex < strip_2.numPixels(); pixelIndex++) {
    strip_2.setPixelColor(pixelIndex, 0);
  }
  strip_1.show();
  strip_2.show();
}

void tutorial_page(){
  delay(200);
  Serial.println("Enter tutorial page");
  while(true){
    bool button1_pressed,button2_pressed;
    button1_pressed = digitalRead(BUTTON1) == LOW;
    button2_pressed = digitalRead(BUTTON2) == LOW;
    if(button1_pressed){
      bluetoothSerial.println("0");
      Serial.println("back");
      return;
    }
    if(button2_pressed){
      bluetoothSerial.println("1");
      Serial.println("next pic");
      delay(200);
    } 
    delay(100);
  }
}

void play_page(){
  delay(200);
  Serial.println("Enter play page");
  int count = 0;
  int state = 0;
  String choice1_str, choice2_str;
  int choice1, choice2;
  while(true){
    bool button1_pressed,button2_pressed;
    button1_pressed = digitalRead(BUTTON1) == LOW;
    button2_pressed = digitalRead(BUTTON2) == LOW;
    if(button1_pressed){
      bluetoothSerial.println("0");
      return;
    }
    if(button2_pressed){
      bluetoothSerial.println("1");
      Serial.println("start_play");
      while(true){
        String data = bluetoothSerial.readStringUntil('\n');
        data.trim(); // Remove leading and trailing spaces
        
        // Check if the received data is in the format of a list (e.g., "[x, y]")
        if (data.startsWith("[") && data.endsWith("]") && data.indexOf(",") > 0) {
          // Remove the brackets and split the string at the comma
          Serial.print("Received: ");
          Serial.println(data);
          data = data.substring(1, data.length() - 1); // Remove brackets
          int commaIndex = data.indexOf(",");
          choice1_str = data.substring(0, commaIndex);
          choice2_str = data.substring(commaIndex + 2); // +2 to skip the comma and space
      
          // Parse the extracted strings into integers
          choice1 = choice1_str.toInt();
          choice2 = choice2_str.toInt();
    
          Serial.print("Choice 1: ");
          Serial.println(choice1);
          Serial.print("Choice 2: ");
          Serial.println(choice2);
          colorWipe_1(colors_1[choice1]);
          colorWipe_2(colors_2[choice2]);
          state = 1;
          Serial.println("wait for ans....");
          while(state == 1){
            button1_pressed = digitalRead(BUTTON1) == LOW;
            button2_pressed = digitalRead(BUTTON2) == LOW;
            if (button1_pressed || button2_pressed) {
              ClearRGB();
              if (button1_pressed) {
                Serial.println(choice1_str);
                bluetoothSerial.println(choice1_str);
              }
              else if (button2_pressed) {
                Serial.println(choice2_str);
                bluetoothSerial.println(choice2_str);
              }
              state = 0;
              count += 1;
            }
            if(count == 15){
              ClearRGB();
              delay(10000);
              return;
            }
          } 
        }
      }
    } 
    delay(100);
  }
}

void loop() {
  bool button1_pressed,button2_pressed;
  while (firstRun) {
    delay(1000);
    Serial.println("Waiting for connection...");
    if (bluetoothSerial.available()) {
      String message = bluetoothSerial.readStringUntil('\n');
      if (message == "Start") {
        Serial.println("Connected to Raspberry Pi");
        bluetoothSerial.println("Connected");
        firstRun = false;
        delay(200);
        menuPage = true;
        choice = 0;
        return;
      }
    }
  }
  while(menuPage){
    button1_pressed = digitalRead(BUTTON1) == LOW;
    button2_pressed = digitalRead(BUTTON2) == LOW;
    colorWipe_1(colors_1[2]);
    colorWipe_2(colors_2[4]);
    if (button1_pressed) {
      choice++;
      delay(150);
      if (choice >= 3) {
        choice = 0;
      }
      bluetoothSerial.println("0"); // Sending the updated choice to the Bluetooth module
      Serial.println("choice " + String(choice));
    }

    if(button2_pressed){
      bluetoothSerial.println("1");
      Serial.println("submit");
      if(choice == 0){
        play_page();
        delay(250);
      }
      else if(choice == 1){
        tutorial_page();
        delay(250);
      }
      else if(choice == 2){
        Serial.println("exit");
        menuPage = false;
        firstRun = true;
        ClearRGB();
        delay(100);
      }
    }
    delay(150);
  }
}