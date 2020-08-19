
# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random

#Setting initial values for variables

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1

#Master adjustments
MASTER_SPEED = 2
MASTER_WALL_DISTANCE = 1.2
TURN_LEFT_DISTANCE = 40

DRIVING_SPEED = 100 * MASTER_SPEED
TURNING_SPEED = 100 * MASTER_SPEED
STOP_DISTANCE = int (22 * MASTER_SPEED) 
MAX_WALL_DISTANCE = int(12 * MASTER_WALL_DISTANCE)
MIN_WALL_DISTANCE = int(10 * MASTER_WALL_DISTANCE)
CORRECTION_SPEED = 85 * MASTER_SPEED
INNER_WHEEL_SPEED = 10 * MASTER_SPEED


follow_left = True

def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)

def stop_robot_left():

    iterations = int(2 / MASTER_SPEED)
    
    for i in range(iterations):
        drive_robot(FORWARDS, 0.1)
        time.sleep(0.10)
    motor_serial.send_command(0, 0)



def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)



def turn_robot_right():

    direction = 1
    iterations = int(13 / MASTER_SPEED)
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)

def turn_robot_left():

    direction = -1
    iterations = int(30 / MASTER_SPEED)
    
    for i in range(iterations):
        motor_serial.send_command(INNER_WHEEL_SPEED, -TURNING_SPEED * direction)
        time.sleep(0.10)
        
def straighten_robot_left():

    direction = 1
    iterations = 1
    print("Straighten left")
    
    for i in range(iterations):
        motor_serial.send_command(CORRECTION_SPEED * direction, DRIVING_SPEED *direction)
        time.sleep(0.10)

def straighten_robot_right():

    direction = 1
    iterations = 1
    print("Straighten right")
    
    for i in range(iterations):
        motor_serial.send_command(DRIVING_SPEED * direction, CORRECTION_SPEED * direction)
        time.sleep(0.10)




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


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    ###############################################################
    ###############################################################
 

    # Get and print readings from distance sensors
    # 1=front, 2=left, 3=right, 4=left back
    dist_1 = motor_serial.get_dist_1() 
    dist_2 = motor_serial.get_dist_2() 
    dist_3 = motor_serial.get_dist_3() 
    dist_4 = motor_serial.get_dist_4()
    dist_5 = motor_serial.get_dist_5() 
    dist_6 = motor_serial.get_dist_6()
    print("Dist 1:", dist_1, "   Dist 2:", dist_2, "   Dist 3:", dist_3, "   Dist 4:", dist_4, "   Dist 5:", dist_5, "   Dist 6:", dist_6)

    # Check if there is an obstacle in the way

    if dist_5 and dist_6 > TURN_LEFT_DISTANCE:

        print("No wall on the left side, turn left")
        stop_robot()


        # Turn robot left
        turn_robot_left()

        drive_robot(FORWARDS, 1)
    
    
        
   

    #Turn robot right

    elif dist_1 < STOP_DISTANCE or dist_2 < STOP_DISTANCE :
        print("Obstacle, turn right!")
        
        stop_robot(1)

        turn_robot_right()
  
        

# If there is nothing in front of the robot it continus driving forwards
    else:
        if dist_2 < MIN_WALL_DISTANCE:
            straighten_robot_right()
            
        elif dist_2 > MAX_WALL_DISTANCE:
            straighten_robot_left()
            
    
        else:
            drive_robot(FORWARDS, 0.1)
            print("FORWARDS")


print("Goodbye")
