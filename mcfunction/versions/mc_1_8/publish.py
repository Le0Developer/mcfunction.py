
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedPublishCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


publish = Command('publish', parsed=ParsedPublishCommand, oplevel=4)

# publish
publish.add_variation()
