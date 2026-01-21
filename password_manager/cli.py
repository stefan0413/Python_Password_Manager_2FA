import io

from qrcode.main import QRCode
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from prompt_toolkit import ANSI
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, FormattedTextControl
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, TextArea
from rich.text import Text

from password_manager.utils.clipboard import copy_to_clipboard


console = Console()

class Menu:
    def __init__(self, title: str, subtitle: str, items: list[str]):
        self.title = title
        self.subtitle = subtitle
        self.items = items
        self.selected = 0
        self.result: str | None = None

    def _render(self) -> str:
        table = Table.grid(padding=1)

        for index, item in enumerate(self.items):
            if index == self.selected:
                table.add_row(f"[black on cyan]▶ {item}[/]")
            else:
                table.add_row(f"  {item}")

        panel = Panel(
            table,
            title=self.title,
            subtitle=self.subtitle,
            border_style="cyan",
        )

        with console.capture() as capture:
            console.print(panel)

        return capture.get()

    def run(self) -> str | None:
        kb = KeyBindings()

        @kb.add("up")
        def _(_):
            self.selected = (self.selected - 1) % len(self.items)

        @kb.add("down")
        def _(_):
            self.selected = (self.selected + 1) % len(self.items)

        @kb.add("enter")
        def _(event):
            self.result = self.items[self.selected]
            event.app.exit()

        @kb.add("q")
        def _(event):
            self.result = None
            event.app.exit()

        @kb.add("c-c")
        def _(_):
            raise KeyboardInterrupt

        control = FormattedTextControl(lambda: ANSI(self._render()))
        window = Window(control, always_hide_cursor=True)

        app = Application(
            layout=Layout(HSplit([window])),
            key_bindings=kb,
            full_screen=True,
        )

        app.run()
        return self.result

class PasswordViewScreen:
    def __init__(
        self,
        *,
        title: str,
        message: str,
        password: str,
    ):
        self.title = title
        self.message = message
        self.password = password

    def run(self) -> None:
        color = "green"

        panel = Panel(
            f"[bold {color}]{self.title}[/bold {color}]\n\n"
            f"{self.message}\n\n"
            "[dim]Press Enter to continue | Press C to copy password[/dim]",
            border_style=color,
        )

        with console.capture() as capture:
            console.print(panel)

        rendered = capture.get()
        kb = KeyBindings()

        # Exit
        @kb.add("enter")
        @kb.add("escape")
        def _(event):
            event.app.exit()

        @kb.add("c-c")
        def _(_):
            raise KeyboardInterrupt

        @kb.add("c")
        def _(event):
            copy_to_clipboard(self.password)

        app = Application(
            layout=Layout(
                Window(
                    FormattedTextControl(ANSI(rendered)),
                    always_hide_cursor=True,
                )
            ),
            key_bindings=kb,
            full_screen=True,
        )

        app.run()

class MessageScreen:
    def __init__(self, title: str, message: str, positive: bool = False):
        self.title = title
        self.message = message
        self.positive = positive

    def run(self) -> None:
        color = "green" if self.positive else "red"

        panel = Panel(
            f"[bold {color}]{self.title}[/bold {color}]\n\n"
            f"{self.message}\n\n"
            "[dim]Press Enter to continue[/dim]",
            border_style=color,
        )

        with console.capture() as capture:
            console.print(panel)

        rendered = capture.get()
        kb = KeyBindings()

        @kb.add("enter")
        @kb.add("escape")
        def _(event):
            event.app.exit()

        @kb.add("c-c")
        def _(_):
            raise KeyboardInterrupt

        app = Application(
            layout=Layout(
                Window(
                    FormattedTextControl(ANSI(rendered)),
                    always_hide_cursor=True,
                )
            ),
            key_bindings=kb,
            full_screen=True,
        )

        app.run()

class InputScreen:
    def __init__(self, title: str, prompt: str, password: bool = False):
        self.title = title
        self.prompt = prompt
        self.password = password
        self.value: str | None = None

    def run(self) -> str | None:
        title_area = TextArea(prompt=self.title, height=2, style="class:title")

        input_area = TextArea(
            prompt=f"{self.prompt}: ",
            password=self.password,
            multiline=False,
        )

        footer = TextArea(
            text="Type and press Enter • Esc to cancel",
            height=1,
            style="class:footer",
            focusable=False,
        )

        frame = Frame(
            HSplit([title_area, input_area, footer], padding=1),
        )

        kb = KeyBindings()

        @kb.add("enter")
        def _(event):
            self.value = input_area.text
            event.app.exit()

        @kb.add("escape")
        def _(event):
            self.value = None
            event.app.exit()

        @kb.add("c-c")
        def _(_):
            raise KeyboardInterrupt

        app = Application(
            layout=Layout(frame, focused_element=input_area),
            key_bindings=kb,
            style=Style.from_dict({
                "title": "bold italic",
                "frame.border": "cyan",
                "footer": "italic dim",
            }),
            full_screen=True,
        )

        app.run()
        return self.value

class QrCodeScreen:
    def __init__(self, title: str, uri: str, secret: str):
        self.title = title
        self.uri = uri
        self.secret = secret

    def _qr_rich(self) -> Text:
        qr = QRCode(border=1)
        qr.add_data(self.uri)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        text = Text()

        for row_top, row_bottom in zip(matrix[::2], matrix[1::2]):
            for top, bottom in zip(row_top, row_bottom):
                if top and bottom:
                    text.append("█", style="white")
                elif top and not bottom:
                    text.append("▀", style="white")
                elif not top and bottom:
                    text.append("▄", style="white")
                else:
                    text.append(" ", style="white")
            text.append("\n")

        return text

    def _secret_text(self) -> Text:
        text = Text()
        text.append("Or enter this secret manually:\n", style="dim")
        text.append(self.secret, style="bold yellow")
        return text

    def run(self) -> None:
        panel = Panel(
                Group(
                        "[bold]Scan this QR code with Google Authenticator[/bold]\n",
                        self._qr_rich(),
                        "\n",
                        self._secret_text(),
                        "\n[dim]Press Enter to continue[/dim]",
                ),
                title=self.title,
                border_style="cyan",
        )

        with console.capture() as capture:
            console.print(panel)

        rendered = capture.get()
        kb = KeyBindings()

        @kb.add("enter")
        def _(event):
            event.app.exit()

        @kb.add("c-c")
        def _(_):
            raise KeyboardInterrupt

        app = Application(
            layout=Layout(
                Window(
                    FormattedTextControl(ANSI(rendered)),
                    always_hide_cursor=True,
                )
            ),
            key_bindings=kb,
            full_screen=True,
        )

        app.run()
