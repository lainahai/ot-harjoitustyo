from pathlib import Path
from typing import Iterable

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DirectoryTree, Static


class FileSelector(VerticalScroll):
    """File selection component for the UI.

    Composed of a label to tell which file is selected and
    a directory tree component filtered by a string.
    """

    class FilteredDirectoryTree(DirectoryTree):
        """DirectoryTree component with filter."""

        def __init__(self, path, filter_string):
            """Constructor for the component.

            args:
                path: string ot PathLike to the directory tree root.
                filter_string: string to filter files by name.
            """
            self.filter_string = filter_string
            super().__init__(path)

        def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
            return [
                path
                for path in paths
                if self.filter_string in path.name or path.is_dir()
            ]

    def __init__(self, title, filter_string, id=None):
        """Constructor for the class.

        args:
            title: String to show as the header for the component.
            filter_string: string to filter files by name.
        """
        self.title = title
        self.filter_string = filter_string
        super().__init__(id=id, can_focus=False)

    def compose(self) -> ComposeResult:
        """Compose the UI elements for this widget."""
        yield Static(self.title, classes="header")
        yield self.FilteredDirectoryTree("./", self.filter_string)
