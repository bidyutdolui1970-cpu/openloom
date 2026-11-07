// OpenLoom - pocket History flashcard device
// Board: ESP32 Dev Module | Libraries: Adafruit GFX, Adafruit SSD1306
// Wiring: OLED SDA->GPIO21, SCL->GPIO22 | FLIP button->GPIO18 | NEXT button->GPIO19 | Active buzzer->GPIO23

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_W 128
#define SCREEN_H 64
#define OLED_ADDR 0x3C

const int BTN_FLIP = 18;
const int BTN_NEXT = 19;
const int BUZZER   = 23;

Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire, -1);

struct Card {
  const char* question;
  const char* answer;
};

// Edit this list to add your own cards.
Card cards[] = {
  {"Battle of Plassey?", "1757"},
  {"Battle of Buxar?", "1764"},
  {"Permanent Settlement of Bengal?", "1793"},
  {"Partition of Bengal?", "1905"},
  {"Jallianwala Bagh massacre?", "1919"},
  {"Quit India Movement?", "1942"},
  {"Independence of India?", "1947"},
};
const int CARD_COUNT = sizeof(cards) / sizeof(cards[0]);

int current = 0;
bool showingAnswer = false;

void beep(int ms) {
  digitalWrite(BUZZER, HIGH);
  delay(ms);
  digitalWrite(BUZZER, LOW);
}

void drawCard() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextWrap(true);

  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Card ");
  display.print(current + 1);
  display.print("/");
  display.println(CARD_COUNT);
  display.drawLine(0, 11, SCREEN_W - 1, 11, SSD1306_WHITE);

  if (!showingAnswer) {
    display.setCursor(0, 17);
    display.println(cards[current].question);
    display.setCursor(0, 55);
    display.print("FLIP: show answer");
  } else {
    const size_t answerLength = strlen(cards[current].answer);
    const uint8_t textSize = answerLength <= 4 ? 3 : (answerLength <= 8 ? 2 : 1);
    display.setTextSize(textSize);
    display.setCursor(0, 29);
    display.println(cards[current].answer);
    display.setTextSize(1);
    display.setCursor(0, 55);
    display.print("NEXT: continue");
  }
  display.display();
}

bool pressed(int pin) {
  if (digitalRead(pin) == LOW) {
    delay(30);  // debounce
    if (digitalRead(pin) == LOW) {
      while (digitalRead(pin) == LOW) delay(5);  // wait for release
      return true;
    }
  }
  return false;
}

void setup() {
  pinMode(BTN_FLIP, INPUT_PULLUP);
  pinMode(BTN_NEXT, INPUT_PULLUP);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  Wire.begin(21, 22);
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    while (true) delay(1000);  // OLED not found
  }

  randomSeed(analogRead(34));
  current = random(CARD_COUNT);
  drawCard();
}

void loop() {
  if (pressed(BTN_FLIP)) {
    showingAnswer = !showingAnswer;
    beep(30);
    drawCard();
  }
  if (pressed(BTN_NEXT)) {
    current = (current + 1) % CARD_COUNT;
    showingAnswer = false;
    beep(30);
    drawCard();
  }
}
