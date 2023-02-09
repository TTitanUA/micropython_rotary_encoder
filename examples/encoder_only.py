from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
import uasyncio as asyncio

# constants
ENCODER_CLK_PIN = 15
ENCODER_DT_PIN = 9


# Define the pins for the rotary encoder and the button
encoder_pin_clk = Pin(ENCODER_CLK_PIN, Pin.IN, Pin.PULL_UP)
encoder_pin_dt = Pin(ENCODER_DT_PIN, Pin.IN, Pin.PULL_UP)

# Create the rotary encoder object
encoder = RotaryEncoderRP2(
    pin_clk=encoder_pin_clk,
    pin_dt=encoder_pin_dt,
)


# Listeners
def any_event_listener(event, clicks):
    print(f"ANY Event ID: {event} Clicks: {clicks}")


def turn_left_listener():
    print(f"Turn Left")


def turn_left_fast_listener():
    print(f"Turn Left Fast")


def turn_right_listener():
    print(f"Turn Right")


def turn_right_fast_listener():
    print(f"Turn Right Fast")


# subscribe to events
encoder.on(RotaryEncoderEvent.ANY, any_event_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT, turn_left_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST, turn_left_fast_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT, turn_right_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST, turn_right_fast_listener)


# Start the event loop
print(f"Connect you rotary encoder to the next GPIO pins: CLK {ENCODER_CLK_PIN}, DT {ENCODER_DT_PIN}")
print("Then interact with it to test the firing of events. Button events will be disabled.")
asyncio.run(encoder.async_tick())
