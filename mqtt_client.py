import paho.mqtt.client as mqtt
from typing import Callable, Optional, Set
import threading

class MQTTClient:
    def __init__(self, on_message_callback: Callable[[str, str], None]):
        self.client: Optional[mqtt.Client] = None
        self.mqtt_thread: Optional[threading.Thread] = None
        self.on_message_callback = on_message_callback
        self.subscribed_topics: Set[str] = set()
        self.is_connected = False

    def connect(self, broker: str, port: int, client_id: str) -> bool:
        try:
            self.client = mqtt.Client(client_id=client_id)
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.connect(broker, port, 60)

            self.mqtt_thread = threading.Thread(target=self.client.loop_forever)
            self.mqtt_thread.daemon = True
            self.mqtt_thread.start()
            self.is_connected = True
            return True
        except Exception as e:
            self.is_connected = False
            raise ConnectionError(f"Failed to connect: {str(e)}")

    def disconnect(self):
        if self.client:
            self.client.disconnect()
            self.client = None
            self.is_connected = False
            self.subscribed_topics.clear()

    def subscribe(self, topic: str) -> bool:
        if self.client and self.is_connected:
            self.client.subscribe(topic)
            self.subscribed_topics.add(topic)
            return True
        return False

    def unsubscribe(self, topic: str):
        if self.client and self.is_connected:
            self.client.unsubscribe(topic)
            self.subscribed_topics.remove(topic)

    def get_subscribed_topics(self) -> Set[str]:
        return self.subscribed_topics

    def publish(self, topic: str, message: str):
        if self.client and self.is_connected:
            self.client.publish(topic, message)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe("iotapp/status")
            self.subscribed_topics.add("iotapp/status")
            client.publish("iotapp/status", "Application Connect Success")
        else:
            self.is_connected = False

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        message = msg.payload.decode()
        self.on_message_callback(topic, message)