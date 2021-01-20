
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, RawNode
from ...parser_types import Entity, Union


@dataclass()
class ParsedGamemodeCommand(ParsedCommand):
    command: str

    gamemode: RawNode

    target: EntityNode = None

    def __str__(self):
        base = f'{self.command} {self.gamemode}'
        if self.target is not None:
            return f'{base} {self.target}'
        return base


gamemode = Command('gamemode', parsed=ParsedGamemodeCommand)

# gamemode (adventure|creative|spectator|survival) [<target>]
#  - gamemode (adventure|creative|spectator|survival) <target>
gamemode.add_variation(
    Parser(Union('adventure', 'creative', 'spectator', 'survival', '0', '1',
                 '2', '3', 'a', 'c', 's'), 'gamemode'),
    Parser(Entity(), 'target'),
)

#  - gamemode (adventure|creative|spectator|survival)
gamemode.add_variation(
    Parser(Union('adventure', 'creative', 'spectator', 'survival',  '0', '1',
                 '2', '3', 'a', 'c', 's'), 'gamemode')
)
