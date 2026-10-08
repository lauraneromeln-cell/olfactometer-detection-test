// 4-channel olfactometer: 3 odors (one of which is the control = peppermint) and one blank

// Pin assignment
#define VALVE_PEPPERMINT 7   
#define VALVE_ROSE 5         
#define VALVE_CINNAMON 4    
#define VALVE_BLANK 3        

bool sequenceActive = false;
unsigned long duration = 0;
int repetitions = 0;
int activeValve = 1;
unsigned long phaseStart = 0;
int counter = 0;
bool valveState = false;

void setup() {
  Serial.begin(9600);

  pinMode(VALVE_PEPPERMINT, OUTPUT);
  pinMode(VALVE_ROSE, OUTPUT);
  pinMode(VALVE_CINNAMON, OUTPUT);
  pinMode(VALVE_BLANK, OUTPUT);

  stopAll();

  Serial.println("Arduino 4-Channel Olfactometer Ready");
}

void loop() {

  // --------- COMMAND RECEPTION ----------
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "STOP") {
      stopAll();
    }
    else if (command.startsWith("OPEN")) {
      int v = command.substring(5).toInt();
      openValve(v);
    }
    else if (command.startsWith("CLOSE")) {
      stopAll();
    }
    else if (command.startsWith("START")) {
      // Format: START valve duration repetitions
      sscanf(command.c_str(), "START %d %lu %d", &activeValve, &duration, &repetitions);
      sequenceActive = true;
      counter = 0;
      valveState = true; // Start by opening
      openValve(activeValve);
      phaseStart = millis();
    }
  }

  // --------- SEQUENCE MANAGEMENT (original algorithm) ----------
  if (sequenceActive) {
    if (millis() - phaseStart >= duration) {
      phaseStart = millis();
      valveState = !valveState;

      if (valveState) {
        openValve(activeValve);
      } else {
        closeValve(activeValve);
        counter++;
        if (counter >= repetitions) {
          stopAll();
          Serial.println("SEQUENCE COMPLETE");
        }
      }
    }
  }
}

void openValve(int v) {
  stopAll(); // Safety: close everything before opening the target valve
  if (v == 1) digitalWrite(VALVE_PEPPERMINT, HIGH);
  else if (v == 2) digitalWrite(VALVE_ROSE, HIGH);
  else if (v == 3) digitalWrite(VALVE_CINNAMON, HIGH);
  else if (v == 4) digitalWrite(VALVE_BLANK, HIGH);
}

void closeValve(int v) {
  if (v == 1) digitalWrite(VALVE_PEPPERMINT, LOW);
  else if (v == 2) digitalWrite(VALVE_ROSE, LOW);
  else if (v == 3) digitalWrite(VALVE_CINNAMON, LOW);
  else if (v == 4) digitalWrite(VALVE_BLANK, LOW);
}

void stopAll() {
  sequenceActive = false;
  digitalWrite(VALVE_PEPPERMINT, LOW);
  digitalWrite(VALVE_ROSE, LOW);
  digitalWrite(VALVE_CINNAMON, LOW);
  digitalWrite(VALVE_BLANK, LOW);
}
