// Measure pulse widths from gamma scintillator
// using Teensy 4.1
// 7-Jan-2024 J.Beale


#include <FreqMeasureMulti.h>

FreqMeasureMulti freq1;
#define MEASURE_PIN 5
#define MEASURE_TYPE FREQMEASUREMULTI_MARK_ONLY

void setup() {
  Serial.begin(115200);
  while (!Serial) ; // wait for Arduino Serial Monitor
  delay(10);
  Serial.println("# Pulse width measure 0.1  JPB 7-Jan-2024");
  freq1.begin(MEASURE_PIN, MEASURE_TYPE);
  do {} while (!freq1.available());  // wait for first read
  freq1.read();  // throw it away, first one is junk

}

void loop() {
  uint32_t pulses = freq1.available();  // returns # captures in buffer
  for (uint8_t i = 0; i < pulses; i++) {
    uint32_t t = freq1.read();
    if (t > 0x80000000) {
      t = 0xffffffff - t;
    }
    Serial.println(t);
  }
}
