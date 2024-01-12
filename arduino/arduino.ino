#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    1000

CRGB leds[NUM_LEDS];

void setup() {
    FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
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
            fill_rainbow(leds, NUM_LEDS, thisHue, deltaHue);
            delay(100);
            FastLED.show();
            return;
        } else if (values[1] == 1) {
            // Set the RGB and brightness values
            fill_solid(leds, NUM_LEDS, CRGB(values[2], values[3], values[4]));
            FastLED.show();
            return;
        } else {
            // Change the color of each LED in the strip gradually to the specified new color.
            fill_gradient_RGB(leds, 0, CRGB(values[2], values[3], values[4]), NUM_LEDS, CRGB(values[2], values[3], values[4]));
            FastLED.show();
            return;
        }
    } else if (values[0] == 0) {
        // If the first value is not 1, turn off all LEDs
        for (int i = 0; i < NUM_LEDS; i++) {
            leds[i] = CRGB::Black;
        }
        FastLED.show();
        return;
    }
    delay(500);
}