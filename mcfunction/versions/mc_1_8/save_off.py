
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedSaveOffCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


save_off = Command('save-off', parsed=ParsedSaveOffCommand, oplevel=3)

# save-off
save_off.add_variation()
