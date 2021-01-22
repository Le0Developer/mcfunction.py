
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import GreedyAny


@dataclass()
class ParsedTeammsgCommand(ParsedCommand):
    command: str

    message: RawNode

    def __str__(self):
        return f'{self.command} {self.message}'


teammsg = Command('teammsg', aliases=['tm'], parsed=ParsedTeammsgCommand,
                  oplevel=0)

# teammsg <message>
teammsg.add_variation(
    Parser(GreedyAny(), 'message'),
)
