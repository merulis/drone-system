import logging

from system.core.settings import settings

import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage

def on_connect(client, userdata, falgs, rc, props):
    logger.info(f"Connected with result code {str(rc)}")


def on_subscribe(client, userdata, mid, rc, props):
    logger.info(f"Subscribe - result code {str(rc)}")


def on_message(client, userdata, message: MQTTMessage):
    logger.info(f"Message: {message.payload.decode()}")


def on_disconnet(client, userdata, falgs, rc, props):
    logger.info(f"Disconnect with result code {str(rc)}")


logging.basicConfig(level=logging.INFO)

subscriber = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

subscriber.on_connect = on_connect
subscriber.on_subscribe = on_subscribe
subscriber.on_message = on_message
subscriber.on_disconnect = on_disconnet

logger = logging.getLogger(__name__)
subscriber.enable_logger(logger)

subscriber.username_pw_set(
    username=settings.MQTT_BROKER_USER,
    password=settings.MQTT_BROKER_PASSWORD,
)
subscriber.connect(
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT,
)

subscriber.subscribe(topic="test", qos=0)

subscriber.loop_forever()
