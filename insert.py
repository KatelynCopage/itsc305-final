import requests
import json
import DHT11
import RPi.GPIO as GPIO
from time import sleep


URL="https://web305.naxr.ca:8443/insert_data"
APIKEY="4abdbf603e44bcd5bfa7f2250f24310d09441e9d30dad004f0762edf358c0069"
NAME="KatelynRPI"


def send_reading(name, temperature, humidity):
  payload = {
    'key': APIKEY,
    'name': name,
    'temperature': str(temperature),
    'humidity': str(humidity)
  }
  r = requests.post(URL, data=payload)
  print("sent reading")

# GPIO initilization that's needed for dht11 module to work
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

sensor = DHT11.DHT11(pin=12)

def get_dht11_reading(sensor):
  result = sensor.read()

  while not result.is_valid():
   print("failed to read sensor, retrying..")
   result = sensor.read()
   sleep(0.5)
  print("got reading " + str(result.temperature) + " " + str(result.humidity))
  return result


while True:
  reading = get_dht11_reading(sensor)
  send_reading(NAME, reading.temperature, reading.humidity)
  sleep(60)
