import io

from qrcode.main import QRCode
from prompt_toolkit import ANSI
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, FormattedTextControl
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

console = Console()
kb = KeyBindings()


class Menu:
    def __init__(self, title: str, subtitle: str, items: list[str]):
        self.title = title
        self.subtitle = subtitle
        self.items = items
        self.selected = 0
        self.result = None

        self.control = FormattedTextControl(self._get_rendered_text)
        self.window = Window(content=self.control, always_hide_cursor=True)

        self.kb = self._create_keybindings()
        self.layout = Layout(HSplit([self.window]))

        self.app = Application(
            layout=self.layout,
            key_bindings=self.kb,
            full_screen=True,
        )

    def _render_rich(self) -> str:
        """Render Rich layout to ANSI text"""
        table = Table.grid(padding=1)
        for i, item in enumerate(self.items):
            if i == self.selected:
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

    def _get_rendered_text(self):
        return ANSI(self._render_rich())

    def _create_keybindings(self):
        @kb.add("c-c")
        def _(event):
            event.app.exit()

        @kb.add("up")
        def _(_):
            self.selected = (self.selected - 1) % len(self.items)

        @kb.add("down")
        def _(_):
            self.selected = (self.selected + 1) % len(self.items)

        @kb.add("enter")
        def _(_):
            self.result = self.items[self.selected]
            self.app.exit()

        @kb.add("q")
        def _(_):
            self.result = None
            self.app.exit()

        return kb

    def run(self):
        self.app.run()
        return self.result


class MessageScreen:
    def __init__(self, title: str, message: str, positive: bool = False):
        self.title = title
        self.message = message
        self.positive = positive

    def run(self):
        color = "green" if self.positive else "red"

        text = f"[bold {color}]{self.title}[/bold {color}]\n\n{self.message}\n\n[dim]Press Enter to continue[/dim]"
        panel = Panel(text, border_style=color)

        with console.capture() as capture:
            console.print(panel)
        rendered = capture.get()

        @kb.add("c-c")
        @kb.add("enter")
        @kb.add("escape")
        def _(event):
            event.app.exit()

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
        self.value = None

    def run(self):
        title_area = TextArea(prompt=self.title, height=2, style="class:title")

        text_area = TextArea(
            prompt=self.prompt + ": ",
            password=self.password,
            multiline=False,
            wrap_lines=True,
        )

        footer = TextArea(
            text="Type and press Enter • Esc to cancel",
            style="class:footer",
            height=1,
            focusable=False,
        )

        body = HSplit([
            title_area,
            text_area,
            footer,
        ], padding=1)

        frame = Frame(
            body=body
        )

        @kb.add("enter")
        def _(event):
            self.value = text_area.text
            event.app.exit()

        @kb.add("escape")
        @kb.add("c-c")
        def _(event):
            self.value = None
            event.app.exit()

        layout = Layout(frame, focused_element=text_area)

        style = Style.from_dict({
            "title": "bold italic",
            "frame.border": "cyan",
            "footer": "italic dim",
        })

        app = Application(
            layout=layout,
            key_bindings=kb,
            style=style,
            full_screen=True,
        )

        app.run()
        return self.value

class QrCodeScreen:
    def __init__(self, title: str, uri: str):
        self.title = title
        self.uri = uri

    def _get_qr_ascii(self) -> str:
        qr = QRCode(border=1)
        qr.add_data(self.uri)
        qr.make()

        buffer = io.StringIO()
        qr.print_ascii(out=buffer, invert=True)
        return buffer.getvalue()

    def _render(self) -> str:
        qr_ascii = self._get_qr_ascii()

        with console.capture() as capture:
            console.print(
                Panel(
                    Group(
                        "[bold]Scan this QR code with Google Authenticator[/bold]\n",
                        qr_ascii,
                        "\n[dim]Press Enter to continue • Esc to cancel[/dim]",
                    ),
                    title=self.title,
                    border_style="cyan",
                )
            )
        return capture.get()

    def run(self):
        rendered = self._render()

        @kb.add("enter")
        @kb.add("escape")
        @kb.add("c-c")
        def _(event):
            event.app.exit()

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
