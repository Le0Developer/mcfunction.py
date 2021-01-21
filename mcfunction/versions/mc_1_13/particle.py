
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import (
    DoubleNode, EntityNode, IntegerNode, ParticleNode, PositionNode, RawNode
)
from ...parser_types import Double, Entity, Integer, Particle, Position, Union
from ...util import ensure_nodes


@dataclass()
class ParsedParticleCommand(ParsedCommand):
    command: str

    name: ParticleNode

    position: PositionNode = None
    delta: PositionNode = None
    speed: DoubleNode = None
    count: IntegerNode = None
    mode: RawNode = None
    viewers: EntityNode = None

    def __str__(self):
        base = f'{self.command} {self.name}'
        if self.position is None:
            return base
        if self.delta is None:
            return f'{base} {self.position}'

        ensure_nodes(self, 'speed', 'count')
        base = f'{base} {self.position} {self.delta} {self.speed} {self.count}'
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
    Parser(Particle(), 'name'),
    Parser(Position(), 'position'),
    Parser(Position(), 'delta'),
    Parser(Double(), 'speed'),
    Parser(Integer(), 'count'),
    Parser(Union('force', 'normal'), 'mode'),
    Parser(Entity(), 'viewers'),
)
#  - particle <name> <pos> <delta> <speed> <count> (force|normal)
particle.add_variation(
    Parser(Particle(), 'name'),
    Parser(Position(), 'position'),
    Parser(Position(), 'delta'),
    Parser(Double(), 'speed'),
    Parser(Integer(), 'count'),
    Parser(Union('force', 'normal'), 'mode'),
)
#  - particle <name> <pos> <delta> <speed> <count>
particle.add_variation(
    Parser(Particle(), 'name'),
    Parser(Position(), 'position'),
    Parser(Position(), 'delta'),
    Parser(Double(), 'speed'),
    Parser(Integer(), 'count'),
)
#  - particle <name> <pos>
particle.add_variation(
    Parser(Particle(), 'name'),
    Parser(Position(), 'position'),
)
#  - particle <name>
particle.add_variation(
    Parser(Particle(), 'name'),
)
