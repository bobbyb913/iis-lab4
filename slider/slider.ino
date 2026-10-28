#define PIN_1 14
#define PIN_2 13

int sensorReadings[2] = { 0, 0 };

//time keeping
unsigned long currentTime = 0;
unsigned long prevPressedTimes[2] = { 0, 0 };

//touch sensing
int touchThresholds[2] = { 1350, 1230 };
int minReadings[2] = { 1100, 1030 };
int maxReadings[2] = { touchThresholds[0] - 5, touchThresholds[1] - 5 };

bool isTouched[2] = { 0, 0 };
bool prevIsTouched[2] = { 0, 0 };

bool isReleased[2] = { 0, 0 };



//position tracking
int yPos[2] = { 0, 0 };

void setup() {
  //initialize Serial
  Serial.begin(9600);

  pinMode(PIN_1, INPUT);
  pinMode(PIN_2, INPUT);
}

void loop() {
  //log old vals
  prevIsTouched[0] = isTouched[0];
  prevIsTouched[1] = isTouched[1];

  //read sensors
  sensorReadings[0] = touchRead(PIN_1);
  sensorReadings[1] = touchRead(PIN_2);

  //detect touch
  detectTouch();
  detectRelease();
  detectYPos();

  //print vals
  for (int i = 0; i < 2; i++) {
    Serial.print(isTouched[i]);
    if (i < 2 - 1) {
      Serial.print(",");
    }
  }
  Serial.print(",");
  for (int i = 0; i < 2; i++) {
    Serial.print(yPos[i]);
    if (i < 2 - 1) {
      Serial.print(",");
    }
  }
  Serial.println("");

  delay(200);
}

void detectTouch() {
  for (int i = 0; i < 2; i++) {
    if (sensorReadings[i] < touchThresholds[i] && !isTouched[i]) {
      isTouched[i] = 1;
    }
    if (sensorReadings[i] > touchThresholds[i] && isTouched[i]) {
      isTouched[i] = 0;
    }
  }
}

void detectRelease() {
  for (int i = 0; i < 2; i++) {
    if (!isTouched[i] && prevIsTouched[i]) {
      isReleased[i] = 1;
    } else {
      isReleased[i] = 0;
    }
  }
}

void detectYPos() {
  for (int i = 0; i < 2; i++) {
    if (isTouched[i]) {
      yPos[i] = map(sensorReadings[i], minReadings[i], maxReadings[i], 0, 255);
    }
  }
}
