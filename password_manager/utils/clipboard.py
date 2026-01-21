import pyperclip
import threading


def clear():
    pyperclip.copy("")

def copy_to_clipboard(text: str, timeout: int = 20) -> None:
    pyperclip.copy(text)

    threading.Timer(timeout, clear).start()
