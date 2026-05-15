import time
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Label
from textual.containers import Vertical, Horizontal
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

class ConfirmDelete(Screen):
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "no":
            self.app.pop_screen()
            self.app.query_one(Body).check_install_status()
        if event.button.id == "yes":
            shutil.rmtree('./renderE', ignore_errors=True)
            self.app.notify("Deleted renderE")
            self.app.pop_screen()
            self.app.query_one(Body).check_install_status()
    def compose(self) -> ComposeResult:
        with Vertical(id='delete-title'):
            yield Label("Are you sure?")
            yield Label("This will PERMANENTLY delete renderE (will not go to system trash)")

        with Horizontal(id="delete-container"):
            yield Button("YES", id='yes')
            yield Button("NO", id="no")

class UtilsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Utilities", id="utils_title")
        with Vertical(id="utils-container"):
            yield Button("Download renderE", id="download")
            yield Button("Delete renderE", id="delete")
            yield Button("Run Setup", id="setup")
            yield Button("Toggle renderE frame", id="frame_toggle")
            yield Button("Add Music", id="music")
            yield Button("Back", id="back")

    def on_mount(self) -> None:
        self.update_button_visibility()

    def on_screen_resume(self) -> None:
        self.update_button_visibility()

    def update_button_visibility(self) -> None:
        exists = os.path.exists("./renderE")
        
        self.query_one("#download", Button).display = not exists
        self.query_one("#delete", Button).display = exists

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "download":
            try:
                subprocess.run(["git", "clone", "https://github.com/LeWolfYT/renderE"])
                time.sleep(0.5)
                try:
                    self.update_button_visibility()
                except Exception:
                    pass
                self.app.refresh()
            except subprocess.CalledProcessError as e:
                pass

        if event.button.id == "frame_toggle":
            file_path = "./renderE/main.py"
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            target = "rl.set_config_flags(rl.ConfigFlags.FLAG_WINDOW_UNDECORATED)"
            commented = f"#{target}"

            if commented in content:
                content = content.replace(commented, target)
                self.notify("Window frame: DISABLED")
            elif target in content:
                content = content.replace(target, commented)
                self.notify("Window frame: ENABLED")
            else:
                self.notify("Could not find configuration line", severity="warning")
                return
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

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
            self.app.query_one(Body).check_install_status()

        if event.button.id == "music":
            music_path = select_file()
            if not os.path.exists("./renderE/bgm"):
                os.makedirs("./renderE/bgm")
            try:
                shutil.copy2(music_path, "./renderE/bgm")
            except: 
                pass

        if event.button.id == "delete":
            self.app.push_screen(ConfirmDelete())


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

    def on_mount(self) -> None:
        self.check_install_status()

    def check_install_status(self) -> None:
        try:
            run_bttn = self.query_one("#run", Button)
            if os.path.exists("./renderE"):
                run_bttn.label = "Run renderE"
                run_bttn.disabled = False
            else:
                run_bttn.label = "renderE not installed"
                run_bttn.disabled = True
        except:
            pass

class Helper(App):

    def compose(self):
        yield Label(id="title", content="renderE Helper")
        yield Body()


    CSS_PATH = "./style.css"

if __name__ == "__main__":
    Helper().run()
