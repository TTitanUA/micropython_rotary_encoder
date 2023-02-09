from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
import uasyncio as asyncio

# constants
ENCODER_SW_PIN = 8


# Define the pin for the button
encoder_pin_sw = Pin(ENCODER_SW_PIN, Pin.IN, Pin.PULL_UP)

# Create the rotary encoder object
encoder = RotaryEncoderRP2(
    pin_sw=encoder_pin_sw,
)


# Listeners
def any_event_listener(event, clicks):
    print(f"ANY Event ID: {event} Clicks: {clicks}")


def single_click_listener():
    print(f"Single Click")


def multy_click_listener(clicks):
    print(f"Multiply Clicks: {clicks}")


def held_listener():
    print(f"Held")


def released_listener():
    print(f"Released")


# subscribe to events
encoder.on(RotaryEncoderEvent.ANY, any_event_listener)
encoder.on(RotaryEncoderEvent.CLICK, single_click_listener)
encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, multy_click_listener)
encoder.on(RotaryEncoderEvent.HELD, held_listener)
encoder.on(RotaryEncoderEvent.RELEASED, released_listener)


# Start the event loop
print("Using such a huge library to collect button events is overkill for me, but if you need to...")
print(f"Connect you button to the next GPIO pin: SW {ENCODER_SW_PIN}")
print("Then interact with it to test the firing of events.")
asyncio.run(encoder.async_tick())
