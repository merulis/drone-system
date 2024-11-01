from system.client.brocker import MQTTClientDroneSide
from system.core.settings import settings


subscriber = MQTTClientDroneSide()
subscriber.start_connetion(
    username=settings.MQTT_BROKER_USER,
    password=settings.MQTT_BROKER_PASSWORD,
    host=settings.MQTT_BROKER_HOST,
    port=settings.MQTT_BROKER_PORT,
)

subscriber.subscribe(topic="test", qos=0)
subscriber.loop_forever()
