import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio
import threading

# LED를 켜고 끄는 함수
def controlLED(on_off):
    GPIO.output(led, on_off)

def getTemperature() : # 센서로부터 온도 값 수신 함수
    return round(sensor.temperature,1) # HTU21D 장치로부터 온도 값 읽기
def getHumidity() : # 센서로부터 습도 값 수신 함수
    return round(sensor.relative_humidity,1) # HTU21D 장치로부터 습도 값 읽기



def measure_distance():
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
    return distance
            
trig = 20    # GPIO20 
echo = 16    # GPIO16 
led = 6     # GPIO6
sda = 2 # GPIO2 핀. sda 이름이 붙여진 핀
scl = 3 # GPIO3 핀. scl 이름이 붙여진 핀
i2c = busio.I2C(scl, sda) # I2C 버스 통신을 실행하는 객체 생성
sensor = HTU21D(i2c) # I2C 버스에서 HTU21D 장치를 제어하는 객체 리턴

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

