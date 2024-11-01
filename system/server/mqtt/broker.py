import asyncio
import logging
import socket
import contextlib
import enum

from typing import (
    Any,
    Self,
    Literal,
    Generator,
    Iterable,
    TypeVar,
)

from paho.mqtt.client import (
    LogLevel,
    Client,
    MQTT_ERR_SUCCESS,
    MQTTv5,
    MQTTv31,
    MQTTv311,
    CallbackAPIVersion,
    ReasonCode,
    WebsocketConnectionError,
    Properties,
    DisconnectFlags,
    ConnectFlags,
    CONNACK_ACCEPTED,
    CleanStartOption,
    MQTT_CLEAN_START_FIRST_ONLY,
)

from system.core.settings import settings

T = TypeVar("T")


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
        clean_session: bool | None = None,
        clean_start: CleanStartOption = MQTT_CLEAN_START_FIRST_ONLY,
        timeout: float | None = None,
        properties: Properties | None = None,
    ):
        self._hostname = hostname
        self._port = port
        self._loop = asyncio.get_running_loop()
        self._clean_start = clean_start
        self.props = properties

        self._pending_subs: dict[
            int, asyncio.Future[tuple[int, ...] | list[ReasonCode]]
        ] = {}
        self._pending_pubs: dict[int, asyncio.Event] = {}

        self._connected: asyncio.Future[None] = asyncio.Future()
        self._disconnected: asyncio.Future[None] = asyncio.Future()
        self._lock: asyncio.Lock = asyncio.Lock()

        if protocol is None:
            protocol = MQTTProtocol.V311

        self._client: Client = Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=protocol.value,
            transport=transport,
            clean_session=clean_session,
            reconnect_on_failure=False,
        )

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_log = self._on_log
        self._client.on_subscribe = self._on_subscribe
        self._client.on_publish = self._on_publish

        if username is not None:
            self._client.username_pw_set(username=username, password=password)

        if logger is None:
            self.logger = logging.getLogger("MQTT")

        if timeout is None:
            timeout = 10
        self.timeout = timeout

    @property
    def _pending_calls(self) -> Generator[int, None, None]:
        yield from self._pending_pubs.keys()
        yield from self._pending_subs.keys()

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

        confirmation = asyncio.Event()
        with self._pending_call(info.mid, confirmation, self._pending_pubs):
            # TODO: set timeout
            await asyncio.wait_for(confirmation.wait(), timeout=self.timeout)

    @contextlib.contextmanager
    def _pending_call(self, mid, value: T, pending_dict: dict[int, T]):
        if mid in self._pending_calls:
            msg = f"There already exists a pending call for message ID: {mid}"
            # FIXME: Create exception
            raise Exception(msg)

        pending_dict[mid] = value
        try:
            # Out from context
            yield
        finally:
            # We must try delete event in context manager
            # anyway delete event after out of context for safety
            try:
                del pending_dict[mid]
            except KeyError:
                pass

    def _on_connect(
        self,
        client: Client,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None = None,
    ) -> None:
        if self._connected.done():
            return

        if reason_code == CONNACK_ACCEPTED:
            self._connected.set_result(None)
        else:
            # We received a negative CONNACK response
            self._connected.set_exception(Exception(reason_code))

    def _on_disconnect(
        self,
        client: Client,
        userdata: Any,
        flags: DisconnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None = None,
    ) -> None:
        if self._disconnected.done():
            return

        if not self._connected.done() or self._connected.exception() is not None:
            return

        if reason_code == MQTT_ERR_SUCCESS:
            self._disconnected.set_result(None)
        else:
            self._disconnected.set_exception(
                Exception(reason_code, "Unexpected disconnection")
            )

    def _on_subscribe(self):
        pass

    def _on_publish(
        self,
        client: Client,
        userdata: Any,
        mid: int,
        reason_code: ReasonCode,
        props,
    ):
        try:
            self._pending_pubs.pop(mid).set()
        except KeyError:
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

    async def __aenter__(self) -> Self:
        if self._lock.locked():
            msg = "Async eventloop is locked"
            raise Exception(msg)
        await self._lock.acquire()
        try:
            loop = asyncio.get_event_loop()
            loop.run_in_executor(
                None,
                self._client.connect,
                self._hostname,
                self._port,
            )
        except (OSError, WebsocketConnectionError) as e:
            self._lock.release()
            msg = "Mqtt error"
            raise e(msg) from None
        try:
            await asyncio.wait_for(self._connected, timeout=None)
        except Exception:
            self._lock.release()
            self._connected = asyncio.Future()
            raise
        if self._disconnected.done():
            self._disconnected = asyncio.Future()
            return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb,
    ) -> None:
        if self._disconnected.done():
            if self._lock.locked():
                self._lock.release()
            if (exc := self._disconnected.exception()) is not None:
                raise exc
            return

        rc = self._client.disconnect()
        if rc == MQTT_ERR_SUCCESS:
            await asyncio.wait_for(self._disconnected, timeout=None)

            if self._connected.done():
                self._connected = asyncio.Future()
        else:
            self._logger.warning(
                f"Could not gracefully disconnect: {rc}. Forcing disconnection."
            )

        if not self._disconnected.done():
            self._disconnected.set_result(None)

        if self._lock.locked():
            self._lock.release()


async def main():
    async with AsyncMQTTClient(
        hostname=settings.MQTT_BROKER_HOST,
        port=settings.MQTT_BROKER_PORT,
        username=settings.MQTT_BROKER_USER,
        password=settings.MQTT_BROKER_PASSWORD,
        protocol=MQTTProtocol.V5,
    ) as client:
        await client.publish("test", payload="#TEST#MASSAGE#")


asyncio.run(main())
