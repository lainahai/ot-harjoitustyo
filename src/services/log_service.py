class LogService:
    def __init__(self, ui=None):
        self.ui = None

    def log(self, log_str, ui_only=False):
        if self.ui:
            self.ui.print_log(log_str)
        elif not ui_only:
            try:
                print(log_str)
            except BrokenPipeError:
                # Avoid unnecessary error if piping output to head or something else that stops reading early.
                return
