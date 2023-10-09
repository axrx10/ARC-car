
from RPi.GPIO import GPIO  

import time

class DistanceSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, False)

    def read(self):
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2

        return distance

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    sensor = DistanceSensor(trig_pin=23, echo_pin=24)
    try:
        while True:
            distance = sensor.read()
            print(f"Distance: {distance} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        sensor.cleanup()
