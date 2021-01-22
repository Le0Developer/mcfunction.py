
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import Union


@dataclass()
class ParsedBanlistCommand(ParsedCommand):
    command: str

    mode: RawNode = None

    def __str__(self):
        if self.mode is None:
            return self.command
        return f'{self.command} {self.mode}'


banlist = Command('banlist', parsed=ParsedBanlistCommand, oplevel=3)

# banlist [ips|players]
#  - banlist (ips|players)
banlist.add_variation(
    Parser(Union('ips', 'players'), 'mode'),
)
#  - banlist
banlist.add_variation()
