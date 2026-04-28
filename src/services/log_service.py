class LogService:
    def __init__(self, ui=None):
        self.ui = ui

    def log(self, log_str, ui_only=False):
        if self.ui:
            self.ui.show_log(log_str)
        elif not ui_only:
            try:
                print(log_str)
            except BrokenPipeError:
                pass
