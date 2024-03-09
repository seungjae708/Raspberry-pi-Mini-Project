import time
import RPi.GPIO as GPIO
import threading
import cv2

def button_pressed(channel):
    print("%d 핀에 연결된 스위치 눌러짐" % channel)

def measure_distance(trig, echo, distance_callback):
    while True:
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)

        pulse_start = time.time()
        pulse_end = time.time()

        while GPIO.input(echo) == GPIO.LOW:
            pulse_start = time.time()

        while GPIO.input(echo) == GPIO.HIGH:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 340 * 100 / 2

        distance_callback(distance)
        time.sleep(0.5)  

def led_on_off(led_pin, value):
    GPIO.output(led_pin, value)

def button_thread():
    GPIO.add_event_detect(button, GPIO.RISING, button_pressed, bouncetime=10)
    while True:
        time.sleep(0.1)

def distance_callback(distance):
    if distance < 10:
        value = GPIO.HIGH  # GPIO.HIGH turns the LED on
    else:
        value = GPIO.LOW   # GPIO.LOW turns the LED off

    led_on_off(led, value)

button = 21 
trig = 20    
echo = 16    
led = 6     

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

button_thread = threading.Thread(target=button_thread)
button_thread.start()

distance_thread = threading.Thread(target=measure_distance, args=(trig, echo, distance_callback))
distance_thread.start()

try:
    while True:
        time.sleep(1)  

except KeyboardInterrupt:
    GPIO.cleanup()
    camera.release()

