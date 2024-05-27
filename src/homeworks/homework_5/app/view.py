from tkinter import Tk, ttk


class ModeChoiceView(ttk.Frame):
    GREETINGS = "Hello! Chose TicTacToe game mod"
    SINGLE_LABEL = "SINGLE"
    BOT_LABEL = "BOT"

    def __init__(self) -> None:
        super().__init__()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text=self.GREETINGS)
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.single_btn = ttk.Button(self, text=self.SINGLE_LABEL)
        self.single_btn.grid(row=3, column=1, pady=50, sticky="NSEW")

        self.bot_btn = ttk.Button(self, text=self.BOT_LABEL)
        self.bot_btn.grid(row=4, column=1, pady=50, sticky="NSEW")


class SideChoiceView(ttk.Frame):
    GREETINGS = "Choose your side"

    def __init__(self) -> None:
        super().__init__()

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        self.header = ttk.Label(self, text=self.GREETINGS, anchor="center")
        self.header.grid(row=0, column=0, columnspan=2)

        self.x_btn = ttk.Button(self, text="X")
        self.x_btn.grid(row=1, column=0, padx=25, pady=25, sticky="NSEW")

        self.o_btn = ttk.Button(self, text="O")
        self.o_btn.grid(row=1, column=1, padx=25, pady=25, sticky="NSEW")


class GameView(ttk.Frame):
    def __init__(self) -> None:
        super().__init__()
        self.buttons: list[ttk.Button] = []
        for x in range(1, 4):
            for y in range(1, 4):
                self.grid_columnconfigure(index=y, weight=1)
                self.grid_rowconfigure(index=x, weight=1)
                btn = ttk.Button(self)
                btn.grid(row=x, column=y, sticky="NSEW")
                self.buttons.append(btn)


class CongratulationsView(ttk.Frame):
    CONGRATULATIONS = "SOMEBODY WON!!!"

    def __init__(self) -> None:
        super().__init__()
        self.menu_btn = ttk.Button(self, text="MENU")
        self.congratulations_label = ttk.Label(self, text=self.CONGRATULATIONS, anchor="center")
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.congratulations_label.grid(row=0, column=0, sticky="NSEW")
        self.menu_btn.grid(row=1, column=0, sticky="NSEW", padx=20, pady=20)


class StrategyChoiceView(ttk.Frame):
    GREETINGS = "Choose Bot strategy"
    RANDOM_LABEL = "RANDOM"
    SMART_LABEL = "SMART"

    def __init__(self) -> None:
        super().__init__()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text=self.GREETINGS)
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.random_btn = ttk.Button(self, text=self.RANDOM_LABEL)
        self.random_btn.grid(row=3, column=1, pady=50, sticky="NSEW")

        self.smart_btn = ttk.Button(self, text=self.SMART_LABEL)
        self.smart_btn.grid(row=4, column=1, pady=50, sticky="NSEW")
