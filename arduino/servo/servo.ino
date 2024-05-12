#include <Servo.h> // подключаем библиотеку для работы с сервоприводом

int incomingByte = 0;            // Received data byte
String inputString = "";         // Used to store received content
boolean newLineReceived = false; // Previous data end flag
boolean startBit  = false;       //Acceptance Agreement Start Sign
int num_reveice = 0;
String received_DATA = "";

Servo servoX;
Servo servoY;

String motor;
int angle;

void setup() {
  Serial.begin(115200);
  servoX.attach(10); // привязываем сервопривод к аналоговому выходу 10
  servoY.attach(11); // привязываем сервопривод к аналоговому выходу 11
}

void loop() {
  readSerial(); 
}

void readSerial() {
  while (Serial.available())
  {
    incomingByte = Serial.read();              //One byte by byte, the next sentence is read into a string array to form a completed packet
    if (incomingByte == '%') {
      num_reveice = 0;
      startBit = true;
    }
    if (startBit == true) {
      num_reveice++;
      inputString += (char) incomingByte;
    }
    if (startBit == true && incomingByte == '#') {
      newLineReceived = true;
      startBit = false;
    }
    if (newLineReceived) {
      received_DATA = inputString.substring(1, (inputString.length() - 1));
      Serial.println(received_DATA);
      inputString = "";   // clear the string
      newLineReceived = false;
      on_receive();
    }
  }
}

void on_receive(){
  motor = received_DATA.substring(0,1);
  angle = received_DATA.substring(1,received_DATA.length()).toInt();

  if (motor == "X"){
    servoX.write(angle);
  }
  if (motor == "Y"){
    servoY.write(angle);
  }
}