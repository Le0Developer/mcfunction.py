
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import RawNode
from ..parser_types import GreedyAny


@dataclass()
class ParsedSayCommand(ParsedCommand):
    command: str

    message: RawNode

    def __str__(self):
        return f'{self.command} {self.message}'


say = Command('say', parsed=ParsedSayCommand)

# say <message>
say.add_variation(
    Parser(GreedyAny(), 'message'),
)
