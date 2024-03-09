import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import circuit

def on_connect(client, userdata,flag, rc):
	client.subscribe("led", qos = 0) # "led" 토픽으로 구독 신청
def on_message(client, userdata, msg) :
	on_off = int(msg.payload); # on_off는 0 또는 1의 정수
	circuit.controlLED(on_off) # LED를 켜거나 끔
ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성
# 도착하는 메시지는 on_message() 함수에 의해 처리되어 LED를 켜거나 끄는 작업과
# 병렬적으로 5초 단위로 온습도 센서로부터 온습도 정보를 읽어 전송하는 무한 루프 실행
button = 21

while True:
	distance = circuit.measure_distance()
	if (distance<10):
		value="하는"
	else:
		value="쉬는"
	client.publish("학생", value, qos=0)
	
	if (circuit.getTemperature()<21 and circuit.getTemperature()>18):
		temp="가 적당합니다"
	elif(circuit.getTemperature()>=21):
		temp="를 내려주세요"
	elif(circuit.getTemperature()<=18):
		temp="를 올려주세요"
	if (circuit.getHumidity()<60 and circuit.getHumidity()>40):
		humd="가 적당합니다"
	elif(circuit.getHumidity()>=60):
		humd="를 내려주세요"
	elif(circuit.getHumidity()<=40):
		humd="를 올려주세요"
	
	client.publish("Temp", temp, qos=0)
	client.publish("Humd", humd, qos=0)
	client.publish("온도", circuit.getTemperature(), qos=0)
	client.publish("습도", circuit.getHumidity(), qos=0)
	time.sleep(1) # 1초 동안 잠자기
client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
