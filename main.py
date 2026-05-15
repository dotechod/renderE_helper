import time
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Label
from textual.containers import Vertical
from textual.screen import Screen

import subprocess

import tkinter as tk
from tkinter import filedialog
import os
import shutil

def select_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select music"
    )

    root.destroy()
    return file_path

class UtilsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Utilities", id="utils_title")
        with Vertical(id="menu-container"):
            yield Button("Download renderE", id="download")
            yield Button("Run Setup", id="setup")
            yield Button("Add Music", id="music")
            yield Button("Back", id="back", variant="error")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "download":
            try:
                subprocess.run(["git", "clone", "https://github.com/LeWolfYT/renderE"])
                time.sleep(0.5)
                self.app.refresh()
            except subprocess.CalledProcessError as e:
                pass
        if event.button.id == "setup":
            with self.app.suspend():
                import sys
                subfolder_path = os.path.abspath("./renderE")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "./renderE/requirements.txt"])
                env = os.environ.copy()
                env["PYTHONPATH"] = subfolder_path + os.pathsep + env.get("PYTHONPATH", "")
                subprocess.run([sys.executable, "setup.py"], cwd=subfolder_path, env=env)
        if event.button.id == "back":
            self.app.pop_screen()
        if event.button.id == "music":
            music_path = select_file()
            if not os.path.exists("./renderE/bgm"):
                os.makedirs("./renderE/bgm")
            try:
                shutil.copy2(music_path, "./renderE/bgm")
            except:
                pass


class Body(Static):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "exit":
            self.app.exit()
        if button_id == "utils":
            self.app.push_screen(UtilsScreen())
        if button_id == "run":
            with self.app.suspend():
                import sys
                subfolder_path = os.path.abspath("./renderE")
                env = os.environ.copy()
                env["PYTHONPATH"] = subfolder_path + os.pathsep + env.get("PYTHONPATH", "")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "./renderE/requirements.txt"])
                subprocess.Popen([sys.executable, "lot8sloop.py"], cwd=subfolder_path, env=env)
                subprocess.run([sys.executable, "main.py"], cwd=subfolder_path, env=env)


    def compose(self):
        with Vertical(id="main-container"):
            yield Button(id="run", flat=True, label="Run renderE")
            yield Button(id="utils", flat=True, label="Utilities")
            yield Button(id="exit", flat=True, label="Exit")

class Helper(App):

    def compose(self):
        yield Label(id="title", content="renderE Helper")
        yield Body()


    CSS_PATH = "./style.css"

if __name__ == "__main__":
    Helper().run()