from tkinter import Tk
from tkinter import font as tkFont
from tkinter import ttk


class ModeChoiceView(ttk.Frame):
    GREETINGS = "Hello! Chose TicTacToe game mod"
    SINGLE_LABEL = "SINGLE"
    BOT_LABEL = "BOT"
    MULTI_LABEL = "MULTIPLAYER"

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

        self.multi_btn = ttk.Button(self, text=self.MULTI_LABEL)
        self.multi_btn.grid(row=5, column=1, pady=50, sticky="NSEW")


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


class RoomChoiceView(ttk.Frame):
    IP_LABEL = "Enter server Ip"
    ROOM_NAME = "Enter room name"
    ROOM_PASSWORD = "Enter room password"
    IP = "127.0.0.1:8888"

    def __init__(self) -> None:
        super().__init__()
        label_font = tkFont.Font(family="Helvetica", size=20)
        entry_font = tkFont.Font(family="Helvetica", size=30)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.ip_label = ttk.Label(self, text=self.IP_LABEL, font=label_font)
        self.ip_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.ip_entry = ttk.Entry(self, justify="center", font=entry_font)
        self.ip_entry.insert(0, self.IP)
        self.ip_entry.grid(row=2, column=0, columnspan=2, pady=15, sticky="NSEW")

        self.room_name_label = ttk.Label(self, text=self.ROOM_NAME, font=label_font, justify="center")
        self.room_name_entry = ttk.Entry(self, justify="center", font=entry_font)
        self.room_name_label.grid(row=3, column=0, columnspan=2)
        self.room_name_entry.grid(row=4, column=0, columnspan=2, pady=15, sticky="NSEW")

        self.room_password_label = ttk.Label(self, text=self.ROOM_PASSWORD, font=label_font, justify="center")
        self.room_password_entry = ttk.Entry(self, justify="center", font=entry_font)
        self.room_password_label.grid(row=5, column=0, columnspan=2)
        self.room_password_entry.grid(row=6, column=0, columnspan=2, pady=15, sticky="NSEW")

        self.x_btn = ttk.Button(self, text="X")
        self.x_btn.grid(row=8, column=0, pady=15, padx=50, sticky="NSEW")

        self.o_btn = ttk.Button(self, text="O")
        self.o_btn.grid(row=8, column=1, pady=15, padx=50, sticky="NSEW")

        self.create_btn = ttk.Button(self, text="Create")
        self.create_btn.grid(row=9, column=0, padx=15, sticky="NSEW")

        self.connect_btn = ttk.Button(self, text="Connect")
        self.connect_btn.grid(row=9, column=1, padx=15, sticky="NSEW")
