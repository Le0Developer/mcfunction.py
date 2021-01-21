
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode
from ...parser_types import Entity


@dataclass()
class ParsedSpectateCommand(ParsedCommand):
    command: str

    target: EntityNode = None
    player: EntityNode = None

    def __str__(self):
        if self.target is not None:
            if self.player is not None:
                return f'{self.command} {self.target} {self.player}'
            return f'{self.command} {self.target}'
        return self.command


spectate = Command('spectate', parsed=ParsedSpectateCommand)

# spectate
spectate.add_variation()

# spectate <target> [<player>]
#  - spectate <target> <player>
spectate.add_variation(
    Parser(Entity(), 'target'),
    Parser(Entity(), 'player'),
)
#  - spectate <target>
spectate.add_variation(
    Parser(Entity(), 'target'),
)
