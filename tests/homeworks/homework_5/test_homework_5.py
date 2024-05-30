import time
from threading import Thread
from unittest import mock

import pytest

from src.homeworks.homework_5.app.model import *


class TestPlayer:
    @staticmethod
    def table_to_observable(table: list[str]) -> list[Observable]:
        return [Observable(sign) if sign != "" else Observable(None) for sign in table]

    @staticmethod
    def table_to_str(table: list[Observable]) -> list[str]:
        return [obs.value if obs.value else "" for obs in table]


class TestSinglePlayer(TestPlayer):
    @pytest.mark.parametrize(
        "sign,table,coord,expected",
        (
            ("O", ["X", "", "", "", "", "", "", "", ""], 3, ["X", "", "", "O", "", "", "", "", ""]),
            ("X", ["X", "X", "O", "", "", "", "", "", ""], 8, ["X", "X", "O", "", "", "", "", "", "X"]),
            ("X", ["X", "O", "", "", "", "", "", "", ""], 2, ["X", "O", "X", "", "", "", "", "", ""]),
        ),
    )
    def test_make_move(self, sign, table, coord, expected):
        player = SinglePlayer(sign)
        obs_table = self.table_to_observable(table)
        player.make_move(obs_table, coord)
        assert self.table_to_str(obs_table) == expected


class TestBotPlayer(TestPlayer):
    @pytest.mark.parametrize(
        "table,expected",
        (
            (["X", "O", "", "X", "O", "", "X", "", ""], True),
            (["X", "O", "", "X", "O", "", "", "", ""], False),
            (["X", "O", "", "O", "X", "", "", "", "X"], True),
            (["X", "O", "", "", "", "", "", "", ""], False),
            (["X", "X", "X", "O", "O", "", "", "", ""], True),
        ),
    )
    def test_check_win_table(self, table, expected):
        obs_table = self.table_to_observable(table)
        assert BotPlayer._check_win_table([obs.value for obs in obs_table]) == expected

    @pytest.mark.parametrize(
        "sign,table,coord",
        (
            ("O", ["X", "", "", "", "", "", "", "", ""], 3),
            ("X", ["X", "X", "O", "", "", "", "", "", ""], 8),
            ("X", ["X", "O", "", "", "", "", "", "", ""], 2),
        ),
    )
    def test_generate_random(self, sign, table, coord):
        with mock.patch("random.choice", return_value=coord):
            player = BotPlayer(is_strategy=False)
            player.sign = sign
            obs_table = self.table_to_observable(table)
            assert player._generate_bot_move(obs_table) == coord

    @pytest.mark.parametrize(
        "sign,table,expected",
        (
            ("O", ["X", "", "O", "", "X", "", "", "", ""], ["X", "", "O", "", "X", "", "", "", "O"]),
            ("X", ["", "", "O", "", "X", "", "", "", "O"], ["", "", "O", "", "X", "X", "", "", "O"]),
            ("X", ["", "", "O", "", "X", "X", "", "", "O"], ["", "", "O", "X", "X", "X", "", "", "O"]),
            ("X", ["X", "X", "", "O", "O", "", "", "", ""], ["X", "X", "X", "O", "O", "", "", "", ""]),
            ("O", ["", "", "", "X", "X", "O", "", "X", "O"], ["", "", "O", "X", "X", "O", "", "X", "O"]),
        ),
    )
    def test_make_move_strategy(self, sign, table, expected):
        player = BotPlayer(is_strategy=True)
        player.sign = sign
        obs_table = self.table_to_observable(table)
        bot_coord = player._generate_bot_move(obs_table)
        table[bot_coord] = sign
        assert table == expected

    @pytest.mark.parametrize(
        "sign,table,coord,expected",
        (
            ("O", ["X", "", "", "", "", "", "", "", ""], 3, ["X", "", "", "O", "", "", "", "", ""]),
            ("X", ["X", "X", "O", "", "", "", "", "", ""], 8, ["X", "X", "O", "", "", "", "", "", "X"]),
            ("X", ["X", "O", "", "", "", "", "", "", ""], 2, ["X", "O", "X", "", "", "", "", "", ""]),
        ),
    )
    def test_make_move_random(self, sign, table, coord, expected):
        with mock.patch("random.choice", return_value=coord):
            player = BotPlayer(is_strategy=False)
            player.sign = sign
            obs_table = self.table_to_observable(table)
            bot_coord = player._generate_bot_move(obs_table)
            table[bot_coord] = sign
            assert table == expected


class TestTicTacToeModel(TestPlayer):
    @pytest.mark.parametrize(
        "table,coord,expected",
        (
            (["X", "", "", "", "", "", "", "", ""], 3, True),
            (["X", "X", "O", "", "", "", "", "", ""], 8, True),
            (["X", "O", "", "", "", "", "", "", ""], 2, True),
            (["X", "O", "", "", "", "", "", "", ""], 1, False),
        ),
    )
    def test_validate_move(self, table, coord, expected):
        model = TicTacToeModel()
        model.table = self.table_to_observable(table)
        assert model._validate_move(coord) == expected

    @pytest.mark.parametrize(
        "table,expected",
        (
            (["X", "O", "", "X", "O", "", "X", "", ""], "X"),
            (["X", "O", "", "X", "O", "", "", "", ""], None),
            (["X", "O", "", "O", "X", "", "", "", "X"], "X"),
            (["X", "O", "", "", "", "", "", "", ""], None),
            (["X", "X", "X", "O", "O", "", "", "", ""], "X"),
        ),
    )
    def test_check_win(self, table, expected):
        model = TicTacToeModel()
        model.table = self.table_to_observable(table)
        assert model._check_win() == expected

    @pytest.mark.parametrize(
        "sign,table,coord,expected",
        (
            ("O", ["X", "", "", "", "", "", "", "", ""], 3, ["X", "", "", "O", "", "", "", "", ""]),
            ("X", ["X", "X", "O", "", "", "", "", "", ""], 8, ["X", "X", "O", "", "", "", "", "", "X"]),
            ("X", ["X", "O", "", "", "", "", "", "", ""], 2, ["X", "O", "X", "", "", "", "", "", ""]),
        ),
    )
    def test_make_move(self, sign, table, coord, expected):
        model = TicTacToeModel()
        model.table = self.table_to_observable(table)
        model.x_player = SinglePlayer(sign)
        model.o_player = SinglePlayer(sign)
        if sign == "X":
            model.current_player.value = model.x_player
        else:
            model.current_player.value = model.o_player
        model.make_move(coord)
        assert self.table_to_str(model.table) == expected

    @pytest.mark.parametrize(
        "sign,table,coord,expected",
        (
            ("X", ["X", "O", "", "X", "O", "", "", "", ""], 6, "X"),
            ("8", ["X", "O", "X", "X", "O", "X", "O", "X", ""], 8, "DRAW"),
            ("X", ["X", "O", "", "O", "X", "", "", "", ""], 8, "X"),
            ("O", ["O", "X", "X", "O", "", "", "", "", ""], 6, "O"),
        ),
    )
    def test_make_move_winner(self, sign, table, coord, expected):
        model = TicTacToeModel()
        model.table = self.table_to_observable(table)
        model.x_player = SinglePlayer(sign)
        model.o_player = SinglePlayer(sign)
        if sign == "X":
            model.current_player.value = model.x_player
        else:
            model.current_player.value = model.o_player
        model.make_move(coord)
        model.check_win_btn()
        assert model.winner.value == expected

    @pytest.mark.parametrize(
        "sign,table,coord",
        (
            ("O", ["X", "", "", "", "", "", "", "", ""], 3),
            ("X", ["X", "X", "O", "", "", "", "", "", ""], 5),
            ("X", ["X", "O", "", "", "", "", "", "", ""], 6),
        ),
    )
    def test_make_move_exception(self, sign, table, coord):
        model = TicTacToeModel()
        model.table = self.table_to_observable(table)
        model.x_player = SinglePlayer(sign)
        model.o_player = SinglePlayer(sign)
        with pytest.raises(ValueError):
            model.make_move(coord)


class TestMultiPlayer:
    ip = "127.0.0.1"
    port = 8888

    def client_handler(self, conn, addr, get_messages, send_messages):
        for i in range(len(get_messages)):
            assert conn.recv(1024).decode() == get_messages[i]
            conn.sendall(send_messages[i].encode())

    def server_test(self, ip, port, get_messages, send_messages):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind((ip, port))
        sock.listen()
        conn, addr = sock.accept()
        thread = Thread(target=self.client_handler, args=(conn, addr, get_messages, send_messages))
        thread.start()

    @pytest.mark.parametrize(
        "get_messages,send_messages",
        (
            (["command,name,password,sign"], ["access granted"]),
            (["hello,hello,hello,hello"], ["access granted"]),
            (["connect,room,password,X"], ["access granted"]),
        ),
    )
    def test_connect(self, get_messages, send_messages):
        Thread(target=lambda: self.server_test(self.ip, self.port, get_messages, send_messages)).start()
        time.sleep(0.5)
        command, name, password, sign = get_messages[0].split(",")
        player = MultiPlayer([Observable() for _ in range(9)])
        player.connect(self.ip, self.port, command, name, password, sign)

    @pytest.mark.parametrize(
        "get_messages,send_messages",
        ((["connect,name,1,sign"], ["access denied"]), (["command,name,pa1s123sword,sign"], ["access denied"])),
    )
    def test_connect_exception(self, get_messages, send_messages):
        with pytest.raises(ValueError):
            Thread(target=lambda: self.server_test(self.ip, self.port, get_messages, send_messages)).start()
            time.sleep(0.5)
            command, name, password, sign = get_messages[0].split(",")
            player = MultiPlayer([Observable() for _ in range(9)])
            player.connect(self.ip, self.port, command, name, password, sign)

    @pytest.mark.parametrize(
        "coord,sign,expected",
        (
            (
                0,
                "X",
                [
                    "X",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ],
            ),
            (
                8,
                "X",
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "X",
                ],
            ),
            (
                3,
                "O",
                [
                    "",
                    "",
                    "",
                    "O",
                    "",
                    "",
                    "",
                    "",
                    "",
                ],
            ),
        ),
    )
    def test_make_move(self, coord, sign, expected):
        with mock.patch("socket.socket.getsockname", return_value=("127.0.0.1", 1234)):
            message = f"{coord},{sign},1234"
            Thread(target=lambda: self.server_test(self.ip, self.port, [message], [message])).start()
            time.sleep(0.5)

            player = MultiPlayer([Observable() for _ in range(9)])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            player.sock = sock
            player.set_sign(sign)
            sock.connect((self.ip, self.port))
            player.make_move(player.table, coord)
