
# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random

########
follow_left = True
########


SPEED_GAIN = 5
TURN_SPEED = 10
STOP_DISTANCE = 20
TURN_LEFT_DISTANCE = 25
MAX_WALL_DISTANCE = 20
MIN_WALL_DISTANCE = 16



def turn_robot_left(left_dist, iterations, speed_motor):

    speed_turn_1 = int(speed_motor / (left_dist / 20)) 
    speed_turn_2 = int(speed_motor)
    
    for i in range(iterations):
        if follow_left == True:
            motor_serial.send_command(speed_turn_2, speed_turn_1)
            time.sleep(0.05)
        else:
            motor_serial.send_command(speed_turn_1, speed_turn_2)
            time.sleep(0.05)
            
def turn_robot_right(iterations):
    turn_duration = (iterations / (SPEED_GAIN * 0.12))

    for i in range(iterations):
        if follow_left == True:
            motor_serial.send_command(TURN_SPEED, TURN_SPEED)
            time.sleep(0.05)
    
        
def drive_forwards(speed1, speed2):
    
    for i in range(iterations):
        motor_serial.send_command(speed2, speed1)
        time.sleep(0.05)

def adjust_left(angle):
    adjust_speed_1 = int((1/angle) * speed_motor)
    adjust_speed_2 = int(speed_motor)
    motor_serial.send_command(adjust_speed_2,adjust_speed_1 )
    time.sleep(0.05)


def adjust_right(angle):
    adjust_speed_1 = int(speed_motor)
    adjust_speed_2 = int((1/angle) * speed_motor)
    motor_serial.send_command(adjust_speed_2, adjust_speed_1)
    time.sleep(0.05)
        
# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :

 # Get and print readings from distance sensors
    # 1=front-left, 2=front-right, 3=right_front, 4=right-back, 5=left-front, 6=left-back
    dist_1 = motor_serial.get_dist_1() 
    dist_2 = motor_serial.get_dist_2() 
    dist_3 = motor_serial.get_dist_3() 
    dist_4 = motor_serial.get_dist_4()
    dist_5 = motor_serial.get_dist_5() 
    dist_6 = motor_serial.get_dist_6()
    print("Dist 1:", dist_1, "   Dist 2:", dist_2, "   Dist 3:", dist_3, "   Dist 4:", dist_4, "   Dist 5:", dist_5, "   Dist 6:", dist_6)

    speed_motor_1 = int(dist_1 * SPEED_GAIN)
    speed_motor_2 = int(dist_2 * SPEED_GAIN)
    speed_motor = int((speed_motor_1 + speed_motor_2)/2)
    left_angle = abs(dist_5 - dist_6)
    right_angle = abs(dist_3 - dist_4)
    
    # Check if there is an obstacle in the way
    if follow_left == True:
        DIRECTION = 1

        if dist_5 > TURN_LEFT_DISTANCE:

            turn_robot_left(dist_5, 1, speed_motor)
            
        elif dist_1 < STOP_DISTANCE or dist_2 < STOP_DISTANCE:

            turn_robot_right(10)

        else:
            if dist_5 < MIN_WALL_DISTANCE:
                adjust_right(left_angle)

            elif dist_5 > MAX_WALL_DISTANCE:
                adjust_left(left_angle)
            else:
                drive_forwards(speed_motor_1, speed_motor_2)
            
            

        
        

    else:
        DIRECTION = 1
        if dist_3 > TURN_LEFT_DISTANCE:
            turn_robot_left(dist_3, 1)
