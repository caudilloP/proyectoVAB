int ledV = 3;
int ledR = 5;
int motor = 6;
int fototrancistor = A0;
int color ;
int valorFototrancistor = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ledV, OUTPUT);
  pinMode(ledR, OUTPUT);
  pinMode(motor, OUTPUT);
}

void loop() {
valorFototrancistor = analogRead(fototrancistor);
if(valorFototrancistor > 900){
  digitalWrite(motor, HIGH);
  }
else{
  digitalWrite(motor, LOW);
/*
 *Cuando se interrumpa la señal del sensor infrarojo, 
 *la banda se detendrá y se deberia enviar una 'a' 
 *a traves del puerto serie a Spyder para que haga la 
 *captura de la imagen y su tratamiento. Si la imagen
 *tratada tiene color verde, se envia una 'v' a traves
 *del puerto serial de Spyder a Arduino para que se 
 *encienda el led verde, y de la misma manera sucedera,
 *si la imagen contiene color rojo, se enviara una 'r'
 *para encender el led rojo. Los leds son simplemente
 *una referencia visual, en lugar de los leds se usara
 *un servo que sera el actuador que hara el cambio de 
 *direccion de las fichas
 */
  //Serial.write('a');
  if (Serial.available() > 0){
    color = Serial.read();
    if(color == 'v'){
      digitalWrite(ledV, HIGH);
      delay(1000);
      digitalWrite(ledV, LOW);
      delay(1000);
      }
      if(color == 'r'){
      digitalWrite(ledR, HIGH);
      delay(1000);
      digitalWrite(ledR, LOW);
      delay(1000);
      }  
    }  
  }
}   
