import RPi.GPIO as GPIO
import time

class MotorControl:
    def __init__(self):
        # Set up GPIO pins
        GPIO.setmode(GPIO.BOARD)
        
        # Define pin numbers for motor control
        self.left_motor_pin1 = 11  # GPIO17
        self.left_motor_gnd = 25  # Ground
        
        self.right_motor_pin1 = 13  # GPIO27
        self.right_motor_gnd = 39  # Ground

        # Set up PWM for motor control
        GPIO.setup(self.left_motor_pin1, GPIO.OUT)
        GPIO.setup(self.right_motor_pin1, GPIO.OUT)

        self.left_motor_pwm = GPIO.PWM(self.left_motor_pin1, 100)
        self.right_motor_pwm = GPIO.PWM(self.right_motor_pin1, 100)

    # Define functions for motor control
    def forward(self):
        self.left_motor_pwm.start(100)
        self.right_motor_pwm.start(100)

    def backward(self):
        self.left_motor_pwm.start(100)
        self.right_motor_pwm.start(100)

    def turn_left(self):
        self.left_motor_pwm.start(50)
        self.right_motor_pwm.start(100)

    def turn_right(self):
        self.left_motor_pwm.start(100)
        self.right_motor_pwm.start(50)

    def stop(self):
        self.left_motor_pwm.stop()
        self.right_motor_pwm.stop()
