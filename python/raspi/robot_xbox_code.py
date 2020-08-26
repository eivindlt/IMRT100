
# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys


import struct
import threading
import time


DRIVING_SPEED = 200

def drive_forwards(speed1, speed2, iterations):
    
    for i in range(iterations):
        motor_serial.send_command(speed2, speed1)
        time.sleep(0.02)


        
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

def __init__(self, device="/dev/input/js0", deadzone=0.2):
        self._mutex = threading.Lock()
        self._shutdown_thread = False
        self._buttons = [False] * 15
        self._axes = [0.0] * 8
        self._button_idx = {
            "A":       0,
            "B":       1,
            "X":       2,
            "Y":       3,
            "LB":      4,
            "RB":      5,
            "Back":    6,
            "Start":   7,
            "Xbox":    8,
            "Lstick":  9,
            "Rstick": 10,
            "Left":   11,
            "Right":  12,
            "Up":     13,
            "Down":   14
        }

        self._axes_idx = {
            "LX": 0,
            "LY": 1,
            "LT": 2,
            "RX": 3,
            "RY": 4,
            "RT": 5
        }

        self._device_listener = threading.Thread(target=self._listen_thread, args=(device, deadzone))
        self._device_listener.start()

  

def _listen_thread(self, device, deadzone):
        
        
        evnt_size = struct.calcsize("ihBB")
        controller_connected = False
        
        self._mutex.acquire()
        shutdown_thread = self._shutdown_thread
        self._mutex.release()
    
    
        while not shutdown_thread:

            try:
                if not controller_connected:
                    file = open(device, "rb")
                    controller_connected = True
                    print("Xbox controller connected!")
                
                else:
                    event = file.read(evnt_size)
                    (but_time, but_value, but_type, but_num) = struct.unpack("ihBB", event)
                    if but_type == 1:
                        self._mutex.acquire()
                        self._buttons[but_num] = not but_value
                        self._mutex.release()

                    elif but_type == 2:
                        but_value /= 32767.
                        if abs(but_value) < deadzone:
                            but_value = 0.
                        self._mutex.acquire()
                        self._axes[but_num] = but_value 
                        self._mutex.release()
            
            except OSError:
                if controller_connected:
                    print("Cannot find xbox controller. Is it on?")
                    controller_connected = False
                time.sleep(0.5)


            self._mutex.acquire()
            shutdown_thread = self._shutdown_thread
            self._mutex.release()

                

        if controller_connected:
            file.close()




def shutdown(self, blocking=True):
        self._mutex.acquire()
        self._shutdown_thread = True
        self._mutex.release()
        if blocking:
            self._device_listener.join()


def get_left_x(self):
        self._mutex.acquire()
        value = self._axes[self._axes_idx["LX"]]
        self._mutex.release()
        return value

def get_left_y(self):
        self._mutex.acquire()
        value = -self._axes[self._axes_idx["LY"]]
        self._mutex.release()
        return value

def get_left_trigger(self):
        self._mutex.acquire()
        value = self._axes[self._axes_idx["LT"]]
        self._mutex.release()
        return value

def get_right_x(self):
        self._mutex.acquire()
        value = self._axes[self._axes_idx["RX"]]
        self._mutex.release()
        return value

def get_right_y(self):
        self._mutex.acquire()
        value = -self._axes[self._axes_idx["RY"]]
        self._mutex.release()
        return value

def get_right_trigger(self):
        self._mutex.acquire()
        value = self._axes[self._axes_idx["RT"]]
        self._mutex.release()
        return value



def get_a(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["A"]]
        self._mutex.release()
        return value

def get_b(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["B"]]
        self._mutex.release()
        return value

def get_x(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["X"]]
        self._mutex.release()
        return value

def get_y(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Y"]]
        self._mutex.release()
        return value

def get_left_bumper(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["LB"]]
        self._mutex.release()
        return value

def get_right_bumper(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["RB"]]
        self._mutex.release()
        return value

def get_back(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Back"]]
        self._mutex.release()
        return value

def get_start(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Start"]]
        self._mutex.release()
        return value

def get_xbox(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Xbox"]]
        self._mutex.release()
        return value

def get_left_stick(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Lstick"]]
        self._mutex.release()
        return value

def get_right_stick(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Rstick"]]
        self._mutex.release()
        return value

def get_dpad_left(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Left"]]
        self._mutex.release()
        return value

def get_dpad_right(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Right"]]
        self._mutex.release()
        return value

def get_dpad_up(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Up"]]
        self._mutex.release()
        return value

def get_dpad_down(self):
        self._mutex.acquire()
        value = self._buttons[self._button_idx["Down"]]
        self._mutex.release()
        return value



# Example of usage
def main():
    controller = IMRTxbox()

    try:
        while(True):
            but_a = controller.get_a()
            but_b = controller.get_b()
            but_x = controller.get_x()
            but_y = controller.get_y()

            but_lt = controller.get_right_trigger()
            but_lt = controller.get_right_trigger()
            
            ax_lx = controller.get_left_x()
            ax_ly = controller.get_left_y()
            ax_rx = controller.get_right_x()
            ax_ry = controller.get_right_y()

            print("a: {}, b: {}, x: {}, y: {}, lx: {:+.2f}, ly: {:+.2f}, rx: {:+.2f}, ry: {:+.2f}".format(but_a, but_b, but_x, but_y, ax_lx, ax_ly, ax_rx, ax_ry), end='\r')
            print("Left trigger", but_lt, "Right trigger", but_rt)

            time.sleep(0.1)

            if but_rt < 0:
                but_rt = 1 -(abs(but_rt))
            else:
                    but_rt = but_rt + 1
            if but_lt <= 0:
                but_lt = 1 -(abs(but_lt))
            else:
                    but_lt = but_lt + 1

            if ax_lx < 0:
                left_turn_speed = (2 - (2*(abs(ax_lx))))

            else:
                right_turn_speed = (2 - ((2*abs(ax_lx))))

            if but_rt > 0 and ax_lx < 0 :
                speed1 = left_turn_speed * DRIVING_SPEED
                speed2 = DRIVING_SPEED
                motor_serial.send_command(speed1, speed2)
                time.sleep(0.05)

            elif but_rt > 0 and ax_lx < 0 :
                speed1 = DRIVING_SPEED
                speed2 = right_turn_speed * DRIVING_SPEED
                motor_serial.send_command(speed1, speed2)
                time.sleep(0.05)

                
            

    except KeyboardInterrupt:
        print("\nTerminated by user")

    finally:
        controller.shutdown()
        print("Exiting program")


