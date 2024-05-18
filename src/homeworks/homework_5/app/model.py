import abc
import random
from copy import copy
from typing import Optional

from src.homeworks.homework_5.app.observer import Observable


class TicTacToeModel(metaclass=abc.ABCMeta):
    current_player: Observable = Observable[str]()
    winner: Observable = Observable[str]()

    def __init__(self) -> None:
        self.table: list[Observable[str]] = [Observable[str]() for _ in range(9)]

    @abc.abstractmethod
    def _validate_move(self, coord: int) -> bool:
        pass

    @abc.abstractmethod
    def _check_win(self) -> bool:
        pass

    def set_player(self, player_sign: str) -> None:
        if player_sign != "X" and player_sign != "O":
            raise ValueError(f"player sign must be X/O, not {player_sign}")
        self.current_player.value = player_sign


class SingleModel(TicTacToeModel):
    def _validate_move(self, coord: int) -> bool:
        return self.table[coord].value is None

    def _check_win(self) -> bool:
        # row
        for row in range(3):
            if self.table[row * 3].value == self.table[row * 3 + 1].value == self.table[row * 3 + 2].value is not None:
                return True

        # column
        for column in range(3):
            if self.table[column].value == self.table[column + 3].value == self.table[column + 6].value is not None:
                return True

        # diagonal
        if self.table[0].value == self.table[4].value == self.table[8].value is not None:
            return True
        if self.table[2].value == self.table[4].value == self.table[6].value is not None:
            return True
        return False

    def make_move(self, coord: int) -> None:
        if self._validate_move(coord):
            self.table[coord].value = self.current_player.value
            if self._check_win():
                self.winner.value = self.current_player.value
            elif all(obs.value for obs in self.table):
                self.winner.value = "DRAW"
            elif self.current_player.value == "X":
                self.current_player.value = "O"
            else:
                self.current_player.value = "X"


class BotModel(TicTacToeModel):
    def __init__(self, is_strategy: bool = False) -> None:
        super().__init__()
        self.is_strategy = is_strategy

    def _validate_move(self, coord: int) -> bool:
        return self.table[coord].value is None

    def _check_win(self) -> bool:
        # row
        for row in range(3):
            if self.table[row * 3].value == self.table[row * 3 + 1].value == self.table[row * 3 + 2].value is not None:
                return True

        # column
        for column in range(3):
            if self.table[column].value == self.table[column + 3].value == self.table[column + 6].value is not None:
                return True

        # diagonal
        if self.table[0].value == self.table[4].value == self.table[8].value is not None:
            return True
        if self.table[2].value == self.table[4].value == self.table[6].value is not None:
            return True
        return False

    def make_move(self, coord: int) -> None:
        if self._validate_move(coord):
            self.table[coord].value = self.current_player.value
            if self._check_win():
                self.winner.value = self.current_player.value
            elif all(obs.value for obs in self.table):
                self.winner.value = "DRAW"
            elif self.current_player.value == "X":
                self.current_player.value = "O"
            else:
                self.current_player.value = "X"
            if self.winner.value is None:
                self.make_move_bot()

    def _generate_bot_move(self, table: list[Optional[str]]) -> int:
        def _check_win_table(table: list[Optional[str]]) -> bool:
            # row
            for row in range(3):
                if table[row * 3] == table[row * 3 + 1] == table[row * 3 + 2] is not None:
                    return True

            # column
            for column in range(3):
                if table[column] == table[column + 3] == table[column + 6] is not None:
                    return True

            # diagonal
            if table[0] == table[4] == table[8] is not None:
                return True
            if table[2] == table[4] == table[6] is not None:
                return True
            return False

        def _generate_random_move() -> int:
            coord = random.randint(0, 8)
            while not self._validate_move(coord):
                print(coord)
                coord = random.randint(0, 8)
            return coord

        if self.is_strategy:
            for coord in range(9):
                if table[coord] is None:
                    table_copy = copy(table)
                    table_copy[coord] = "X" if self.current_player.value == "O" else "O"
                    if _check_win_table(table_copy):
                        return coord
        return _generate_random_move()

    def make_move_bot(self) -> None:
        coord = self._generate_bot_move([obs.value for obs in self.table])

        self.table[coord].value = self.current_player.value
        if self._check_win():
            self.winner.value = self.current_player.value
        elif all(obs.value for obs in self.table):
            self.winner.value = "DRAW"
        elif self.current_player.value == "X":
            self.current_player.value = "O"
        else:
            self.current_player.value = "X"
