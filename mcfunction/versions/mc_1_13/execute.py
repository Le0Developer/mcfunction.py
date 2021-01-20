from __future__ import annotations

from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException, ParserException
from ...nodes import (
    BlockNode, DoubleNode, EntityNode, NamespaceIDNode, PositionNode, RawNode,
    RotationNode
)
from ...parser import parse_command
from ...parser_types import (
    Any, Block, Double, Entity, Literal, NamespaceID, Objective, Position,
    ScoreboardEntity, Rotation, Union
)
from ...util import ensure_nodes, tokenize


@dataclass()
class ParsedExecuteCommand(ParsedCommand):
    command: str

    conditions: t.List[ParsedExecuteCondition]
    run: ParsedCommand

    def __str__(self):
        if self.conditions:
            conditions = ' '.join(str(x) for x in self.conditions)
            return f'{self.command} {conditions} run {self.run}'
        return f'{self.command} run {self.run}'


@dataclass()
class ParsedExecuteCondition(ParsedCommand):
    action: RawNode

    axes: RawNode = None
    anchor: RawNode = None
    target: EntityNode = None
    position: PositionNode = None
    rotation: RotationNode = None
    is_entity: RawNode = None
    dimension: NamespaceIDNode = None

    condition: RawNode = None
    mode: RawNode = None
    block: BlockNode = None
    start: PositionNode = None
    end: PositionNode = None
    destination: t.Union[NamespaceIDNode, PositionNode, EntityNode] = None
    source_type: RawNode = None
    source: t.Union[PositionNode, EntityNode, NamespaceIDNode] = None
    path: RawNode = None
    type: RawNode = None
    comparison: RawNode = None
    target_objective: RawNode = None
    source_objective: RawNode = None
    range: RawNode = None
    scale: DoubleNode = None

    def __str__(self):
        base = f'{self.action}'
        if self.action.value == 'align':
            ensure_nodes(self, 'axes')
            return f'{base} {self.axes}'

        elif self.action.value == 'anchored':
            ensure_nodes(self, 'anchor')
            return f'{base} {self.anchor}'

        elif self.action.value in ('at', 'as'):
            ensure_nodes(self, 'target')
            return f'{base} {self.target}'

        elif self.action.value == 'facing':
            if self.is_entity is not None:
                ensure_nodes(self, 'target', 'anchor')
                return f'{base} {self.is_entity} {self.target} {self.anchor}'
            ensure_nodes(self, 'position')
            return f'{base} {self.position}'

        elif self.action.value == 'in':
            ensure_nodes(self, 'dimension')
            return f'{base} {self.dimension}'

        elif self.action.value == 'positioned':
            if self.is_entity is not None:
                ensure_nodes(self, 'target')
                return f'{base} {self.is_entity} {self.target}'
            ensure_nodes(self, 'position')
            return f'{base} {self.position}'

        elif self.action.value == 'rotated':
            if self.is_entity is not None:
                ensure_nodes(self, 'target')
                return f'{base} {self.is_entity} {self.target}'
            ensure_nodes(self, 'rotation')
            return f'{base} {self.rotation}'

        elif self.action.value == 'store':
            ensure_nodes(self, 'condition', 'mode')
            command = f'{base} {self.condition} {self.mode}'
            if self.mode.value in ('block', 'entity'):
                ensure_nodes(self, 'destination', 'path', 'type', 'scale')
                return (
                    f'{command} {self.destination} {self.path} '
                    f'{self.type} {self.scale}'
                )
            elif self.mode.value == 'bossbar':
                ensure_nodes(self, 'destination', 'path')
                return f'{command} {self.destination} {self.path}'
            elif self.mode.value == 'score':
                ensure_nodes(self, 'target', 'target_objective')
                return f'{command} {self.target} {self.target_objective}'
            else:
                raise ConstructionException(
                    f'expected mode to be \'block\', \'entity\', \'bossbar\' '
                    f'or \'score\', not {self.mode.value!r}'
                )

        else:
            raise ConstructionException(
                f'expected action to be \'align\', \'anchored\', \'as\', '
                f'\'at\', \'facing\', \'in\', \'positioned\', \'rotated\', '
                f'\'store\', \'store\', not {self.action.value!r}'
            )


class ExecuteCommand(Command):
    def parse(self, command: str):
        # remove command name
        command = ' '.join(tuple(tokenize(command, ' '))[1:])
        conditions = []

        while True:
            exception = None
            exception_dept = -1
            for variation in self.variations:
                result = {}
                parts = tokenize(command, ' ')
                for no, parser in enumerate(variation):
                    try:
                        node = parser.parser.parse(parts)
                    except ParserException as exc:
                        if no > exception_dept:
                            exception = exc
                            exception_dept = no
                        break
                    except StopIteration:  # pragma: no cover
                        if no > exception_dept:
                            exception = ParserException('too few arguments')
                            exception_dept = no
                        break
                    else:
                        if parser.destination:
                            result[parser.destination] = node

                else:
                    command = ' '.join(parts)
                    parsed = self.parsed(**result)
                    if parsed.action.value == 'run':
                        return ParsedExecuteCommand(
                            'execute', conditions, parse_command(command)
                        )
                    conditions.append(self.parsed(**result))
                    break

            else:  # pragma: no cover
                if exception is None:
                    raise ParserException('should not happen')
                raise exception


execute = ExecuteCommand('execute', parsed=ParsedExecuteCondition)


# ... align <axes>
execute.add_variation(
    Parser(Literal('align'), 'action'),
    Parser(Any(), 'axes'),
)

# ... anchored <anchor>
execute.add_variation(
    Parser(Literal('anchored'), 'action'),
    Parser(Union('eyes', 'feet'), 'anchor'),
)

# ... as <targets>
execute.add_variation(
    Parser(Union('as', 'at'), 'action'),
    Parser(Entity(), 'target'),
)

# ... facing <pos>
execute.add_variation(
    Parser(Literal('facing'), 'action'),
    Parser(Position(), 'position'),
)
# ... facing entity <target> <anchor>
execute.add_variation(
    Parser(Literal('facing'), 'action'),
    Parser(Literal('entity'), 'is_entity'),
    Parser(Entity(), 'target'),
    Parser(Union('eyes', 'feet'), 'anchor'),
)

# ... in <dimension>
execute.add_variation(
    Parser(Literal('in'), 'action'),
    Parser(NamespaceID(), 'dimension'),
)

# ... positioned <pos>
execute.add_variation(
    Parser(Literal('positioned'), 'action'),
    Parser(Position(), 'position'),
)
# ... positioned as <targets>
execute.add_variation(
    Parser(Literal('positioned'), 'action'),
    Parser(Literal('as'), 'is_entity'),
    Parser(Entity(), 'target'),
)

# ... rotated <rot>
execute.add_variation(
    Parser(Literal('rotated'), 'action'),
    Parser(Rotation(), 'rotation'),
)
# ... rotated as <targets>
execute.add_variation(
    Parser(Literal('rotated'), 'action'),
    Parser(Literal('as'), 'is_entity'),
    Parser(Entity(), 'target'),
)

SOURCES = (('block', Position), ('entity', Entity))
# ... store (result|success) block <targetPos> <path> <type> <scale>
# ... store (result|success) entity <target> <path> <type> <scale>
for source_type, parser in SOURCES:
    execute.add_variation(
        Parser(Literal('store'), 'action'),
        Parser(Union('result', 'success'), 'condition'),
        Parser(Literal(source_type), 'mode'),
        Parser(parser(), 'destination'),
        Parser(Any(), 'path'),
        Parser(Union('byte', 'short', 'int', 'long', 'float', 'double'),
               'type'),
        Parser(Double(), 'scale'),
    )
# ... store (result|success) bossbar <id> (value|max)
execute.add_variation(
    Parser(Literal('store'), 'action'),
    Parser(Union('result', 'success'), 'condition'),
    Parser(Literal('bossbar'), 'mode'),
    Parser(NamespaceID(), 'destination'),
    Parser(Union('value', 'max'), 'path'),  # not really path, better ideas?
)
# ... store (result|success) score <targets> <objective>
execute.add_variation(
    Parser(Literal('store'), 'action'),
    Parser(Union('result', 'success'), 'condition'),
    Parser(Literal('score'), 'mode'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Any(), 'target_objective'),
)

# ... run
execute.add_variation(
    Parser(Literal('run'), 'action'),
)
