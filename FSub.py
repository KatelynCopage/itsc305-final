from time import sleep
import ssl
import json
import paho.mqtt.client as mqtt

MQTT_CLIENT_ID = "Gr5FinalProjSub" # This is for your own client identification. Can be anything
MQTT_USERNAME = "EA8bMCsuIgYAJCkSFTcAOTE" #This is the ThingsSpeak's Author
MQTT_PASSWD = "7dozBqqYOQsmZlaJVVouk06d" #This is the MQTT API Key found under My Profile in ThingSpeak
MQTT_HOST = "mqtt.thingspeak.com" #This is the ThingSpeak hostname
MQTT_PORT = 8883 #Typical port # for MQTT protocol. If using TLS -> 8883
CHANNEL_ID = "1570491" #Channel ID found on ThingSpeak website
MQTT_READ_APIKEY = "P6X4T8MEN2XK7JAV" # Write API Key found under ThingSpeak Channel Settings
MQTT_SUBSCRIBE_TOPIC = "channels/" + CHANNEL_ID + "/subscribe/fields/field1/" #+ MQTT_READ_APIKEY
root_cert_path = "./cacert.pem"
"""
Standard callback functions. See Phao MQTT documentation for more
This will be called on receipt of a message from the subscribed topic(s)
"""
#def on_message(client, userdata, message):
#	print("Message topic: ", message.topic)
#	print("Message payload: ", message.payload)
#	print("Message QoS: ", message.qos)
#	x = json.loads(message.payload)
#	print(x)


def on_subscribe(client, userdata, mid, granted_qos):
	print("subscribed", userdata)

#def tls_set(ca_certs=root_cert_path, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS, ciphers=None):
#	print("TLS", ciphers)

def on_connect(client, userdata, flags, rc):
	print("Connected ", rc)

def on_message(client, userdata, message):
        print("Message topic: ", message.topic)
        print("Message payload: ", message.payload)
        print("Message QoS: ", message.qos)
        x = json.loads(message.payload)
        print(x)

def on_log(client, userdata, level, buf):
	print("log:", buf)

try:
	client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
	client.tls_set(ca_certs=root_cert_path, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
	client.tls_insecure_set(False)

	client.on_subscribe = on_subscribe
	client.on_connect = on_connect
	client.on_message = on_message


	client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWD)
	client.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)

	client.loop_start()

	client.subscribe(MQTT_SUBSCRIBE_TOPIC, qos=0)

	while True:
		sleep(1)
		if not client.is_connected:
			print("Client disconnected. Trying to reconnect.")
			client.reconnect()

except KeyboardInterrupt:
	client.unsubscribe(MQTT_SUBSCRIBE_TOPIC)
	client.disconnect()
