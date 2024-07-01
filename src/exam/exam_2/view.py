import asyncio
import tkinter as tk
from tkinter import Tk

from src.exam.exam_2.model import *


class App:
    async def exec(self) -> None:
        self.window = Window()
        await self.window.show()


class Window:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.root = Tk()
        self.root.title("bash")
        self.root.geometry("1200x700")
        self.root.resizable(width=False, height=False)
        self.show_box = tk.Text(self.root, font=("Arial", 14))
        self.show_box.place(x=100, y=25, width=1000, height=500)

    async def button_func(self, command: str) -> None:
        text = await get_info(command)
        self.show_box.delete("1.0", tk.END)
        self.show_box.insert(tk.END, text)

    async def show(self) -> None:
        best_button = tk.Button(self.root, text="BEST", command=lambda: self.loop.create_task(self.button_func("BEST")))
        last_button = tk.Button(self.root, text="LAST", command=lambda: self.loop.create_task(self.button_func("LAST")))
        random_button = tk.Button(
            self.root, text="RANDOM", command=lambda: self.loop.create_task(self.button_func("RANDOM"))
        )

        best_button.place(x=25, y=550, width=350, height=75)
        last_button.place(x=425, y=550, width=350, height=75)
        random_button.place(x=825, y=550, width=350, height=75)

        while True:
            self.root.update()
            await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(App().exec())
