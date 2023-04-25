#include <BH1750.h>
#include <ShiftPWM.h>   // include ShiftPWM.h after setting the pins!
#include <Wire.h>
#define delayTime 1

 BH1750 lightMeter;
const int sensorPin = A0; //定义SR501人体红外的引脚
const int ledPinB = 9;    //定义LED灯的引脚
const int ledPinG = 10;    //定义LED灯的引脚
const int ledPinR = 11;    //定义LED灯的引脚
int sensorValue = 0;      //声明传感器数据变量
const int threshold = 30; // 光照度阈值，单位为lx，根据需要调整

// You can choose the latch pin yourself.
const int ShiftPWM_latchPin=8;


// If your LED's turn on if the pin is low, set this to true, otherwise set it to false.
const bool ShiftPWM_invertOutputs = false;

// You can enable the option below to shift the PWM phase of each shift register by 8 compared to the previous.
// This will slightly increase the interrupt load, but will prevent all PWM signals from becoming high at the same time.
// This will be a bit easier on your power supply, because the current peaks are distributed.
const bool ShiftPWM_balanceLoad = false;



// Here you set the number of brightness levels, the update frequency and the number of shift registers.
// These values affect the load of ShiftPWM.
// Choose them wisely and use the PrintInterruptLoad() function to verify your load.
unsigned char maxBrightness = 255;
unsigned char pwmFrequency = 75;
unsigned int numRegisters = 6;
unsigned int numOutputs = numRegisters*8;
unsigned int numRGBLeds = numRegisters*8/3;
unsigned int fadingMode = 0; //start with all LED's off.

unsigned long startTime = 0; // start time for the chosen fading mode

int redValue;
int greenValue;
int blueValue;

void printInfos(int R, int G, int B, int sensorValue, uint16_t lux);

void setup(){
  while(!Serial){
    delay(100);
  }
  Serial.begin(115200);
  Wire.begin();
  lightMeter.begin();
  pinMode(sensorPin, INPUT);

  // Sets the number of 8-bit registers that are used.
  ShiftPWM.SetAmountOfRegisters(numRegisters);

  // SetPinGrouping allows flexibility in LED setup.
  // If your LED's are connected like this: RRRRGGGGBBBBRRRRGGGGBBBB, use SetPinGrouping(4).
  ShiftPWM.SetPinGrouping(1); //This is the default, but I added here to demonstrate how to use the funtion

  ShiftPWM.Start(pwmFrequency,maxBrightness);
}

void loop()
{
  bool isGetFace = false;
  String input = Serial.readString();
  sensorValue = analogRead(sensorPin);   //读取传感器数据
  uint16_t lux = lightMeter.readLightLevel();

  sscanf(input.c_str(), "%3d %3d %3d", &redValue, &greenValue, &blueValue);

  if (redValue != 0 || greenValue != 0 || blueValue != 0) {
    isGetFace = true;
  }

  if(sensorValue > 800 && lux < threshold) {
    for(unsigned int led=0; led<numRGBLeds; led++){
      ShiftPWM.SetRGB(led,255,255,255);
    }
  }

  if (isGetFace) {
    for(unsigned int led=0; led<numRGBLeds; led++){
      ShiftPWM.SetRGB(led,redValue,greenValue,blueValue);
    }
  }

  while (Serial.read() >= 0){
      ; // flush remaining characters
  }

  printInfos(redValue, greenValue, blueValue, sensorValue, lux);
  delay(delayTime);
}

void printInfos(int R, int G, int B, int sensorValue, uint16_t lux) {
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.print(" lx");
  Serial.print("  sensorValue: ");
  Serial.print(sensorValue);
  Serial.print("  current RGB: ");
  Serial.print(R);
  Serial.print(G);
  Serial.println(B);
}