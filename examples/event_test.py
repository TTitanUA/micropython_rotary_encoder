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


def turn_left_listener():
    print(f"Turn Left")


def turn_left_hold():
    print(f"Turn Left Hold")


def turn_left_fast_listener():
    print(f"Turn Left Fast")


def turn_left_fast_hold():
    print(f"Turn Left Fast Hold")


def turn_right_listener():
    print(f"Turn Right")


def turn_right_hold():
    print(f"Turn Right Hold")


def turn_right_fast_listener():
    print(f"Turn Right Fast")


def turn_right_fast_hold():
    print(f"Turn Right Fast Hold")


# subscribe to events
encoder.on(RotaryEncoderEvent.ANY, any_event_listener)
encoder.on(RotaryEncoderEvent.CLICK, single_click_listener)
encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, multy_click_listener)
encoder.on(RotaryEncoderEvent.HELD, held_listener)
encoder.on(RotaryEncoderEvent.RELEASED, released_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT, turn_left_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT_HOLD, turn_left_hold)
encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST, turn_left_fast_listener)
encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST_HOLD, turn_left_fast_hold)
encoder.on(RotaryEncoderEvent.TURN_RIGHT, turn_right_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT_HOLD, turn_right_hold)
encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST, turn_right_fast_listener)
encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST_HOLD, turn_right_fast_hold)


# Start the event loop
print(f"Connect you rotary encoder to the next GPIO pins: CLK {ENCODER_CLK_PIN}, DT {ENCODER_DT_PIN} and SW {ENCODER_SW_PIN}")
print("Then interact with it to test the firing of events.")
asyncio.run(encoder.async_tick())
