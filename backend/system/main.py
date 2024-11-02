from system
from system.server.mqtt.client import MQTTClient

publisher = MQTTClient()
publisher.start_connetion(
    username=settings.MQTT_BROKER_USER,
    password=settings.MQTT_BROKER_PASSWORD,
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT,
)

publisher.publish("test", "Hello MQTT!")

while True:
    pass
