#define GREEN 9
#define BLUE 10
#define RED 11

int redValue;
int greenValue;
int blueValue;

void setup(){
  Serial.begin(115200);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  digitalWrite(RED, HIGH);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
}

void loop(){
  #define delayTime 1
  String input = Serial.readString();
  Serial.println(input);
  sscanf(input.c_str(), "%3d %3d %3d", &redValue, &greenValue, &blueValue);
  Serial.println(redValue);
  Serial.println(greenValue);
  Serial.println(blueValue);
  analogWrite(RED, redValue);
  analogWrite(BLUE, blueValue);
  analogWrite(GREEN, greenValue);

  delay(delayTime);
}

