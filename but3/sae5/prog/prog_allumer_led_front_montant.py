from machine import Pin
import time

LED = Pin(2, Pin.OUT)
BP = Pin(4, Pin.IN, Pin.PULL_UP)  # Bouton sur la broche GPIO 4 avec pull-up

def button_isr(pin):
  LED.value(not LED.value())

BP.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)
