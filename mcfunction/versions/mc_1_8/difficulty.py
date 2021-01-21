
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import Union


@dataclass()
class ParsedDifficultyCommand(ParsedCommand):
    command: str

    difficulty: RawNode

    def __str__(self):
        return f'{self.command} {self.difficulty}'


difficulty = Command('difficulty', parsed=ParsedDifficultyCommand)

# difficulty peaceful
# difficulty easy
# difficulty normal
# difficulty hard
difficulty.add_variation(
    Parser(Union('peaceful', 'easy', 'normal', 'hard'), 'difficulty')
)
