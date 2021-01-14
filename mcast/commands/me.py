
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import RawNode
from ..parser_types import GreedyAny


@dataclass()
class ParsedMeCommand(ParsedCommand):
    command: str

    message: RawNode

    def __str__(self):
        return f'{self.command} {self.message}'


me = Command('me', parsed=ParsedMeCommand)

# me <message>
me.add_variation(
    Parser(GreedyAny(), 'message'),
)
