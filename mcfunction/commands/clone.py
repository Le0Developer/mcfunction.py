
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import BlockNode, PositionNode, RawNode
from ..parser_types import Block, Literal, Position, Union


@dataclass()
class ParsedCloneCommand(ParsedCommand):
    command: str

    begin: PositionNode
    end: PositionNode
    destination: PositionNode
    mask_mode: RawNode = None  # unnamed in JE, taken from BE
    filter: BlockNode = None
    clone_mode: RawNode = None  # unnamed in JE, taken from BE

    def __str__(self):
        base = f'{self.command} {self.begin} {self.end} {self.destination}'
        if self.mask_mode is None:
            return base

        elif self.mask_mode.value in ('replace', 'masked'):
            command = f'{base} {self.mask_mode}'

        elif self.mask_mode.value == 'filtered':
            command = f'{base} filtered {self.filter}'

        else:
            raise ConstructionException(
                f'invalid mask_mode for clone command, expected one of '
                f'\'replace\', \'masked\' or \'filtered\', '
                f'not {self.mask_mode.value!r}'
            )

        if self.clone_mode is not None:
            return f'{command} {self.clone_mode}'

        return command


clone = Command('clone', parsed=ParsedCloneCommand)

# clone <begin> <end> <destination> [replace|masked] [force|move|normal]
#  - clone <begin> <end> <destination> <replace|masked> <force|move|normal>
clone.add_variation(
    Parser(Position(), 'begin'),
    Parser(Position(), 'end'),
    Parser(Position(), 'destination'),
    Parser(Union('replace', 'masked'), 'mask_mode'),
    Parser(Union('force', 'move', 'normal'), 'clone_mode'),
)
#  - clone <begin> <end> <destination> <replace|masked>
clone.add_variation(
    Parser(Position(), 'begin'),
    Parser(Position(), 'end'),
    Parser(Position(), 'destination'),
    Parser(Union('replace', 'masked'), 'mask_mode'),
)
#  - clone <begin> <end> <destination>
clone.add_variation(
    Parser(Position(), 'begin'),
    Parser(Position(), 'end'),
    Parser(Position(), 'destination'),
)

# clone <begin> <end> <destination> filtered <filter> [force|move|normal]
#  - clone <begin> <end> <destination> filtered <filter> <force|move|normal>
clone.add_variation(
    Parser(Position(), 'begin'),
    Parser(Position(), 'end'),
    Parser(Position(), 'destination'),
    Parser(Literal('filtered'), 'mask_mode'),
    Parser(Block(), 'filter'),
    Parser(Union('force', 'move', 'normal'), 'clone_mode')
)

#  - clone <begin> <end> <destination> filtered <filter>
clone.add_variation(
    Parser(Position(), 'begin'),
    Parser(Position(), 'end'),
    Parser(Position(), 'destination'),
    Parser(Literal('filtered'), 'mask_mode'),
    Parser(Block(), 'filter'),
)
