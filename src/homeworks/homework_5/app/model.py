import abc
import random
from copy import copy
from typing import Optional

from src.homeworks.homework_5.app.observer import Observable


class Player(metaclass=abc.ABCMeta):
    def __init__(self, sign: Optional[str] = None) -> None:
        self.sign = sign

    def set_sign(self, sign: str) -> None:
        self.sign = sign

    @abc.abstractmethod
    def make_move(self, table: list[Observable], coord: Optional[int]) -> None:
        ...


class TicTacToeModel:
    table: list[Observable] = [Observable() for _ in range(9)]
    winner: Observable[str] = Observable()
    x_player: Player
    o_player: Player
    current_player: Observable[Player] = Observable()

    def _check_win(self) -> bool:
        for row in range(3):
            if self.table[row * 3].value == self.table[row * 3 + 1].value == self.table[row * 3 + 2].value is not None:
                return True

        for column in range(3):
            if self.table[column].value == self.table[column + 3].value == self.table[column + 6].value is not None:
                return True

        if self.table[0].value == self.table[4].value == self.table[8].value is not None:
            return True
        if self.table[2].value == self.table[4].value == self.table[6].value is not None:
            return True
        return False

    def _validate_move(self, coord: Optional[int]) -> bool:
        return (coord is None) or (self.table[coord].value is None)

    def restart(self) -> None:
        self.table: list[Observable] = [Observable() for _ in range(9)]
        self.winner: Observable[str] = Observable()
        self.current_player: Observable[Player] = Observable()

    def make_move(self, coord: Optional[int]) -> None:
        if self._validate_move(coord):
            if self.current_player.value:
                self.current_player.value.make_move(self.table, coord)
            else:
                raise ValueError("current player is None")

            # Check winner
            if self._check_win():
                self.winner.value = self.current_player.value.sign
            elif all(obs.value for obs in self.table):
                self.winner.value = "DRAW"

            # Swap players move
            elif self.current_player.value == self.o_player:
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
