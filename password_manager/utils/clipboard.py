import pyperclip
import threading


def clear():
    pyperclip.copy("")

def copy_to_clipboard(text: str, timeout: int = 20) -> None:
    sanitized_text = "".join(c for c in text if c.isalnum())
    pyperclip.copy(sanitized_text)

    timer = threading.Timer(timeout, clear)
    timer.daemon = True
    timer.start()
