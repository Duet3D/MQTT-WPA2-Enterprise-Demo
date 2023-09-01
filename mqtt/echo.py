# Runs the MQTT broker and echo client. See README.md for more information
# about the demonstration this Python script is a part of.

import paho.mqtt.client as mqtt
import subprocess

from colorama import Fore
from colorama import Style

HOST = "demo-router"
PORT = 1883
USERNAME = "mqtt-echo"
PASSWORD = "mqtt-echo-pswd"
CLIENT_ID = "echo"
SUBSCRIBE_TOPIC = "topic-duet"
PUBLISH_TOPIC = "topic-echo"
WILL_TOPIC = "topic-will"

topics = dict()

def broker():
    # Start the Mosquitto broker in verbose mode, using the config file.
    subprocess.run(["mosquitto", "-v", "-c", "mosquitto.conf"])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        def display(result, topic):
            if result == 0:
                print(f"{Fore.YELLOW}echo: subscribe to '{topic}' succeeded, waiting for messages...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}echo: subscribe to '{topic}' failed.{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}echo: connect succeeded, subscribing to topic '{SUBSCRIBE_TOPIC}'...{Style.RESET_ALL}")
        result, _ = client.subscribe(SUBSCRIBE_TOPIC)
        display(result, SUBSCRIBE_TOPIC)

        print(f"{Fore.YELLOW}echo: subscribing to will topic '{WILL_TOPIC}'...{Style.RESET_ALL}")
        result, _ = client.subscribe(WILL_TOPIC)
        display(result, WILL_TOPIC)
    else:
        print(f"{Fore.YELLOW}echo: connect failed, result code: {rc}{Style.RESET_ALL}")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == SUBSCRIBE_TOPIC:
        print(f"{Fore.YELLOW}echo: received message with topic '{msg.topic}': '{msg.payload}', echoing... {Style.RESET_ALL}")
        res = client.publish(PUBLISH_TOPIC, msg.payload, msg.qos, msg.retain)

        if res[0] == 0:
            print(f"{Fore.YELLOW}echo: echo succeeded {Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}echo: echo failed, result code: ${res[0]}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}echo: recieved will message with topic '{msg.topic}': {msg.payload} {Style.RESET_ALL}")

def main():
    client = mqtt.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    print(f"{Fore.YELLOW}echo: connecting to '{HOST}' on port '{PORT}' as '{CLIENT_ID}'{Style.RESET_ALL}...")
    client.connect(HOST, PORT)
    client.loop_forever()

if __name__ == '__main__':
    main()