
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedStopCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


stop = Command('stop', commandblock=False, parsed=ParsedStopCommand)

# stop
stop.add_variation()
