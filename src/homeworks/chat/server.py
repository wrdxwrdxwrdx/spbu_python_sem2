import asyncio
from argparse import ArgumentParser
from asyncio import StreamReader, StreamWriter
from typing import Optional

from loguru import logger


class Chat:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.users: dict[str, tuple[StreamReader, StreamWriter]] = {}

    async def send_to_everyone(self, message: str, dodge_name: Optional[str] = None) -> None:
        tasks = []
        for username, (reader, writer) in self.users.items():
            if username != dodge_name:
                writer.write(message.encode())
                tasks.append(writer.drain())
        await asyncio.gather(*tasks)

    async def get_name(self, reader: StreamReader, writer: StreamWriter) -> str:
        writer.write("Welcome to Chat, please enter your USERNAME:\n".encode())
        await writer.drain()
        username = (await reader.readline()).decode().strip()
        while username in self.users:
            writer.write(f"{username} already taken. Please select another:\n".encode())
            await writer.drain()
            username = (await reader.readline()).decode().strip()
        return username

    async def connect_user(self, username: str, reader: StreamReader, writer: StreamWriter) -> None:
        self.users[username] = (reader, writer)
        await self.send_to_everyone(f"{username} connected\n")
        logger.info(f"User '{username}' connected")

    async def disconnect_user(self, username: str) -> None:
        self.users[username][1].close()
        await self.users[username][1].wait_closed()
        del self.users[username]
        await self.send_to_everyone(f"{username} disconnected\n")
        logger.info(f"{username} disconnected")

    async def client_handler(self, reader: StreamReader, writer: StreamWriter) -> None:
        username = await self.get_name(reader, writer)
        await self.connect_user(username, reader, writer)
        while True:
            message_byte = await reader.readline()
            if message_byte == b"":
                await self.disconnect_user(username)
                break
            else:
                message = message_byte.decode()
                await self.send_to_everyone(f"{username}: {message}", dodge_name=username)

    async def main(self) -> None:
        server = await asyncio.start_server(self.client_handler, self.ip, self.port)

        async with server:
            logger.info(f"Server started {self.ip}:{self.port}")
            await server.serve_forever()


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--ip", type=str, default="127.0.0.1", help="Enter server IP")
    argparser.add_argument("--port", type=int, default=8888, help="Enter server PORT")
    args = argparser.parse_args()

    chat = Chat(**vars(args))
    asyncio.run(chat.main())
