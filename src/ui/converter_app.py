from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import (
    Button,
    DirectoryTree,
    Footer,
    Header,
    Input,
    Label,
    Log,
    Rule,
    Static,
)

from ui.file_selector import FileSelector


class ConverterLayout(Widget):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("Hullo", id="selections"),
            Horizontal(
                FileSelector("Select table file", ".tbl", id="dynamotable"),
                FileSelector("Select VLL file", ".vll", id="vll"),
                FileSelector(
                    "Select starfile with tomogram data", ".star", id="tomograms"
                ),
            ),
            Log(max_lines=10),
        )


class CompactHorizontal(Horizontal):
    DEFAULT_CSS = """
        CompactHorizontal {
            height: auto;
        }
        """


class ConverterApp(App):
    def __init__(self, particle_service):
        self.dynamotable_path = None
        self.vll_path = None
        self.tomograms_path = None
        self.particle_service = particle_service
        super().__init__()

    BINDINGS = [("c", "start_conversion", "Start the conversion")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Horizontal(
                FileSelector("Select table file", ".tbl", id="dynamotable"),
                FileSelector("Select VLL file", ".vll", id="vll"),
                FileSelector(
                    "Select starfile with tomogram data", ".star", id="tomograms"
                ),
            ),
            Label("Output file name", id="input_label"),
            Input(
                type="text",
                max_length=200,
                value="particles.star",
                id="output_filename",
            ),
            Rule(),
            Static(self.get_selection_string(), id="selections"),
            CompactHorizontal(
                Button("Convert and save", id="convert-save"),
                Button("Convert and show", id="convert-print"),
                Button("Quit", id="quit"),
            ),
            Log(max_lines=None, id="log"),
        )

    def print_log(self, log_str):
        self.query_one("#log").write_lines(log_str.splitlines())

    @on(DirectoryTree.FileSelected, "#dynamotable DirectoryTree")
    def handle_dynamo_path(self, message):
        self.dynamotable_path = message.path
        self.update_selections()

    @on(DirectoryTree.FileSelected, "#vll DirectoryTree")
    def handle_vll_path(self, message):
        self.vll_path = message.path
        self.update_selections()

    @on(DirectoryTree.FileSelected, "#tomograms DirectoryTree")
    def handle_tomograms_path(self, message):
        self.tomograms_path = message.path
        self.update_selections()

    @on(Button.Pressed, "#convert-save")
    def convert_save_button_pressed(self):
        output_filename = self.query_one("#output_filename").value
        self.action_start_conversion(output_filename)

    @on(Button.Pressed, "#convert-print")
    def convert_print_button_pressed(self):
        self.action_start_conversion()

    @on(Button.Pressed, "#quit")
    def quit_button_pressed(self):
        self.exit()

    def action_start_conversion(self, output_filename=None):
        self.particle_service.convert_dynamo_star(
            self.dynamotable_path,
            self.tomograms_path,
            self.vll_path,
            output_filename,
        )

    def update_selections(self):
        self.query_one("#selections").update(self.get_selection_string())

    def get_selection_string(self):
        table_str = f"Table file:     {str(self.dynamotable_path or '')}"
        vll_str = f"VLL file:       {str(self.vll_path or '')}"
        tomograms_str = f"Tomograms file: {str(self.tomograms_path or '')}"
        return f"{table_str}\n{vll_str}\n{tomograms_str}"
