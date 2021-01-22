
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedStopCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


stop = Command('stop', parsed=ParsedStopCommand, oplevel=4)

# stop
stop.add_variation()
