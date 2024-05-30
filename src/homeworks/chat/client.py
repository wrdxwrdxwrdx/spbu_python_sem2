import asyncio
import sys
import time
from argparse import ArgumentParser
from asyncio import StreamReader, StreamWriter

from loguru import logger


class Client:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

    @staticmethod
    async def get_message(reader: StreamReader) -> None:
        while True:
            message = await reader.readline()
            if message == b"":
                logger.info("Server crashed :( ")
                break
            print(message.decode().strip())

    @staticmethod
    async def send_message(writer: StreamWriter) -> None:
        while True:
            message = await asyncio.get_running_loop().run_in_executor(None, sys.stdin.readline)
            writer.write(message.encode())
            await writer.drain()

    async def connect(self) -> tuple[StreamReader, StreamWriter]:
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        return reader, writer

    async def main(self) -> None:
        reader, writer = await self.connect()
        loop = asyncio.get_event_loop()
        read_task = loop.create_task(self.get_message(reader))
        write_task = loop.create_task(self.send_message(writer))
        while loop.is_running():
            await asyncio.sleep(0)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--ip", type=str, default="127.0.0.1", help="Enter server IP")
    argparser.add_argument("--port", type=int, default=8888, help="Enter server PORT")
    args = argparser.parse_args()

    client = Client(**vars(args))
    try:
        asyncio.run(client.main())
    except KeyboardInterrupt as err:
        print("client closed")
