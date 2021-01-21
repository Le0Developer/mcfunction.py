
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import DoubleNode, EntityNode, PositionNode, RawNode
from ...parser_types import Any, Double, Entity, Literal, Position
from ...util import ensure_nodes


SOURCES = (('block', Position), ('entity', Entity))


@dataclass()
class ParsedDataCommand(ParsedCommand):
    command: str

    action: RawNode

    target_type: RawNode = None
    target: t.Union[PositionNode, EntityNode] = None
    path: RawNode = None
    nbt: RawNode = None
    scale: DoubleNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value == 'get':
            ensure_nodes(self, 'target', 'target_type')
            command = f'{base} {self.target_type} {self.target}'
            if self.path is not None:
                if self.scale is not None:
                    return f'{command} {self.path} {self.scale}'
                return f'{command} {self.path}'
            return command

        elif self.action.value == 'merge':
            ensure_nodes(self, 'target', 'target_type', 'nbt')
            return f'{base} {self.target_type} {self.target} {self.nbt}'

        elif self.action.value == 'remove':
            return f'{base} {self.target_type} {self.target} {self.path}'

        else:
            raise ConstructionException(
                f'expected action to be \'get\', \'merge\', or '
                f'\'remove\', not {self.action.value}'
            )


data = Command('data', parsed=ParsedDataCommand)

for name, parser in SOURCES:
    # data get <TARGET> [<path>] [<scale>]
    #  - data get <TARGET> <path> <scale>
    data.add_variation(
        Parser(Literal('get'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
        Parser(Any(), 'path'),
        Parser(Double(), 'scale'),
    )
    #  - data get <TARGET> <path>
    data.add_variation(
        Parser(Literal('get'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
        Parser(Any(), 'path'),
    )
    #  - data get <TARGET>
    data.add_variation(
        Parser(Literal('get'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
    )

    # data merge <TARGET> <nbt>
    data.add_variation(
        Parser(Literal('merge'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
        Parser(Any(), 'nbt'),
    )

    # data remove <TARGET> <path>
    data.add_variation(
        Parser(Literal('remove'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
        Parser(Any(), 'path'),
    )
