from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
import uasyncio as asyncio

# constants
ENCODER_CLK_PIN = 15
ENCODER_DT_PIN = 9
ENCODER_SW_PIN = 8


# Define the pins for the rotary encoder and the button
encoder_pin_clk = Pin(ENCODER_CLK_PIN, Pin.IN, Pin.PULL_UP)
encoder_pin_dt = Pin(ENCODER_DT_PIN, Pin.IN, Pin.PULL_UP)
encoder_pin_sw = Pin(ENCODER_SW_PIN, Pin.IN, Pin.PULL_UP)

# Create the rotary encoder object
encoder = RotaryEncoderRP2(
    pin_clk=encoder_pin_clk,
    pin_dt=encoder_pin_dt,
    pin_sw=encoder_pin_sw,
)


# Listeners
def click_listener_1():
    print(f"Click listener #1")


def click_listener_2():
    print(f"Click listener #2")


# Add the listeners #1
encoder.on(RotaryEncoderEvent.CLICK, click_listener_1)
encoder.on(RotaryEncoderEvent.CLICK, click_listener_1)
encoder.on(RotaryEncoderEvent.CLICK, click_listener_1)
encoder.on(RotaryEncoderEvent.CLICK, click_listener_1)
encoder.on(RotaryEncoderEvent.CLICK, click_listener_1)

# Add the listeners #2
encoder.on(RotaryEncoderEvent.CLICK, click_listener_2)


# Remove listeners #1
def remove_click_listener_1(clicks):
    if clicks == 2:
        encoder.off(RotaryEncoderEvent.CLICK, click_listener_1)
        print("Removed click listener #1")
    elif clicks == 3:
        encoder.off_all(RotaryEncoderEvent.CLICK, click_listener_1)
        print("Removed all click listener #1")
    else:
        print(f"It is not a double click and not triple click. Clicks {clicks}")


encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, remove_click_listener_1)


# Remove all listeners
def remove_all_click_listeners():
    print("Removed all click listeners")
    encoder.off_all(RotaryEncoderEvent.CLICK)


encoder.on(RotaryEncoderEvent.HELD, lambda: print("Release the button to remove all click listeners"))
encoder.on(RotaryEncoderEvent.RELEASED, remove_all_click_listeners)


# Add listeners again
def add_click_listener_1():
    encoder.on(RotaryEncoderEvent.CLICK, click_listener_1)
    print("Added click listener #1")


encoder.on(RotaryEncoderEvent.TURN_RIGHT, add_click_listener_1)


def add_click_listener_2():
    encoder.on(RotaryEncoderEvent.CLICK, click_listener_2)
    print("Added click listener #2")


encoder.on(RotaryEncoderEvent.TURN_LEFT, add_click_listener_2)


# Start the event loop
print(f"Connect you rotary encoder to the next GPIO pins: CLK {ENCODER_CLK_PIN}, DT {ENCODER_DT_PIN} and SW {ENCODER_SW_PIN}")
print("Now you can do next actions:")
print("1. Turn the encoder to the right to add click listener #1")
print("2. Turn the encoder to the left to add click listener #2")
print("3. Double click to remove one click listener #1")
print("4. Triple click to remove all click listener #1")
print("5. Hold the button to remove all click listeners")
print("6. Click to show click listeners feedback")
print("Have fun!")
asyncio.run(encoder.async_tick())
