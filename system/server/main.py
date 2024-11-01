import time

from system.core.settings import settings
from system.server.brocker import MQTTClientBackendSide


publisher = MQTTClientBackendSide()
publisher.start_connetion(
    username=settings.MQTT_BROKER_USER,
    password=settings.MQTT_BROKER_PASSWORD,
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT,
)

publisher.loop_start()

for i in range(100):
    time.sleep(2)
    publisher.publish(topic="test", qos=0, payload=f"Test message {i}")

publisher.loop_stop()
publisher.disconnect()
