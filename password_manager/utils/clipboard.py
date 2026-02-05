import pyperclip
import threading


def clear():
    pyperclip.copy("")


def copy_to_clipboard(text: str, strip_non_alphanum=False, timeout: int = 20) -> None:
    sanitized_text = text if not strip_non_alphanum else stip_non_alphanum_chars(text)

    pyperclip.copy(sanitized_text)

    clear_clipboard_after_timeout(timeout)

def clear_clipboard_after_timeout(timeout: int) -> None:
    timer = threading.Timer(timeout, clear)
    timer.daemon = True
    timer.start()



def stip_non_alphanum_chars(text: str) -> str:
    return "".join(c for c in text if c.isalnum())
