
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedSeedCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


seed = Command('seed', parsed=ParsedSeedCommand)

# seed
seed.add_variation()
