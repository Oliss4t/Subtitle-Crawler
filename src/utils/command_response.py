import click

class CommandResponse:
    """
    This class defines a response of a CLI command.
    """
    def __init__(self, _successful: bool, _message : str):
        """
        Constructor
        :param _successful: boolean whether the command was successful or failed/an error occurred
        :param _message: message of the result of the command
        """
        self.successful = _successful
        self.message = _message

    def print_result_to_console(self):
        """
        prints the result to the CLI.
        Successful results getting printed in green.
        Unsuccessful results getting printed red.
        """
        click.secho(self.message, fg="green", bold=True) if self.successful else click.secho(self.message, fg="red", bold=True)
