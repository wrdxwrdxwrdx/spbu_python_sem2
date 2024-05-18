from unittest import mock

import pytest

from src.homeworks.homework_5.app.model import *


class TestSingleModel:
    @staticmethod
    def _set_table(model: SingleModel, new_table: [Optional[str]]):
        if len(new_table) == 9:
            for i in range(9):
                if new_table[i]:
                    model.table[i].value = new_table[i]
                else:
                    model.table[i].value = None

    @staticmethod
    def _get_table(model: SingleModel):
        output = []
        for i in model.table:
            if i.value:
                output.append(i.value)
            else:
                output.append("")
        return output

    @pytest.mark.parametrize(
        "table,coord,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], 2, True),
            (["X", "O", "", "", "", "", "", "", ""], 1, False),
            (["X", "O", "X", "", "", "", "", "", ""], 5, True),
            (["X", "O", "", "", "", "", "X", "", ""], 0, False),
        ),
    )
    def test_validate_move(self, table, coord, expected):
        model = SingleModel()
        self._set_table(model, table)
        assert model._validate_move(coord) == expected

    @pytest.mark.parametrize(
        "table,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], False),
            (["X", "O", "", "", "", "", "", "", ""], False),
            (["X", "X", "X", "", "", "", "", "", ""], True),
            (["X", "O", "O", "O", "O", "", "X", "", ""], False),
            (["X", "O", "O", "O", "O", "O", "X", "", ""], True),
            (["X", "", "X", "X", "", "", "X", "", ""], True),
            (["X", "O", "", "O", "O", "", "X", "O", ""], True),
            (["X", "", "X", "O", "O", "X", "X", "O", "X"], True),
            (["X", "", "", "", "X", "", "", "", "X"], True),
            (["", "", "O", "", "O", "", "O", "", ""], True),
        ),
    )
    def test_check_win(self, table, expected):
        model = SingleModel()
        self._set_table(model, table)
        assert model._check_win() == expected

    @pytest.mark.parametrize(
        "table,player,coord,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], "X", 1, ["X", "O", "", "", "", "", "", "", ""]),
            (["X", "O", "", "", "", "", "", "", ""], "X", 2, ["X", "O", "X", "", "", "", "", "", ""]),
            (["X", "O", "", "", "", "", "", "", ""], "O", 3, ["X", "O", "", "O", "", "", "", "", ""]),
            (["X", "O", "", "", "", "", "", "", ""], "O", 8, ["X", "O", "", "", "", "", "", "", "O"]),
        ),
    )
    def test_make_move(self, table, player, coord, expected):
        model = SingleModel()
        self._set_table(model, table)
        model.current_player.value = player
        model.make_move(coord)
        table = self._get_table(model)
        assert table == expected


class TestBotModel:
    @staticmethod
    def _set_table(model: BotModel, new_table: [Optional[str]]):
        if len(new_table) == 9:
            for i in range(9):
                if new_table[i]:
                    model.table[i].value = new_table[i]
                else:
                    model.table[i].value = None

    @staticmethod
    def _get_table(model: BotModel):
        output = []
        for i in model.table:
            if i.value:
                output.append(i.value)
            else:
                output.append("")
        return output

    @pytest.mark.parametrize(
        "table,coord,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], 2, True),
            (["X", "O", "", "", "", "", "", "", ""], 1, False),
            (["X", "O", "X", "", "", "", "", "", ""], 5, True),
            (["X", "O", "", "", "", "", "X", "", ""], 0, False),
        ),
    )
    def test_validate_move(self, table, coord, expected):
        model = BotModel(is_strategy=False)
        self._set_table(model, table)
        assert model._validate_move(coord) == expected

    @pytest.mark.parametrize(
        "table,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], False),
            (["X", "O", "", "", "", "", "", "", ""], False),
            (["X", "X", "X", "", "", "", "", "", ""], True),
            (["X", "O", "O", "O", "O", "", "X", "", ""], False),
            (["X", "O", "O", "O", "O", "O", "X", "", ""], True),
            (["X", "", "X", "X", "", "", "X", "", ""], True),
            (["X", "O", "", "O", "O", "", "X", "O", ""], True),
            (["X", "", "X", "O", "O", "X", "X", "O", "X"], True),
            (["X", "", "", "", "X", "", "", "", "X"], True),
            (["", "", "O", "", "O", "", "O", "", ""], True),
        ),
    )
    def test_check_win(self, table, expected):
        model = BotModel(is_strategy=False)
        self._set_table(model, table)
        assert model._check_win() == expected

    @pytest.mark.parametrize(
        "table,player,coord,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], "X", 1, ["X", "O", "", "", "", "", "", "", ""]),
            (["X", "O", "", "", "", "", "", "", ""], "X", 2, ["X", "O", "X", "", "", "", "", "", "O"]),
            (["X", "O", "", "", "", "", "", "", ""], "O", 3, ["X", "O", "", "O", "", "", "", "", "X"]),
            (["X", "O", "", "", "", "", "", "", ""], "O", 7, ["X", "O", "", "", "", "", "", "O", "X"]),
        ),
    )
    def test_make_move(self, table, player, coord, expected):
        with mock.patch("random.randint", return_value=8):
            model = BotModel(is_strategy=False)
            self._set_table(model, table)
            model.current_player.value = player
            model.make_move(coord)
            table = self._get_table(model)
            assert table == expected

    @pytest.mark.parametrize(
        "table,player,coord,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], "X", 1, ["X", "O", "", "", "", "", "", "", ""]),
            (["X", "O", "", "", "", "", "", "", ""], "X", 2, ["X", "O", "X", "", "", "", "", "", "O"]),
            (["X", "O", "", "", "", "", "", "", ""], "O", 3, ["X", "O", "", "O", "", "", "", "", "X"]),
            (["X", "", "", "O", "", "", "", "", ""], "X", 1, ["X", "X", "O", "O", "", "", "", "", ""]),
            (["X", "O", "", "O", "", "", "", "", ""], "X", 4, ["X", "O", "", "O", "X", "", "", "", "O"]),
            (["X", "", "O", "", "", "", "", "", ""], "X", 3, ["X", "", "O", "X", "", "", "O", "", ""]),
        ),
    )
    def test_make_move(self, table, player, coord, expected):
        with mock.patch("random.randint", return_value=8):
            model = BotModel(is_strategy=True)
            self._set_table(model, table)
            model.current_player.value = player
            model.make_move(coord)
            table = self._get_table(model)
            assert table == expected

    @pytest.mark.parametrize(
        "table,player,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], "X", ["X", "O", "", "", "", "", "", "", "X"]),
            (["X", "O", "", "", "", "", "", "", ""], "X", ["X", "O", "", "", "", "", "", "", "X"]),
            (["X", "O", "", "", "", "", "", "", ""], "O", ["X", "O", "", "", "", "", "", "", "O"]),
            (["O", "O", "", "X", "X", "", "", "", ""], "X", ["O", "O", "X", "X", "X", "", "", "", ""]),
            (["X", "O", "", "", "X", "", "", "", ""], "O", ["X", "O", "", "", "X", "", "", "", "O"]),
        ),
    )
    def test_make_move_bot_strategy(self, table, player, expected):
        with mock.patch("random.randint", return_value=8):
            model = BotModel(is_strategy=True)
            self._set_table(model, table)
            model.current_player.value = player
            model.make_move_bot()
            table = self._get_table(model)
            assert table == expected

    @pytest.mark.parametrize(
        "table,player,expected",
        (
            (["X", "O", "", "", "", "", "", "", ""], "X", ["X", "O", "", "", "", "", "", "", "X"]),
            (["X", "O", "", "", "", "", "", "", ""], "X", ["X", "O", "", "", "", "", "", "", "X"]),
            (["X", "O", "", "", "", "", "", "", ""], "O", ["X", "O", "", "", "", "", "", "", "O"]),
            (["O", "O", "", "X", "X", "", "", "", ""], "X", ["O", "O", "", "X", "X", "", "", "", "X"]),
            (["X", "O", "", "", "X", "", "", "", ""], "O", ["X", "O", "", "", "X", "", "", "", "O"]),
        ),
    )
    def test_make_move_bot_random(self, table, player, expected):
        with mock.patch("random.randint", return_value=8):
            model = BotModel(is_strategy=False)
            self._set_table(model, table)
            model.current_player.value = player
            model.make_move_bot()
            table = self._get_table(model)
            assert table == expected
