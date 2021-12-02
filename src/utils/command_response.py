import click

class CommandResponse:
    def __init__(self, _successful: bool, _message : str):
        self.successful = _successful
        self.message = _message

    def print_result_to_console(self):
        click.secho(self.message, fg="green", bold=True) if self.successful else click.secho(self.message, fg="red", bold=True)
