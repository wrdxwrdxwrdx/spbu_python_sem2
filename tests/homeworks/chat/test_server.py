import pytest

from src.homeworks.chat.server import *


class TestChat:
    ip, port = "127.0.0.1", 8888

    @staticmethod
    async def read_from_reader(reader: StreamReader):
        messages = []
        while True:
            message = await reader.readline()
            if message == b"" or message.decode() == "QUIT":
                break
            else:
                messages.append(message.decode())
        return messages

    @pytest.mark.asyncio
    @pytest.mark.parametrize("username", ("Artem\n", "Roma\n", "SomeText\n", "\n"))
    async def test_connect(self, username):
        chat = Chat(self.ip, self.port)
        chat_task = asyncio.create_task(chat.main())
        await asyncio.sleep(0.1)
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        reader_task = asyncio.create_task(self.read_from_reader(reader))
        await asyncio.sleep(0.1)

        writer.write(username.encode())
        await writer.drain()
        await asyncio.sleep(0.1)
        assert username.strip() in chat.users
        reader_task.cancel()
        chat_task.cancel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "username, another_username", (("Artem\n", "Roma\n"), ("Roma\n", "Artem\n"), ("SomeText\n", "txeTemoS\n"))
    )
    async def test_taken_username_connect(self, username, another_username):
        chat = Chat(self.ip, self.port)
        chat_task = asyncio.create_task(chat.main())
        await asyncio.sleep(0.1)
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        reader_task = asyncio.create_task(self.read_from_reader(reader))
        await asyncio.sleep(0.1)

        writer.write(username.encode())
        await writer.drain()
        await asyncio.sleep(0.1)

        reader, writer = await asyncio.open_connection(self.ip, self.port)
        await asyncio.sleep(0.1)
        await reader.readline()
        writer.write(username.encode())
        await writer.drain()
        await asyncio.sleep(0.1)

        assert (await reader.readline()).decode() == f"{username.strip()} already taken. Please select another:\n"

        writer.write(another_username.encode())
        await writer.drain()
        await asyncio.sleep(0.1)
        assert username.strip() in chat.users
        reader_task.cancel()
        chat_task.cancel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("username", ("Artem\n", "Roma\n", "SomeText\n", "\n"))
    async def test_quit_disconnect(self, username):
        chat = Chat(self.ip, self.port)
        chat_task = asyncio.create_task(chat.main())
        await asyncio.sleep(0.1)
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        reader_task = asyncio.create_task(self.read_from_reader(reader))
        await asyncio.sleep(0.1)

        writer.write(username.encode())
        await writer.drain()
        await asyncio.sleep(0.1)
        assert username.strip() in chat.users
        writer.write("QUIT\n".encode())
        await writer.drain()
        await asyncio.sleep(0.1)
        assert username.strip() not in chat.users
        reader_task.cancel()
        chat_task.cancel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("username", ("Artem\n", "Roma\n", "SomeText\n", "\n"))
    async def test_empty_byte_disconnect(self, username):
        chat = Chat(self.ip, self.port)
        chat_task = asyncio.create_task(chat.main())
        await asyncio.sleep(0.1)
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        reader_task = asyncio.create_task(self.read_from_reader(reader))
        await asyncio.sleep(0.1)

        writer.write(username.encode())
        await writer.drain()
        await asyncio.sleep(0.1)
        assert username.strip() in chat.users

        writer.close()
        await writer.wait_closed()
        await asyncio.sleep(0.1)

        assert username.strip() not in chat.users
        reader_task.cancel()
        chat_task.cancel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "users, message", ((("Artem\n", "Roma\n", "SomeText\n"), "Hello\n"), (("1\n", "2\n"), "HI\n"))
    )
    async def test_send_to_everyone(self, users, message):
        ip, host = self.ip, self.port
        chat = Chat(ip, host)
        chat_task = asyncio.create_task(chat.main())
        await asyncio.sleep(0.1)
        readers = []
        for username in users:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
            readers.append(reader)
            await reader.readline()
            await asyncio.sleep(0.1)
            writer.write(username.encode())
            await writer.drain()
            await asyncio.sleep(0.1)
        await chat.send_to_everyone(message)
        for reader in readers:
            reader_message = (await reader.readline()).decode()
            while "connected" in reader_message:
                reader_message = (await reader.readline()).decode()
            assert reader_message == message
        chat_task.cancel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "users, messages, expected_messages",
        (
            (
                ("Artem\n", "Roman\n"),
                (["Hello\n", "Bye\n"], ["Hi\n", "Goodbye\n"]),
                (
                    ["Artem connected\n", "Roman connected\n", "Roman: Hi\n", "Roman: Goodbye\n"],
                    ["Roman connected\n", "Artem: Hello\n", "Artem: Bye\n", "Artem disconnected\n"],
                ),
            ),
            (
                ("User_1\n", "User_2\n"),
                (
                    ["message_1\n", "message_2\n", "message_3\n", "message_4\n"],
                    ["message_5\n", "message_6\n", "message_7\n", "message_8\n"],
                ),
                (
                    [
                        "User_1 connected\n",
                        "User_2 connected\n",
                        "User_2: message_5\n",
                        "User_2: message_6\n",
                        "User_2: message_7\n",
                        "User_2: message_8\n",
                    ],
                    [
                        "User_2 connected\n",
                        "User_1: message_1\n",
                        "User_1: message_2\n",
                        "User_1: message_3\n",
                        "User_1: message_4\n",
                        "User_1 disconnected\n",
                    ],
                ),
            ),
        ),
    )
    async def test_main_scenario(self, users, messages, expected_messages):
        chat = Chat(self.ip, self.port)
        chat_task = asyncio.create_task(chat.main())
        await asyncio.sleep(0.1)

        users_info = {}
        for index in range(len(users)):
            reader, writer = await asyncio.open_connection(self.ip, self.port)
            await reader.readline()
            await asyncio.sleep(0.1)
            reader_task = asyncio.create_task(self.read_from_reader(reader))
            username = users[index]
            users_info[username] = (reader_task, writer)
            writer.write(username.encode())
            await writer.drain()
            await asyncio.sleep(0.1)

        for index in range(len(users)):
            user_messages = messages[index]
            username = users[index]
            writer = users_info[username][1]
            for message in user_messages:
                writer.write(message.encode())
                await writer.drain()
                await asyncio.sleep(0.1)

        for _, writer in users_info.values():
            writer.write("QUIT\n".encode())
            await writer.drain()
            await asyncio.sleep(0.1)

        for index, username in enumerate(users):
            assert users_info[username][0].result() == expected_messages[index]
        chat_task.cancel()
