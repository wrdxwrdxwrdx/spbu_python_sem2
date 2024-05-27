import abc
import asyncio
import time
from functools import partial
from tkinter import Tk, ttk
from typing import Callable, Optional

from model import BotPlayer, Player, SinglePlayer, TicTacToeModel
from view import CongratulationsView, GameView, ModeChoiceView, SideChoiceView, StrategyChoiceView

loop = asyncio.new_event_loop()


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: TicTacToeModel):
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, root: Tk) -> None:
        self.loop = asyncio.new_event_loop()
        self._model: TicTacToeModel = TicTacToeModel()
        self._root = root
        self._viewmodels: dict[str, IViewModel] = {
            "ModeChoice": ModeChoiceViewModel(self._model),
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
                lambda value: asyncio.get_event_loop().create_task(self._model.make_move(None))
                if isinstance(value, BotPlayer)
                else ...
            )
            view_model.switch(
                "StrategyChoice", {"ViewModel": view_model, "me": SinglePlayer(), "opponent": BotPlayer()}
            )

        view.single_btn.config(command=single_btn_cmd)
        view.bot_btn.config(command=bot_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        frame = ModeChoiceView()
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
        def create_callback_func(coord: int) -> Callable:
            return lambda value: view.buttons[coord].config(text=value)

        def player_move(coord: int) -> None:
            if self._model.current_player.value:
                asyncio.run(self._model.make_move(coord))

        for coord in range(len(view.buttons)):
            self._model.table[coord].add_callback(create_callback_func(coord))
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
        return frame
