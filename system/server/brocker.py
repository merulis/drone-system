import logging

from paho.mqtt.client import (
    LogLevel,
    Client,
    MQTTv5,
    CallbackAPIVersion,
)


class MQTTClientBackendSide(Client):
    def __init__(
        self,
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id="",
        clean_session=None,
        userdata=None,
        protocol=MQTTv5,
        transport="tcp",
        reconnect_on_failure=True,
        manual_ack=False,
        logger: logging.Logger = None,
    ):
        super().__init__(
            callback_api_version,
            client_id,
            clean_session,
            userdata,
            protocol,
            transport,
            reconnect_on_failure,
            manual_ack,
        )
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

    def on_log(
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
        logging_on: bool = True
    ):
        if logging_on:
            logging.basicConfig(level=logging.INFO)

        self.username_pw_set(username=username, password=password)
        self.connect(host=host, port=port)
