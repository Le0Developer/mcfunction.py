
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import (
    DoubleNode, EntityNode, IntegerNode, NamespaceIDNode, PositionNode, RawNode
)
from ...parser_types import Block, Double, Entity, Integer, Position, Union


@dataclass()
class ParsedParticleCommand(ParsedCommand):
    command: str

    name: NamespaceIDNode
    position: PositionNode
    delta: PositionNode
    speed: DoubleNode
    count: IntegerNode

    mode: RawNode = None
    viewers: EntityNode = None

    def __str__(self):
        base = f'{self.command} {self.name} {self.position} {self.delta} ' \
               f'{self.speed} {self.count}'

        if self.mode is None:
            return base
        if self.viewers is None:
            return f'{base} {self.mode}'
        return f'{base} {self.mode} {self.viewers}'


particle = Command('particle', parsed=ParsedParticleCommand)

# particle <name> [<parameters>] [<pos>] [<delta>] <speed> <count>
#   [force|normal] [<viewers>]
#  - particle <name> <pos> <delta> <speed> <count> (force|normal) <viewers>
particle.add_variation(
    Parser(Block(), 'name'),
    Parser(Position(), 'position'),
    Parser(Position(), 'delta'),
    Parser(Double(), 'speed'),
    Parser(Integer(), 'count'),
    Parser(Union('force', 'normal'), 'mode'),
    Parser(Entity(), 'viewers'),
)
#  - particle <name> <pos> <delta> <speed> <count> (force|normal)
particle.add_variation(
    Parser(Block(), 'name'),
    Parser(Position(), 'position'),
    Parser(Position(), 'delta'),
    Parser(Double(), 'speed'),
    Parser(Integer(), 'count'),
    Parser(Union('force', 'normal'), 'mode'),
)
#  - particle <name> <pos> <delta> <speed> <count>
particle.add_variation(
    Parser(Block(), 'name'),
    Parser(Position(), 'position'),
    Parser(Position(), 'delta'),
    Parser(Double(), 'speed'),
    Parser(Integer(), 'count'),
)
