from machine import Pin, Timer
import uasyncio as asyncio
from .rotary_encoder import RotaryEncoder


class RotaryEncoderRP2(RotaryEncoder):
    timer: Timer = None
    alive: bool = True

    def __init__(
            self,
            pin_clk: Pin = None,
            pin_dt: Pin = None,
            pin_sw: Pin = None,
            debounce_ms: int = 50,
            encoder_step: int = 1,
            hold_ms: int = 1000,
            step_ms: int = 200,
            fast_ms: int = 50,
            click_ms: int = 400,

    ):
        super().__init__(
            pin_clk=pin_clk,
            pin_dt=pin_dt,
            pin_sw=pin_sw,
            debounce_ms=debounce_ms,
            encoder_step=encoder_step,
            hold_ms=hold_ms,
            step_ms=step_ms,
            fast_ms=fast_ms,
            click_ms=click_ms,
        )

        self._enable_irq()

    def __delete__(self, instance):
        self.alive = False

        if self.timer is not None:
            self.timer.deinit()

    async def async_tick(self, timeout=1):
        """async_tick is used to process the encoder events. It should be run by asyncio."""
        while self.alive:
            self.__tick()
            await asyncio.sleep_ms(timeout)

    def timer_tick(self, timeout=1):
        """
            timer_tick is used to process the encoder events. It automatically creates the system irq timer.
            :link https://docs.micropython.org/en/latest/rp2/quickref.html#timers
        """
        self.timer = Timer(-1, period=timeout, mode=Timer.PERIODIC, callback=lambda t: self.__tick())

    def raw_tick(self):
        """raw_tick is used to process the encoder events. It should be run by the main loop manually. """
        self.__tick()

    def _enable_irq(self):
        if self.pin_clk is not None and self.pin_dt is not None:
            self.pin_clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._enc_irq_handler)
            self.pin_dt.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._enc_irq_handler)

        if self.pin_sw is not None:
            self.pin_sw.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._sw_irq_handler)
