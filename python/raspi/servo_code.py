
import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.OUT)

pwm=GPIO.PWM(13, 50)

pwm.start(5)

def SetAngle(angle):
        for s in range(angle)
                duty = angle / 18 + 2
                GPIO.output(13, True)
                pwm.ChangeDutyCycle(duty)
                sleep(0.1)
                GPIO.output(13, False)
                pwm.ChangeDutyCycle(0)

for i in range(5):
        SetAngle(30)

        sleep(0.1)
        SetAngle(5)




pwm.stop()

GPIO.cleanup()
