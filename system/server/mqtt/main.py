from system.core.settings import settings
from system.server.mqtt.broker import MQTTClientBackendSide

publisher = MQTTClientBackendSide()
publisher.start_connetion(
    username=settings.MQTT_BROKER_USER,
    password=settings.MQTT_BROKER_PASSWORD,
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT,
)
