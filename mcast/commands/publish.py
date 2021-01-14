
from dataclasses import dataclass

from . import Command, ParsedCommand


@dataclass()
class ParsedPublishCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


publish = Command('publish', commandblock=False, parsed=ParsedPublishCommand)

# publish
publish.add_variation()
