import paho.mqtt.client as mqtt
import DHT11
import RPi.GPIO as GPIO
import json
import ssl
import signal
from time import sleep

# GPIO initilization that's needed for dht11 module to work
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Value for the I2C DHT module
# PLEASE CHANGE THIS FOR YOUR BREADBOARD
reading = DHT11.DHT11(pin = 12).read()

# Data values for temperature and humidity
tempdata = reading.temperature
humiddata = reading.humidity

print("Temperature in SE: ",tempdata)
print("Humidity in SE: ",humiddata)

# Message that prints on connection
def on_connect(client, userdata, flags, rc):
    print("Connected ", rc)

# Message that prints on successful publish 
def on_publish(client, userdata, result):
    print("Published ", result)

# Declaration of mqtt client
MQTT_CLIENT_ID = "KatelynRPI" # Client Identification. Please change this
                             # to "[your name]RPI"
MQTT_USERNAME = "ExMzCh87ORUQEx4QMi4SNCc" #My Author Code. Change to your publishing device's Username.
MQTT_PASSWD = "HxIMVEeheAoQsFgC15g6ShJt" #My Profile API code. Change to your publishing device's password.
MQTT_HOST = "mqtt.thingspeak.com" #ThingSpeak hostname. Keep as is.
MQTT_PORT = 8883 #TLS port number
CHANNEL_ID = "1570491" #Channel ID. Keep as is.
MQTT_WRITE_APIKEY = "26J8RXGEDIL9QXVI" # Write API Key. Keep as is.
MQTT_PUBLISH_TOPIC = "channels/" + CHANNEL_ID + "/publish/" + MQTT_WRITE_APIKEY
root_cert_path = "./cacert.pem"


try:
    # MQTT client setup and initilization
    client = mqtt.Client(client_id= MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.username_pw_set(username = MQTT_USERNAME, password=MQTT_PASSWD)
    client.tls_set(ca_certs=root_cert_path, certfile=None, keyfile=None,
                        cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(False)
    client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
    client.on_connect = on_connect
    client.loop_start()

    client.on_connect = on_connect
    client.on_publish = on_publish
    # Data publish
    while True:
        if not client.is_connected:
            print("Client disconnected. Trying to reconnect.")
            client.reconnect()
        jsonvalue=json.dumps({"name":MQTT_CLIENT_ID, "temperature":str(reading.temperature), "humidity":str(reading.humidity)})

        pub_topic = "field1=" + jsonvalue
        client.loop_start()
        client.publish(MQTT_PUBLISH_TOPIC, pub_topic)
        sleep(15)

# Exception catch for clean exit
except KeyboardInterrupt:
    client.disconnect()
    print("\rExiting Program...")
    signal.SIGINT
