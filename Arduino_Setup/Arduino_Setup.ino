void setup() {
  // put your setup code here, to run once:
  // 12 direction
  // 3 PWM
  pinMode(12, OUTPUT);
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  // char *test;
  String test;
  while(Serial.available() > 0){
    test = Serial.readString();
    Serial.println(test);
  }
  
  Serial.print("123123");
  //Serial.println
  
  digitalWrite(12, HIGH);
  //digitalWrite(9, LOW);
  analogWrite(3, 123);
  delay(3000);
  digitalWrite(12, LOW);
  //digitalWrite(9, LOW);
  analogWrite(3, 123);
  delay(3000);
  digitalWrite(3,0);
  delay(1000);
  // exit(0);
}

