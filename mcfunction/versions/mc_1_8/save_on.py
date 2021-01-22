
from dataclasses import dataclass

from .. import Command, ParsedCommand


@dataclass()
class ParsedSaveOnCommand(ParsedCommand):
    command: str

    def __str__(self):
        return self.command


save_on = Command('save-on', parsed=ParsedSaveOnCommand, oplevel=3)

# save-on
save_on.add_variation()
