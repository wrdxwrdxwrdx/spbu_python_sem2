from unittest.mock import patch

import pytest

from src.homeworks.chat.client import *
from src.homeworks.chat.server import *


class TestClientSend:
    ip, port = "127.0.0.1", 8888

    @staticmethod
    async def echo_handler(reader: StreamReader, writer: StreamWriter) -> None:
        while True:
            message = (await reader.readline()).decode()
            logger.info(message)
            writer.write(message.encode())
            await writer.drain()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("message", ("Hello\n", "Bye\n", "Smth\n"))
    @patch("sys.stdin.readline")
    async def test_send_message(self, mock_stdin, message):
        mock_stdin.return_value = message
        server = await asyncio.start_server(self.echo_handler, self.ip, self.port)
        async with server:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
            send_task = asyncio.create_task(Client.send_message(writer))
            echo_message = (await reader.readline()).decode()
            assert echo_message == message
            send_task.cancel()
            server.close()


class TestClientGet:
    ip, port = "127.0.0.1", 8888

    @pytest.mark.asyncio
    @pytest.mark.parametrize("message", ("Hello\n", "Bye\n", "Smth\n"))
    async def test_send_message(self, message):
        async def client_handler(reader: StreamReader, writer: StreamWriter) -> None:
            while True:
                writer.write(message.encode())
                await writer.drain()

        server = await asyncio.start_server(client_handler, self.ip, self.port)
        async with server:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
            get_task = asyncio.create_task(Client.get_message(reader))
            got_message = (await reader.readline()).decode()
            assert got_message == message
            get_task.cancel()
            server.close()
