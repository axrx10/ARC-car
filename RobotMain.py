from motorModule import Motor
import controllerModule as controller

motor = Motor(2,3,4,17,22,27)

def main():
    
    jsValues = controller.getJS()
    # If they are positive, the robot will move wrong direction
    motor.move(-(jsValues['axis2']),-(jsValues['axis1']),0.1)
    
    # Test motor
    #motor.move(0.6,0,2)
    #motor.stop(2)
    #motor.move(-0.5,0.2,2)
    #motor.stop(2)
 
if __name__ == '__main__':
    while True:
        main()