/*
pulseCount

Use pulseIn() function to measure pulse widths
and count pulses per unit time
6-Jan-2024 J.Beale
*/

const uint8_t inPin = 3;  // pulse input pin
int ledState = LOW;

unsigned long pTimeout = 20000000;  // 20 seconds, expect at least one pulse in that time
unsigned long tNow, tLast, tPrior;  // microseconds this pulse, previous pulse, previous interval
unsigned long tInterval = 60000000;  // microseconds in time interval (60s for counts-per-minute)
unsigned long count=0;
unsigned long intervalCount = 0;  // how many time intervals have elapsed so far
unsigned long pSum = 0;  // sum of pulse-length microseconds in this interval

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(inPin, INPUT);
  Serial.begin(115200);
  delay(2000);
  Serial.println("index, count, avg_us");
  Serial.println("# Pulse Length 0.1 JPB");
  tPrior = micros();
}

// the loop function runs over and over again forever
void loop() {
  unsigned long pTime = pulseIn(inPin, HIGH, pTimeout);
  pSum += pTime;
  tNow = micros();
  count += 1;
  if ((count % 10 )== 0) {
    ledState = !ledState;
    digitalWrite(LED_BUILTIN, ledState);  // toggle the LED every N pulses
  }
  if ((tNow - tPrior) > tInterval) {  // have exceeded the measurement time interval?
    intervalCount += 1;
    tPrior += tInterval;   // allow for any overage past nominal, for next time
    float pAvg = (float) pSum / count;
    Serial.print(intervalCount);
    Serial.print(",");
    Serial.print(count);
    Serial.print(",");
    Serial.print(pAvg,3);
    Serial.println();
    pSum = 0;
    count = 0;  // reset count of pulses in this interval
  }
}
