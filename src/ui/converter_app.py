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


class CompactHorizontal(Horizontal):
    """A Horizontal Widget with height fit to the contents."""

    DEFAULT_CSS = """
        CompactHorizontal {
            height: auto;
        }
        """


class ConverterApp(App):
    """Class responsible for the interactive UI of the application."""

    def __init__(self, particle_service):
        """Constructor for the class.

        args:
            particle_service: a ParticleService object for handling metadata conversion.
        """
        self._dynamotable_path = None
        self._vll_path = None
        self._tomograms_path = None
        self._particle_service = particle_service
        super().__init__()

    BINDINGS = [("c", "start_conversion", "Start the conversion")]

    def compose(self) -> ComposeResult:
        """Compose the UI elements for the application."""

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
            Static(self._get_selection_string(), id="selections"),
            CompactHorizontal(
                Button("Convert and save", id="convert-save"),
                Button("Convert and show", id="convert-print"),
                Button("Quit", id="quit"),
            ),
            Log(max_lines=None, id="log"),
        )

    def show_log(self, log_str):
        """Writes a string to the log element in the UI.

        args:
            log_str: string to write.
        """
        self.query_one("#log").write_lines(log_str.splitlines())

    @on(DirectoryTree.FileSelected, "#dynamotable DirectoryTree")
    def _handle_dynamo_path(self, message):
        self._dynamotable_path = message.path
        self._update_selections()

    @on(DirectoryTree.FileSelected, "#vll DirectoryTree")
    def _handle_vll_path(self, message):
        self._vll_path = message.path
        self._update_selections()

    @on(DirectoryTree.FileSelected, "#tomograms DirectoryTree")
    def _handle_tomograms_path(self, message):
        self._tomograms_path = message.path
        self._update_selections()

    @on(Button.Pressed, "#convert-save")
    def _convert_save_button_pressed(self):
        output_filename = self.query_one("#output_filename").value
        self.action_start_conversion(output_filename)

    @on(Button.Pressed, "#convert-print")
    def _convert_print_button_pressed(self):
        self.action_start_conversion()

    @on(Button.Pressed, "#quit")
    def _quit_button_pressed(self):
        self.exit()

    def action_start_conversion(self, output_filename=None):
        """Starts the conversion process.

        args:
            output_filename:
                Optional, defaults to None.
                string or PathLike to the file where converted data should be written.
                If omitted, the results will be redirected to the log.
        """
        self._particle_service.convert_dynamo_star(
            self._dynamotable_path,
            self._tomograms_path,
            self._vll_path,
            output_filename,
        )

    def _update_selections(self):
        self.query_one("#selections").update(self._get_selection_string())

    def _get_selection_string(self):
        table_str = f"Table file:     {str(self._dynamotable_path or '')}"
        vll_str = f"VLL file:       {str(self._vll_path or '')}"
        tomograms_str = f"Tomograms file: {str(self._tomograms_path or '')}"
        return f"{table_str}\n{vll_str}\n{tomograms_str}"
