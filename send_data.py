import asyncio
import json
import base64

import nats
from loguru import logger

SERVERS = [
    "nats://localhost:4222",
]
USER = "user1"
PASSWORD = "secret1"
TOPIC = "recognize_tasks"


def encode_payload(data: dict) -> bytes:
    return base64.b64encode(json.dumps(data).encode())


async def run():
    async def error_cb(e):
        logger.exception(e)

    async def reconnected_cb():
        logger.info("Got reconnected to NATS...")

    options = {
        "error_cb": error_cb,
        "reconnected_cb": reconnected_cb,
        "user": USER,
        "password": PASSWORD,
        "servers": SERVERS,
    }

    nc = None
    try:
        nc = await nats.connect(**options)
    except Exception as e:
        print(e)

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

    await nc.publish(TOPIC, data)

    logger.info("Finished")


if __name__ == "__main__":
    asyncio.run(run())
