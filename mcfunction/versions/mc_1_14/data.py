
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import DoubleNode, EntityNode, IntegerNode, PositionNode, RawNode
from ...parser_types import Any, Double, Entity, Integer, Literal, Position
from ...util import ensure_nodes


SOURCES = (('block', Position), ('entity', Entity))


@dataclass()
class ParsedDataCommand(ParsedCommand):
    command: str

    action: RawNode

    target_type: RawNode = None
    target: t.Union[PositionNode, EntityNode] = None
    modification: RawNode = None
    modification_source: RawNode = None
    path: RawNode = None
    index: IntegerNode = None
    source_path: RawNode = None
    source_type: RawNode = None
    source: t.Union[PositionNode, EntityNode] = None
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

        elif self.action.value == 'modify':
            ensure_nodes(
                self, 'target', 'target_type', 'path', 'modification',
                'modification_source'
            )
            command = f'{base} {self.target_type} {self.target} {self.path}'
            if self.modification.value == 'insert':
                ensure_nodes(self, 'index')
                command = f'{command} {self.modification} {self.index}'
            else:
                command = f'{command} {self.modification}'

            if self.modification_source.value == 'from':
                ensure_nodes(self, 'source', 'source_type')
                command = f'{command} {self.modification_source} ' \
                          f'{self.source_type} {self.source}'
                if self.source_path is not None:
                    return f'{command} {self.source_path}'
                return command

            elif self.modification_source.value == 'value':
                ensure_nodes(self, 'source_path')
                return f'{command} {self.modification_source} ' \
                       f'{self.source_path}'

            else:
                raise ConstructionException(
                    f'expected modification_source to be \'from\' '
                    f'or \'value\', not {self.modification_source.value}'
                )

        elif self.action.value == 'remove':
            return f'{base} {self.target_type} {self.target} {self.path}'

        else:
            raise ConstructionException(
                f'expected action to be \'get\', \'merge\', \'modify\' or '
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

    # TODO: use Union for this?
    for modification in ('append', 'merge', 'prepend', 'set'):
        for source_name, source_parser in SOURCES:
            # data modify <TARGET> <targetPath> <MODIFICATION> from <SOURCE>
            #   [<sourcePath>]
            #  - modify <TARGET> <targetPath> <MODIFICATION> from <SOURCE>
            #     <sourcePath>

            data.add_variation(
                Parser(Literal('modify'), 'action'),
                Parser(Literal(name), 'target_type'),
                Parser(parser(), 'target'),
                Parser(Any(), 'path'),
                Parser(Literal(modification), 'modification'),
                Parser(Literal('from'), 'modification_source'),
                Parser(Literal(source_name), 'source_type'),
                Parser(source_parser(), 'source'),
                Parser(Any(), 'source_path')
            )

            data.add_variation(
                Parser(Literal('modify'), 'action'),
                Parser(Literal(name), 'target_type'),
                Parser(parser(), 'target'),
                Parser(Any(), 'path'),
                Parser(Literal(modification), 'modification'),
                Parser(Literal('from'), 'modification_source'),
                Parser(Literal(source_name), 'source_type'),
                Parser(source_parser(), 'source'),
            )

        # data modify <TARGET> <targetPath> <MODIFICATION> value <value>
        data.add_variation(
            Parser(Literal('modify'), 'action'),
            Parser(Literal(name), 'target_type'),
            Parser(parser(), 'target'),
            Parser(Any(), 'path'),
            Parser(Literal(modification), 'modification'),
            Parser(Literal('value'), 'modification_source'),
            Parser(Any(), 'source_path'),
        )

    for source_name, source_parser in SOURCES:
        data.add_variation(
            Parser(Literal('modify'), 'action'),
            Parser(Literal(name), 'target_type'),
            Parser(parser(), 'target'),
            Parser(Any(), 'path'),
            Parser(Literal('insert'), 'modification'),
            Parser(Integer(), 'index'),
            Parser(Literal('from'), 'modification_source'),
            Parser(Literal(source_name), 'source_type'),
            Parser(source_parser(), 'source'),
            Parser(Any(), 'source_path')
        )

        data.add_variation(
            Parser(Literal('modify'), 'action'),
            Parser(Literal(name), 'target_type'),
            Parser(parser(), 'target'),
            Parser(Any(), 'path'),
            Parser(Literal('insert'), 'modification'),
            Parser(Integer(), 'index'),
            Parser(Literal('from'), 'modification_source'),
            Parser(Literal(source_name), 'source_type'),
            Parser(source_parser(), 'source'),
        )

    # data modify <TARGET> <targetPath> <MODIFICATION> value <value>
    data.add_variation(
        Parser(Literal('modify'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
        Parser(Any(), 'path'),
        Parser(Literal('insert'), 'modification'),
        Parser(Integer(), 'index'),
        Parser(Literal('value'), 'modification_source'),
        Parser(Any(), 'source_path'),
    )

    # data remove <TARGET> <path>
    data.add_variation(
        Parser(Literal('remove'), 'action'),
        Parser(Literal(name), 'target_type'),
        Parser(parser(), 'target'),
        Parser(Any(), 'path'),
    )
