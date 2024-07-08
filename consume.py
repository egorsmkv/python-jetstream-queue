import signal
import asyncio
import json
import base64

import nats
from nats.aio.msg import Msg
from loguru import logger

SERVERS = [
    "nats://localhost:4222",
]
USER = "user1"
PASSWORD = "secret1"
TOPIC = "recognize_tasks"
QUEUE = ""


def decode_message(msg: Msg) -> dict:
    return json.loads(base64.b64decode(msg.data))


def decode_str(data: str) -> dict:
    return json.loads(base64.b64decode(data))


async def run():
    async def error_cb(e):
        logger.exception(e)

    async def closed_cb():
        await asyncio.sleep(0.2)
        loop.stop()

    async def reconnected_cb():
        logger.info("Got reconnected to NATS...")

    async def subscribe_handler(msg: Msg):
        data = decode_message(msg)
        payload = data["payload"]

        match payload["task"]:
            case "recognize_webhook":
                payload = decode_str(payload["body"])

                audio_url = payload["audio_url"]
                webhook_url = payload["webhook_url"]

                logger.info(
                    "We should recognize a file {url} and send the webhook to {webhook}",
                    url=audio_url,
                    webhook=webhook_url,
                )
            case _:
                logger.error(f"Got unknown task: {payload['task']}")

    options = {
        "error_cb": error_cb,
        "closed_cb": closed_cb,
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

    logger.info(f"Listening on [{TOPIC}]")

    def signal_handler():
        if nc.is_closed:
            return
        asyncio.create_task(nc.drain())

    for sig in ("SIGINT", "SIGTERM"):
        asyncio.get_running_loop().add_signal_handler(
            getattr(signal, sig), signal_handler
        )

    await nc.subscribe(TOPIC, QUEUE, subscribe_handler)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run())
    try:
        loop.run_forever()
    finally:
        loop.close()
