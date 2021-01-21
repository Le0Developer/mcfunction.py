
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import Union


@dataclass()
class ParsedDefaultgamemodeCommand(ParsedCommand):
    command: str

    gamemode: RawNode

    def __str__(self):
        return f'{self.command} {self.gamemode}'


defaultgamemode = Command('defaultgamemode',
                          parsed=ParsedDefaultgamemodeCommand)

# defaultgamemode survival
# defaultgamemode creative
# defaultgamemode adventure
# defaultgamemode spectator
defaultgamemode.add_variation(
    Parser(Union('survival', 'creative', 'adventure', 'spectator'), 'gamemode')
)
