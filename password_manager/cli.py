from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import Window, HSplit
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.controls import FormattedTextControl

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.widgets import TextArea


console = Console()


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
        kb = KeyBindings()

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
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    def run(self):
        color = "green" if self.title == "Success" else "red"

        text = f"[bold {color}]{self.title}[/bold {color}]\n\n{self.message}\n\n[dim]Press Enter to continue[/dim]"
        panel = Panel(text, border_style=color)

        with console.capture() as capture:
            console.print(panel)
        rendered = capture.get()

        kb = KeyBindings()

        @kb.add("c-c")
        def _(event):
            event.app.exit()

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
        input_field = TextArea(
            prompt=f"{self.prompt}: ",
            password=self.password,
            multiline=False,
            wrap_lines=False,
        )

        kb = KeyBindings()

        @kb.add("c-c")
        def _(event):
            event.app.exit()

        @kb.add("enter")
        def _(event):
            self.value = input_field.text
            event.app.exit()

        @kb.add("escape")
        def _(event):
            self.value = None
            event.app.exit()

        header_panel = Panel(
            f"[bold cyan]{self.title}[/bold cyan]\n\n"
            "[dim]Type and press Enter • Esc to cancel[/dim]",
            border_style="cyan",
        )

        with console.capture() as capture:
            console.print(header_panel)
        header_ansi = capture.get()

        layout = Layout(
            HSplit([
                Window(
                    FormattedTextControl(ANSI(header_ansi)),
                    height=6,
                    always_hide_cursor=True,
                ),
                Frame(
                    body=input_field.__pt_container__(),
                    title=self.prompt,
                )
            ]),
            focused_element=input_field,
        )

        app = Application(
            layout=layout,
            key_bindings=kb,
            full_screen=True,
        )

        app.run()
        return self.value
