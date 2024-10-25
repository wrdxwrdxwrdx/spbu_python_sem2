import abc
from functools import partial
from threading import Thread
from tkinter import Tk, ttk
from typing import Callable, Optional

from src.homeworks.TicTacToe.app.model import BotPlayer, MultiPlayer, Player, SinglePlayer, TicTacToeModel
from src.homeworks.TicTacToe.app.view import (
    CongratulationsView,
    GameView,
    ModeChoiceView,
    RoomChoiceView,
    SideChoiceView,
    StrategyChoiceView,
)


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: TicTacToeModel):
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, root: Tk) -> None:
        self._model: TicTacToeModel = TicTacToeModel()
        self._root = root
        self._viewmodels: dict[str, IViewModel] = {
            "ModeChoice": ModeChoiceViewModel(self._model),
            "RoomChoice": RoomChoiceViewModel(self._model),
            "StrategyChoice": StrategyChoiceViewModel(self._model),
            "SideChoice": SideChoiceViewModel(self._model),
            "Game": GameViewModel(self._model),
            "Congratulations": CongratulationsViewModel(self._model),
        }

        self._current_view: Optional[ttk.Frame] = None

    def switch(self, name: str, data: dict) -> None:
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self) -> None:
        self.switch("ModeChoice", {"ViewModel": self})


class ModeChoiceViewModel(IViewModel):
    def _bind(self, view: ModeChoiceView, view_model: ViewModel) -> None:
        def single_btn_cmd() -> None:
            self._model.x_player = SinglePlayer("X")
            self._model.o_player = SinglePlayer("O")
            view_model.switch("Game", {"ViewModel": view_model})

        def bot_btn_cmd() -> None:
            self._model.current_player.add_callback(
                lambda value: self._model.make_move(None)
                if isinstance(value, BotPlayer) and self._model.game_is_running
                else ...
            )
            view_model.switch(
                "StrategyChoice", {"ViewModel": view_model, "me": SinglePlayer(), "opponent": BotPlayer()}
            )

        def multi_btn_cmd() -> None:
            view_model.switch("RoomChoice", {"ViewModel": view_model})

        view.single_btn.config(command=single_btn_cmd)
        view.bot_btn.config(command=bot_btn_cmd)
        view.multi_btn.config(command=multi_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        frame = ModeChoiceView()
        self._bind(frame, data["ViewModel"])
        return frame


class RoomChoiceViewModel(IViewModel):
    def _bind(self, view: RoomChoiceView, view_model: ViewModel) -> None:
        self.sign = "X"

        def x_btn_cmd() -> None:
            self.sign = "X"

        def o_btn_cmd() -> None:
            self.sign = "O"

        def get_user_input() -> tuple[str, int, str, str]:
            ip, port = view.ip_entry.get().split(":")
            ip = str(ip)
            port = int(port)
            name = str(view.room_name_entry.get())
            password = str(view.room_password_entry.get())
            return ip, port, name, password

        def create_btn_cmd() -> None:
            def create() -> None:
                try:
                    player.connect(ip, port, "create", name, password, self.sign)
                    view_model.switch("Game", {"ViewModel": view_model})
                    self._model.current_player.value = self._model.o_player
                    player.start_game()
                except ValueError as error:
                    view.error_label.config(text=str(error))

            ip, port, name, password = get_user_input()
            player = MultiPlayer(self._model.table)
            self._model.x_player = player
            self._model.o_player = player

            Thread(target=create).start()

        def connect_btn_cmd() -> None:
            def connect() -> None:
                try:
                    player.connect(ip, port, "connect", name, password, self.sign)
                    view_model.switch("Game", {"ViewModel": view_model})
                    self._model.current_player.value = self._model.o_player
                    player.start_game()
                except ValueError as error:
                    view.error_label.config(text=str(error))

            ip, port, name, password = get_user_input()
            player = MultiPlayer(self._model.table)
            self._model.x_player = player
            self._model.o_player = player

            Thread(target=connect).start()

        view.x_btn.config(command=x_btn_cmd)
        view.o_btn.config(command=o_btn_cmd)
        view.create_btn.config(command=create_btn_cmd)
        view.connect_btn.config(command=connect_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        frame = RoomChoiceView()
        self._bind(frame, data["ViewModel"])
        return frame


class StrategyChoiceViewModel(IViewModel):
    def _bind(self, view: StrategyChoiceView, view_model: ViewModel, bot: BotPlayer, me: Player) -> None:
        def random_btn_cmd() -> None:
            bot.is_strategy = False
            view_model.switch(
                "SideChoice",
                {"me": me, "opponent": bot, "ViewModel": view_model},
            )

        def smart_btn_cmd() -> None:
            bot.is_strategy = True
            view_model.switch(
                "SideChoice",
                {"me": me, "opponent": bot, "ViewModel": view_model},
            )

        view.random_btn.config(command=random_btn_cmd)
        view.smart_btn.config(command=smart_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        if "opponent" not in data:
            raise RuntimeError("opponent must be in data")
        if "me" not in data:
            raise RuntimeError("me must be in data")
        frame = StrategyChoiceView()
        self._bind(frame, data["ViewModel"], data["opponent"], data["me"])
        return frame


class SideChoiceViewModel(IViewModel):
    def _bind(self, view: SideChoiceView, me: Player, opponent: Player, view_model: ViewModel) -> None:
        def x_btn_cmd() -> None:
            me.set_sign("X")
            opponent.set_sign("O")
            self._model.x_player = me
            self._model.o_player = opponent
            view_model.switch("Game", {"ViewModel": view_model})

        def o_btn_cmd() -> None:
            me.set_sign("O")
            opponent.set_sign("X")
            self._model.x_player = opponent
            self._model.o_player = me
            view_model.switch("Game", {"ViewModel": view_model})

        view.x_btn.config(command=x_btn_cmd)
        view.o_btn.config(command=o_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "opponent" not in data:
            raise RuntimeError("opponent must be in data")
        if "me" not in data:
            raise RuntimeError("me must be in data")
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        frame = SideChoiceView()
        self._bind(frame, data["me"], data["opponent"], data["ViewModel"])
        return frame


class GameViewModel(IViewModel):
    def _bind(self, view: GameView, view_model: ViewModel) -> None:
        def change_button_text(coord: int) -> Callable:
            return lambda value: view.buttons[coord].config(text=value)

        def player_move(coord: int) -> None:
            if self._model.current_player.value:
                self._model.make_move(coord)

        for coord in range(len(view.buttons)):
            self._model.table[coord].add_callback(change_button_text(coord))
            self._model.table[coord].add_callback(lambda _: self._model.check_win_btn())
            btn = view.buttons[coord]
            btn.config(command=partial(player_move, coord))

        self._model.winner.add_callback(
            lambda winner: view_model.switch("Congratulations", {"winner": winner, "ViewModel": view_model})
        )

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise KeyError("No ViewModel in data")
        frame = GameView()
        self._bind(frame, data["ViewModel"])
        self._model.current_player.value = self._model.x_player
        return frame


class CongratulationsViewModel(IViewModel):
    def _bind(self, view: CongratulationsView, view_model: ViewModel, winner: str) -> None:
        def menu_btn_func() -> None:
            self._model.restart()
            view_model.switch("ModeChoice", {"ViewModel": view_model})

        if winner != "DRAW":
            view.congratulations_label.config(text=f"{winner} WON!!!")
        else:
            view.congratulations_label.config(text="DRAW!!!")

        view.menu_btn.config(command=menu_btn_func)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "winner" not in data:
            raise KeyError("No winner in data")
        if "ViewModel" not in data:
            raise KeyError("No ViewModel in data")
        frame = CongratulationsView()
        self._bind(frame, data["ViewModel"], data["winner"])
        if self._model.o_player:
            self._model.o_player.end_game()
        if self._model.x_player:
            self._model.x_player.end_game()
        return frame
