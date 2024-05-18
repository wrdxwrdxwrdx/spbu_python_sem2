import abc
from functools import partial
from tkinter import Tk, ttk
from typing import Callable, Optional

from model import BotModel, SingleModel, TicTacToeModel
from view import CongratulationsView, GameView, ModeChoiceView, SideChoiceView, StrategyChoiceView


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: Optional[TicTacToeModel]):
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, root: Tk) -> None:
        self._model: Optional[TicTacToeModel] = None
        self._root = root

        self._viewmodels: dict[str, IViewModel] = {
            "ModeChoice": ModeChoiceViewModel(self._model),
            "StrategyChoice": StrategyChoiceViewModel(None),
        }

        self._current_view: Optional[ttk.Frame] = None

    def set_model(self, model: Optional[TicTacToeModel], viewmodels: dict[str, IViewModel]) -> None:
        self._model = model
        self._viewmodels = viewmodels

    def switch(self, name: str, data: dict) -> None:
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self) -> None:
        self.switch("ModeChoice", {"ViewModel": self})


class GameViewModel(IViewModel):
    _model: SingleModel

    def _bind(self, view: GameView, view_model: ViewModel) -> None:
        def create_callback_func(coord: int) -> Callable:
            return lambda value: view.buttons[coord].config(text=value)

        for coord in range(len(view.buttons)):
            f = create_callback_func(coord)
            self._model.table[coord].add_callback(f)
            func = partial(self._model.make_move, coord)
            btn = view.buttons[coord]
            btn.config(command=func)

        if len(self._model.winner.callbacks) == 0:
            self._model.winner.add_callback(
                lambda winner: view_model.switch("Congratulations", {"winner": winner, "ViewModel": view_model})
            )

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise KeyError("No ViewModel in data")
        frame = GameView()
        self._bind(frame, data["ViewModel"])
        return frame


class CongratulationsViewModel(IViewModel):
    def _bind(self, view: CongratulationsView, view_model: ViewModel, winner: str) -> None:
        def menu_btn_func() -> None:
            if self._model:
                self._model.winner.value = None

            view_model.set_model(
                None,
                {
                    "ModeChoice": ModeChoiceViewModel(None),
                    "StrategyChoice": StrategyChoiceViewModel(None),
                },
            )
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


class StrategyChoiceViewModel(IViewModel):
    def _bind(self, view: StrategyChoiceView, view_model: ViewModel) -> None:
        def random_btn_cmd() -> None:
            model = BotModel(is_strategy=False)
            callback = model.current_player.add_callback(lambda _: view_model.switch("Game", {"ViewModel": view_model}))
            viewmodels = {
                "ModeChoice": self,
                "StrategyChoice": StrategyChoiceViewModel(model),
                "SideChoice": SideChoiceViewModel(model),
                "Game": GameViewModel(model),
                "Congratulations": CongratulationsViewModel(model),
            }
            view_model.set_model(model, viewmodels)
            view_model.switch(
                "SideChoice",
                {
                    "callback": callback,
                },
            )

        def smart_btn_cmd() -> None:
            model = BotModel(is_strategy=True)
            callback = model.current_player.add_callback(lambda _: view_model.switch("Game", {"ViewModel": view_model}))
            viewmodels = {
                "ModeChoice": self,
                "StrategyChoice": StrategyChoiceViewModel(model),
                "SideChoice": SideChoiceViewModel(model),
                "Game": GameViewModel(model),
                "Congratulations": CongratulationsViewModel(model),
            }
            view_model.set_model(model, viewmodels)
            view_model.switch(
                "SideChoice",
                {
                    "callback": callback,
                },
            )

        view.random_btn.config(command=random_btn_cmd)
        view.smart_btn.config(command=smart_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        frame = StrategyChoiceView()
        self._bind(frame, data["ViewModel"])
        return frame


class ModeChoiceViewModel(IViewModel):
    def _bind(self, view: ModeChoiceView, view_model: ViewModel) -> None:
        def single_btn_cmd() -> None:
            model = SingleModel()
            callback = model.current_player.add_callback(lambda _: view_model.switch("Game", {"ViewModel": view_model}))
            viewmodels = {
                "ModeChoice": self,
                "SideChoice": SideChoiceViewModel(model),
                "Game": GameViewModel(model),
                "Congratulations": CongratulationsViewModel(model),
            }
            view_model.set_model(model, viewmodels)
            view_model.switch("SideChoice", {"callback": callback})

        def bot_btn_cmd() -> None:
            view_model.switch("StrategyChoice", {"ViewModel": view_model})

        view.single_btn.config(command=single_btn_cmd)
        view.bot_btn.config(command=bot_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        if "ViewModel" not in data:
            raise RuntimeError("ViewModel must be in data")
        frame = ModeChoiceView()
        self._bind(frame, data["ViewModel"])
        return frame


class SideChoiceViewModel(IViewModel):
    def _bind(self, view: SideChoiceView, callback: Callable) -> None:
        def x_btn_cmd() -> None:
            if self._model:
                self._model.set_player("X")
            callback()

        def o_btn_cmd() -> None:
            if self._model:
                self._model.set_player("O")
            callback()

        view.x_btn.config(command=x_btn_cmd)
        view.o_btn.config(command=o_btn_cmd)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = SideChoiceView()
        self._bind(frame, data["callback"])
        return frame
