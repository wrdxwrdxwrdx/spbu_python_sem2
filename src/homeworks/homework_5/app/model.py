import abc
import random
import socket
from copy import copy
from typing import Optional

from src.homeworks.homework_5.app.observer import Observable


class Player(metaclass=abc.ABCMeta):
    def __init__(self, sign: Optional[str] = None) -> None:
        self.sign = sign

    def set_sign(self, sign: str) -> None:
        self.sign = sign

    @staticmethod
    def _check_win_table(table: list[Optional[str]]) -> bool:
        for row in range(3):
            if table[row * 3] == table[row * 3 + 1] == table[row * 3 + 2] is not None:
                return True

        for column in range(3):
            if table[column] == table[column + 3] == table[column + 6] is not None:
                return True

        if table[0] == table[4] == table[8] is not None:
            return True
        if table[2] == table[4] == table[6] is not None:
            return True
        return False

    @abc.abstractmethod
    def make_move(self, table: list[Observable], coord: Optional[int]) -> None:
        ...


class TicTacToeModel:
    def __init__(self) -> None:
        self.table: list[Observable] = [Observable() for _ in range(9)]
        self.winner: Observable[str] = Observable()
        self.x_player: Optional[Player] = None
        self.o_player: Optional[Player] = None
        self.current_player: Observable[Player] = Observable()
        self.game_is_running: bool = True

    def _check_win(self) -> Optional[str]:
        for row in range(3):
            if self.table[row * 3].value == self.table[row * 3 + 1].value == self.table[row * 3 + 2].value is not None:
                return self.table[row * 3].value

        for column in range(3):
            if self.table[column].value == self.table[column + 3].value == self.table[column + 6].value is not None:
                return self.table[column].value

        if self.table[0].value == self.table[4].value == self.table[8].value is not None:
            return self.table[0].value
        if self.table[2].value == self.table[4].value == self.table[6].value is not None:
            return self.table[2].value

    def check_win_btn(self) -> None:
        if self._check_win():
            self.winner.value = self._check_win()
            self.game_is_running = False
        elif all(obs.value for obs in self.table):
            self.winner.value = "DRAW"
            self.game_is_running = False

    def _validate_move(self, coord: Optional[int]) -> bool:
        return (coord is None) or (self.table[coord].value is None)

    def restart(self) -> None:
        self.table = [Observable() for _ in range(9)]
        self.winner = Observable()
        self.current_player = Observable()
        self.x_player = None
        self.o_player = None
        self.game_is_running = True

    def make_move(self, coord: Optional[int]) -> None:
        if self._validate_move(coord):
            if self.current_player.value:
                self.current_player.value.make_move(self.table, coord)
            else:
                raise ValueError("current player is None")

            if self.current_player.value == self.o_player:
                self.current_player.value = self.x_player
            else:
                self.current_player.value = self.o_player


class SinglePlayer(Player):
    def make_move(self, table: list[Observable], coord: Optional[int]) -> None:
        if coord is not None:
            table[coord].value = self.sign
        else:
            raise ValueError("SinglePlayer's make_move coord must be int, not None")


class BotPlayer(Player):
    def __init__(self, is_strategy: bool = False) -> None:
        super().__init__()
        self.is_strategy = is_strategy

    def _generate_bot_move(self, table: list[Observable]) -> int:
        def _generate_random_move() -> int:
            valid_moves = []
            for index, obs in enumerate(table):
                if obs.value is None:
                    valid_moves.append(index)
            return random.choice(valid_moves)

        if self.is_strategy:
            for coord in range(9):
                if table[coord].value is None:
                    table_copy = copy([obs.value for obs in table])
                    table_copy[coord] = "O" if self.sign == "O" else "X"
                    if self._check_win_table(table_copy):
                        return coord
            for coord in range(9):
                if table[coord].value is None:
                    table_copy = copy([obs.value for obs in table])
                    table_copy[coord] = "X" if self.sign == "O" else "O"
                    if self._check_win_table(table_copy):
                        return coord
        return _generate_random_move()

    def make_move(self, table: list[Observable], coord: Optional[int]) -> None:
        table[self._generate_bot_move(table)].value = self.sign


class MultiPlayer(Player):
    def __init__(self, table: list[Observable], is_my_move: bool = True):
        super().__init__()
        self.table = table
        self.is_my_move = is_my_move
        for obs in table:

            def change_my_move(value: str) -> None:
                self.is_my_move = not self.is_my_move

            obs.add_callback(change_my_move)

    def change_table(self, sock: socket.socket) -> None:
        while True:
            try:
                server_message = (sock.recv(1024)).decode().split(",")
            except Exception as error:
                break
            if len(server_message) == 2:
                coord, sign = server_message
                coord = int(coord)
                self.table[coord].value = sign
                table_str = [obs.value for obs in self.table]
                if self._check_win_table(table_str) or all(table_str):
                    sock.close()
            else:
                raise ValueError("Incorrect info from server, expected (coord,sign)")

    def connect(self, ip: str, port: int, command: str, name: str, password: str, sign: str) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        sock.connect((ip, port))
        sock.sendall(f"{command},{name},{password},{sign}".encode())

        command_status = sock.recv(1024).decode()
        if command_status != "access granted":
            raise ValueError(command_status)

    def start_game(self) -> None:
        my_sign = (self.sock.recv(1024)).decode()
        self.sign = my_sign
        self.is_my_move = my_sign == "X"
        self.change_table(self.sock)

    def make_move(self, table: list[Observable], coord: Optional[int]) -> None:
        if self.is_my_move:
            self.sock.send(f"{coord},{self.sign},{self.sock.getsockname()[1]}".encode())
