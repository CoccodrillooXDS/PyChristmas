#include <FastLED.h>

#define LED_PIN_STRISCIA1     3
#define NUM_LEDS_STRISCIA1    300

#define LED_PIN_STRISCIA2     4
#define NUM_LEDS_STRISCIA2    350

#define LED_PIN_STRISCIA3     5
#define NUM_LEDS_STRISCIA3    350

CRGB leds1[NUM_LEDS_STRISCIA1];
CRGB leds2[NUM_LEDS_STRISCIA2];
CRGB leds3[NUM_LEDS_STRISCIA3];

void setup() {
    FastLED.addLeds<WS2812, LED_PIN_STRISCIA1, GRB>(leds1, NUM_LEDS_STRISCIA1);
    FastLED.addLeds<WS2812, LED_PIN_STRISCIA2, GRB>(leds2, NUM_LEDS_STRISCIA2);
    FastLED.addLeds<WS2812, LED_PIN_STRISCIA3, GRB>(leds3, NUM_LEDS_STRISCIA3);
    Serial.begin(9600);
}

void loop() {
    String input = Serial.readStringUntil('\n');
    // Parse the input string into an array
    int values[6];
    int index = 0;
    for (int i = 0; i < 6; i++) {
        values[i] = -1;
    }
    char inputChars[input.length() + 1];
    input.toCharArray(inputChars, input.length() + 1);
    char* chars_array = strtok(inputChars, ",\n"); // Include '\n' in the delimiter string
    while(chars_array) {
        values[index++] = atoi(chars_array);
        chars_array = strtok(NULL, ",\n"); // Include '\n' in the delimiter string
    }
    Serial.println("OK");
    // Check the first value for enabling/disabling LEDs
    if (values[0] == 1) {
        // Check the second value for instant LED change or rainbow LED change
        if (values[1] == 2) {
            uint8_t thisSpeed = 10;
            uint8_t deltaHue= 10;
            uint8_t thisHue = beat8(thisSpeed,255); 
            fill_rainbow(leds1, NUM_LEDS_STRISCIA1, thisHue, deltaHue);
            fill_rainbow(leds2, NUM_LEDS_STRISCIA2, thisHue, deltaHue);
            fill_rainbow(leds3, NUM_LEDS_STRISCIA3, thisHue, deltaHue);
            delay(100);
            FastLED.show();
            return;
        } else if (values[1] == 1) {
            // Set the RGB and brightness values
            fill_solid(leds1, NUM_LEDS_STRISCIA1, CRGB(values[2], values[3], values[4]));
            fill_solid(leds2, NUM_LEDS_STRISCIA2, CRGB(values[2], values[3], values[4]));
            fill_solid(leds3, NUM_LEDS_STRISCIA3, CRGB(values[2], values[3], values[4]));
            FastLED.show();
            return;
        } else {
            // Change the color of each LED in the strip gradually to the specified new color.
            fill_gradient_RGB(leds1, 0, CRGB(values[2], values[3], values[4]), NUM_LEDS_STRISCIA1, CRGB(values[2], values[3], values[4]));
            fill_gradient_RGB(leds2, 0, CRGB(values[2], values[3], values[4]), NUM_LEDS_STRISCIA2, CRGB(values[2], values[3], values[4]));
            fill_gradient_RGB(leds3, 0, CRGB(values[2], values[3], values[4]), NUM_LEDS_STRISCIA3, CRGB(values[2], values[3], values[4]));
            FastLED.show();
            return;
        }
    } else if (values[0] == 0) {
        // If the first value is not 1, turn off all LEDs
        for (int i = 0; i < NUM_LEDS_STRISCIA1; i++) {
            leds[i] = CRGB::Black;
        }
        for (int i = 0; i < NUM_LEDS_STRISCIA2; i++) {
            leds[i] = CRGB::Black;
        }
        for (int i = 0; i < NUM_LEDS_STRISCIA3; i++) {
            leds[i] = CRGB::Black;
        }
        FastLED.show();
        return;
    }
    delay(500);
}