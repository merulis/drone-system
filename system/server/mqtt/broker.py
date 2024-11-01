import asyncio
import logging
import enum

from typing import (
    Literal,
)

from paho.mqtt.client import (
    LogLevel,
    Client,
    MQTT_ERR_SUCCESS,
    MQTTv5,
    MQTTv31,
    MQTTv311,
    CallbackAPIVersion,
    MQTTMessageInfo,
)


class MQTTProtocol(enum.IntEnum):
    V31 = MQTTv31
    V311 = MQTTv311
    V5 = MQTTv5


class AsyncMQTTClient:
    def __init__(
        self,
        hostname: str,
        username: str | None = None,
        password: str | None = None,
        port: int = 1883,
        logger: logging.Logger | None = None,
        client_id: str | None = None,
        protocol: MQTTProtocol = None,
        transport: Literal["tcp", "websocket", "unix"] = "tcp",
        clean_session: bool = False,
    ):
        self._hostname = hostname
        self._port = port
        self._loop = asyncio.get_running_loop()

        self._lock: asyncio.Lock = asyncio.Lock()

        self._client: Client = Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=protocol,
            transport=transport,
            clean_session=clean_session,
            reconnect_on_failure=False,
        )

        self._client.on_log = self._on_log
        self._client.on_subscribe = self._on_subscribe
        self._client.on_publish = self._on_publish

        if username is not None:
            self.username_pw_set(username=username, password=password)

        if logger is None:
            self.logger = logging.getLogger("MQTT")

    async def subscribe(self, topic, qos):
        result_code, mid = self._client.subscribe(topic=topic, qos=qos)

        if result_code != MQTT_ERR_SUCCESS or mid is None:
            # FIXME: Create Exeptions
            raise Exception(result_code, "Could not subscribe to topic")

    async def publish(
        self,
        topic,
        payload,
        qos,
        retain: bool = False,
    ):
        info = self._client.publish(
            topic=topic,
            payload=payload,
            qos=qos,
            retain=retain,
        )

        if info.rc != MQTT_ERR_SUCCESS:
            # FIXME: Create Exeptions
            raise Exception(info.rc, "Could not publish message")

        if info.is_published():
            return

    def _on_subscribe(self):
        pass

    def _on_publish(self):
        pass

    def _on_log(
        self,
        client,
        obj,
        level: LogLevel,
        buf,
    ):
        match level:
            case LogLevel.MQTT_LOG_DEBUG:
                self.logger.info(f"MQTT_LOG_DEBUG:{buf}")
            case LogLevel.MQTT_LOG_INFO:
                self.logger.info(f"MQTT_LOG_INFO:{buf}")
            case LogLevel.MQTT_LOG_NOTICE:
                self.logger.info(f"MQTT_LOG_NOTICE:{buf}")

    def start_connetion(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        logging_on: bool = True,
    ):
        if logging_on:
            logging.basicConfig(level=logging.INFO)

        self.username_pw_set(username=username, password=password)
        self.connect(host=host, port=port)
