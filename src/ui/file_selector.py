from pathlib import Path
from typing import Iterable

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DirectoryTree, Static


class FileSelector(VerticalScroll):
    class FilteredDirectoryTree(DirectoryTree):
        def __init__(self, path, filter_string):
            self.filter_string = filter_string
            super().__init__(path)

        def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
            return [
                path
                for path in paths
                if self.filter_string in path.name or path.is_dir()
            ]

    def __init__(self, title, filter_string, id=None):
        self.title = title
        self.filter_string = filter_string
        self.selected_file_path = None
        super().__init__(id=id, can_focus=False)

    def compose(self) -> ComposeResult:
        yield Static(self.title, classes="header")
        # yield Static("", id="selected")
        yield self.FilteredDirectoryTree("./", self.filter_string)

    def on_directory_tree_file_selected(self, message: DirectoryTree.FileSelected):
        self.selected_file_path = message.path
        # self.query_one("#selected").update(f"Selected: {str(self.selected_file_path)}")
