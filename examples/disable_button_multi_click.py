from machine import Pin
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
import utime

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
    step_ms=0,  # disable MULTIPLE_CLICK event
)


# Listeners
def click_listener():
    print(f"click_listener")


def multy_click_listener():
    print(f"multi_click_listener")


# subscribe to events
encoder.on(RotaryEncoderEvent.CLICK, click_listener)
encoder.on(RotaryEncoderEvent.MULTIPLE_CLICK, multy_click_listener)

# Subscribe to system timer irq
encoder.timer_tick()


# Start the event loop
print(f"Connect you rotary encoder to the next GPIO pins: CLK {ENCODER_CLK_PIN}, DT {ENCODER_DT_PIN} and SW {ENCODER_SW_PIN}")
print("In this example, we disable a MULTIPLE_CLICK event.")

while True:
    utime.sleep(1)
