from motorModule import Motor
#import controllerModule as controller
from distanceSensor import DistanceSensor
import time

sensor = DistanceSensor()
motor = Motor(2,3,4,17,22,27)

def main():
    # uncomment when testing
    #jsValues = controller.getJS()
    # If they are positive, the robot will move wrong direction
    #motor.move(-(jsValues['axis2']),-(jsValues['axis1']),0.1)
    
    # Test motor
    #motor.move(0.6,0,2)
    #motor.stop(2)
    #motor.move(-0.5,0.2,2)
    #motor.stop(2)
    
    try:
        while True:
            distance = sensor.get_distance()
            print("Distance:", distance, "cm")

            if distance <= 20:
                print("Car stopped moving")
                motor.stop(2)  # Stop the motor
            else:
                # You can add motor movement logic here
                motor.move(0.6, 0, 2)  # Example movement

            time.sleep(1)  # Delay between each distance check

    finally:
        sensor.cleanup()
 
if __name__ == '__main__':
    while True:
        main()