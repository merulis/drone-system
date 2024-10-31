import time
import logging

import paho.mqtt.client as mqtt


def on_connect(client, userdata, falgs, rc, props):
    logger.info(f"Connected with result code {str(rc)}")


def on_publish(client, userdata, mid, rc, props):
    logger.info(f"Publish - message ID: {mid}, result code {str(rc)}")


def on_disconnet(client, userdata, falgs, rc, props):
    logger.info(f"Disconnect with result code {str(rc)}")


logging.basicConfig(level=logging.INFO)

publisher = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

publisher.on_connect = on_connect
publisher.on_publish = on_publish
publisher.on_disconnect = on_disconnet

logger = logging.getLogger(__name__)
publisher.enable_logger(logger)

publisher.connect(host="localhost", port=1883)


publisher.loop_start()

for i in range(100):
    time.sleep(2)
    publisher.publish(topic="test", qos=0, payload=f"Test message {i}")

publisher.loop_stop()
publisher.disconnect()
