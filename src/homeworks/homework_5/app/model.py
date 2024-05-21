import abc
import random
from copy import copy
from typing import Optional

from src.homeworks.homework_5.app.observer import Observable


class TicTacToeModel:
    current_player: Observable = Observable[str]()
    winner: Observable = Observable[str]()

    def __init__(self) -> None:
        self.table: list[Observable[str]] = [Observable[str]() for _ in range(9)]

    @staticmethod
    async def _check_win_table(table: list[Optional[str]]) -> bool:
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

    def _validate_move(self, coord: int) -> bool:
        return self.table[coord].value is None

    async def _check_win(self) -> bool:
        table = [obs.value for obs in self.table]
        return await self._check_win_table(table)

    async def set_player(self, player_sign: str) -> None:
        if player_sign != "X" and player_sign != "O":
            raise ValueError(f"player sign must be X/O, not {player_sign}")
        self.current_player.value = player_sign


class SingleModel(TicTacToeModel):
    async def make_move(self, coord: int) -> None:
        if self._validate_move(coord):
            self.table[coord].value = self.current_player.value
            if await self._check_win():
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

    async def make_move(self, coord: int) -> None:
        if self._validate_move(coord):
            self.table[coord].value = self.current_player.value
            if await self._check_win():
                self.winner.value = self.current_player.value
            elif all(obs.value for obs in self.table):
                self.winner.value = "DRAW"
            elif self.current_player.value == "X":
                self.current_player.value = "O"
            else:
                self.current_player.value = "X"
            if self.winner.value is None:
                await self.make_move_bot()

    async def _generate_bot_move(self, table: list[Optional[str]]) -> int:
        def _generate_random_move() -> int:
            coord = random.randint(0, 8)
            while not self._validate_move(coord):
                coord = random.randint(0, 8)
            return coord

        if self.is_strategy:
            for coord in range(9):
                if table[coord] is None:
                    table_copy = copy(table)
                    table_copy[coord] = "X" if self.current_player.value == "O" else "O"
                    if await self._check_win_table(table_copy):
                        return coord
        return _generate_random_move()

    async def make_move_bot(self) -> None:
        coord = await self._generate_bot_move([obs.value for obs in self.table])

        self.table[coord].value = self.current_player.value
        if await self._check_win():
            self.winner.value = self.current_player.value
        elif all(obs.value for obs in self.table):
            self.winner.value = "DRAW"
        elif self.current_player.value == "X":
            self.current_player.value = "O"
        else:
            self.current_player.value = "X"
