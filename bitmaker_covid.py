from microbit import *
import time
import speech

class Servo:

    """
    A simple class for controlling hobby servos.
    Args:
        pin (pin0 .. pin3): The pin where servo is connected.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between minimum and maximum positions.
    Usage:
        SG90 @ 3.3v servo connected to pin0
        = Servo(pin0).write_angle(90)
    """

    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
        sleep(100)
        #self.pin.write_digital(0)  # turn the pin off

    def write_angle(self, degrees=None):
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)
    
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

def _get_distance(pin):
    pin.write_digital(0)
    time.sleep_us(2)
    pin.write_digital(1)
    time.sleep_us(10)
    pin.write_digital(0)

    t0 = time.ticks_us()
    count = 0
    while count < _TIMEOUT1:
        if pin.read_digital():
            break
        count += 1
    if count >= _TIMEOUT1:
        return -1

    t1 = time.ticks_us()
    count = 0
    while count < _TIMEOUT2:
        if not pin.read_digital():
            break
        count += 1
    if count >= _TIMEOUT2:
        return -1
    t2 = time.ticks_us()
    dt = int(time.ticks_diff(t1,t0))

    if dt > 5300:
        return -1
    distance = (time.ticks_diff(t2,t1) / 29 / 2)    # cm
    return distance


display.clear()
stage = 0
start_time = 0
sv1 = Servo(pin1)
sv1.write_angle(90) # turn servo to 90 degrees

while True:

    distance = _get_distance(pin2)
    if distance <= 10 and distance > 0:
        if time.ticks_diff(time.ticks_ms(), start_time) >= 1000:
            stage += 1
            start_time = time.ticks_ms()
        
        if stage == 1:
            speech.say("COMMENCING EXTERMINATION OF CORONA-VIRUS", speed=120, pitch=100, throat=100, mouth=200)
            sv1.write_angle(80)        
        if stage == 2: 
            speech.say("CORONA-VIRUS WILL BE EXTER-MI-NATED", speed=120, pitch=100, throat=100, mouth=200)
            sv1.write_angle(70)  
        if stage == 3: 
            speech.say("CORONA-VIRUS WILL BE EXTER-MI-NATED", speed=120, pitch=100, throat=100, mouth=200)
            sv1.write_angle(60) 
        if stage == 4:
            speech.say("VICTORY OVER CORONA-VIRUS IS NEAR", speed=120, pitch=100, throat=100, mouth=200)
            sv1.write_angle(50)
        if stage == 5:
            speech.say("CORONA-VIRUS HAS BEEN EXTER-MI-NATED", speed=120, pitch=100, throat=100, mouth=200)
            sv1.write_angle(40)
            stage = 0
            sleep(1000)
    else:
        
        if stage == 0: sv1.write_angle(90)
        if stage != 0:
            speech.say("CORONA-VIRUS IS ESCAPING ", speed=120, pitch=100, throat=100, mouth=200)
            sv1.write_angle(90)
            stage = 0
