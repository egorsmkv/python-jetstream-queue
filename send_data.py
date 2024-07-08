import json
import base64

from pynats import NATSClient
from loguru import logger

SERVER = "nats://user1:secret1@localhost:4222"
TOPIC = "recognize_tasks"


def encode_payload(data: dict) -> bytes:
    return base64.b64encode(json.dumps(data).encode())


def run():
    with NATSClient(url=SERVER) as client:
        client.connect()

        # Subscribe
        def callback(msg):
            print(f"Received a message with subject {msg.subject}: {msg}")

        client.subscribe(subject="test-subject", callback=callback)

        logger.info(f"Trying to publish data to [{TOPIC}]")

        data = encode_payload(
            {
                "payload": {
                    "task": "recognize_webhook",
                    "body": encode_payload(
                        {
                            "audio_url": "...",
                            "webhook_url": "...",
                        }
                    ).decode(),
                }
            }
        )

        client.publish(subject=TOPIC, payload=data)

        logger.info("Finished")


if __name__ == "__main__":
    run()
