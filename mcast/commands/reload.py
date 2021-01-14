
from dataclasses import dataclass

from . import Command, ParsedCommand


@dataclass()
class ParsedReloadCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


reload = Command('reload', parsed=ParsedReloadCommand)

# reload
reload.add_variation()
