int x=0,c=0;
void setup() {
  // put your setup code here, to run once:
   //pinMode(ledPin, OUTPUT);  // initialize the LED pin as an output
  Serial.begin(57600);
//Serial.begin(9600);
 Serial.setTimeout(1);
 pinMode(3,OUTPUT);
 digitalWrite(3,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0);{
  x=Serial.read();
//x = Serial.readString().toInt();
if(x=='1'){
  c++;
  if(c>10){
digitalWrite(3,HIGH);
delay(1000);
c=0;
}
else{
 
  digitalWrite(3,LOW);
 
  }

}
else if(x=='0'){

digitalWrite(3,LOW);
  c=0;
}

}
}
