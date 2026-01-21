import pyperclip
import threading


def clear():
    pyperclip.copy("")

def copy_to_clipboard(text: str, timeout: int = 60) -> None:
    pyperclip.copy(text)

    threading.Timer(timeout, clear).start()
