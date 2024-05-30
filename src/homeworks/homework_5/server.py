import socket
import time
from threading import Thread
from typing import Any, Optional

from loguru import logger


class Room:
    def __init__(self, room_name: str, password: str) -> None:
        self.room_name = room_name
        self.password = password
        self.x_player: Optional[list[socket.socket, Any]] = None
        self.o_player: Optional[list[socket.socket, Any]] = None
        self.current_player: Optional[list[socket.socket, Any]] = None

    def change_current_player(self):
        if self.current_player == self.x_player:
            self.current_player = self.o_player
        elif self.current_player == self.o_player:
            self.current_player = self.x_player
        else:
            raise ValueError("Unexpected current player in room ")

    def send_back(self, data: bytes) -> None:
        command = data.decode()
        coord, sign, port = command.split(",")
        if port == str(self.current_player[1][1]):
            self.x_player[0].send(f"{coord},{sign}".encode())
            self.o_player[0].send(f"{coord},{sign}".encode())
            self.change_current_player()

    def start(self, conn: socket.socket, addr: Any) -> None:
        if self.x_player and self.o_player:
            self.current_player: list[socket.socket, Any] = self.x_player
            while True:
                data = self.current_player[0].recv(1024)
                if data:
                    self.send_back(data)
                else:
                    self.x_player[0].close()
                    self.o_player[0].close()
                    logger.info(f"{addr} has been disconnected")
                    break
        else:
            raise ValueError("room started without player")


class Sever:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port
        self.rooms: dict[str, Room] = dict()

    def create(self, conn: socket.socket, addr: Any, room_name: str, password: str, sign: str) -> str:
        if room_name not in self.rooms:
            self.rooms[room_name] = Room(room_name, password)
            room = self.rooms[room_name]
            if sign == "X":
                room.x_player = [conn, addr]
            else:
                room.o_player = [conn, addr]
            logger.info(f"room {room_name} with password {password} was created by {addr}")
            conn.send("access granted".encode())
            return room_name
        else:
            conn.send("access denied".encode())
            raise ValueError("Room already created")

    def connect(self, conn: socket.socket, addr: Any, room_name: str, password: str) -> str:
        if room_name in self.rooms:
            if password == self.rooms[room_name].password:
                room = self.rooms[room_name]
                if room.x_player is None:
                    room.x_player = [conn, addr]
                    logger.info(f"{addr} connected to room {room_name}")
                    conn.send("access granted".encode())
                    return room_name
                elif room.o_player is None:
                    room.o_player = [conn, addr]
                    logger.info(f"{addr} connected to room {room_name}")
                    conn.send("access granted".encode())
                    return room_name
                else:
                    conn.send("access denied".encode())
                    raise ValueError("Room is full")
            else:
                conn.send("access denied".encode())
                raise ValueError("Incorrect password")
        else:
            conn.send("access denied".encode())
            raise ValueError(f"No room with name {room_name}")

    def room_handler(self, conn: socket.socket, addr: Any) -> str:
        full_command = conn.recv(1024).decode().split(",")
        if len(full_command) != 4:
            raise ValueError("Incorrect input from reader about room, expected type: command,name,password,sign")
        else:
            command, room_name, password, sign = full_command
            if command == "create":
                return self.create(conn, addr, room_name, password, sign)
            elif command == "connect":
                return self.connect(conn, addr, room_name, password)
            else:
                conn.send("access denied".encode())
                ValueError("Unexpected room command")

    def client_handler(self, conn: socket.socket, addr: Any) -> None:
        room_name = self.room_handler(conn, addr)
        room = self.rooms[room_name]
        while (room.o_player is None) or (room.x_player is None):
            time.sleep(0)
        logger.info(f"Room {room_name} completed, game started for {addr}")
        if room.o_player == [conn, addr]:
            conn.sendall("O".encode())
        if room.x_player == [conn, addr]:
            conn.sendall("X".encode())
        logger.info(f"Message about side sent to {addr}")
        room.start(conn, addr)
        if room_name in self.rooms:
            del self.rooms[room_name]
            logger.info(f"room {room_name} was closed")

    def main(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        logger.info(f"Server started at {self.ip}:{self.port}")
        sock.bind((self.ip, self.port))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            logger.info(f"Connected from {addr}")
            thread = Thread(target=self.client_handler, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    server = Sever("127.0.0.1", 8888)
    server.main()
