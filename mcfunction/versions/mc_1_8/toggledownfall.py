
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedToggledownfallCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


toggledownfall = Command('toggledownfall', parsed=ParsedToggledownfallCommand)

# toggledownfall
toggledownfall.add_variation()
