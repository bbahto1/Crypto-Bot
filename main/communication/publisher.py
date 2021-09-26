import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "crypto-bot-messages"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, message):
    msg = message
    for sent_msg in msg:
        time.sleep(10)
        result = client.publish(topic, sent_msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{sent_msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
    
def run(message):
    client = connect_mqtt()
    client.loop_start()
    publish(client, message)


if __name__ == '__main__':
    run()