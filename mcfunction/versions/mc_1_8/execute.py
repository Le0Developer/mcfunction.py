from __future__ import annotations

from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ParserException
from ...nodes import BlockNode, EntityNode, IntegerNode, PositionNode, RawNode
from ...parser import parse_command
from ...parser_types import Block, Entity, Integer, Literal, Position
from ...util import ensure_nodes, tokenize


@dataclass()
class ParsedExecuteCommand(ParsedCommand):
    command: str

    target: EntityNode
    position: PositionNode
    run: ParsedCommand

    detect: RawNode = None
    detect_position: PositionNode = None
    block: BlockNode = None
    data: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.target} {self.position}'
        if self.detect is not None:
            ensure_nodes(self, 'detect_position', 'block', 'data')
            return f'{base} {self.detect} {self.detect_position} ' \
                   f'{self.block} {self.data} {self.run}'
        return f'{base} {self.run}'


class ExecuteCommand(Command):
    def parse(self, command: str):
        exception = None
        exception_dept = -1
        for variation in self.variations:
            parts = tokenize(command, ' ')
            result = {'command': next(parts)}
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
                result['run'] = parse_command(' '.join(parts))
                return self.parsed(**result)

        if exception is None:  # pragma: no cover
            raise ParserException('should not happen')
        raise exception  # pragma: no cover


execute = ExecuteCommand('execute', parsed=ParsedExecuteCommand)

# execute <target> <position> detect <position> <block> <data> <command>
execute.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Literal('detect'), 'detect'),
    Parser(Position(), 'detect_position'),
    Parser(Block(), 'block'),
    Parser(Integer(), 'data')
)
# execute <target> <position> <command>
execute.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position')
)
