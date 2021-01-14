
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import DoubleNode, EntityNode, Position2dNode, RawNode
from ..parser_types import Double, Entity, Literal, Position2d, Union
from ..util import ensure_nodes


@dataclass()
class ParsedSpreadplayersCommand(ParsedCommand):
    command: str

    center: Position2dNode
    distance: DoubleNode
    range: DoubleNode
    teams: RawNode
    target: EntityNode

    under: RawNode = None
    height: DoubleNode = None

    def __str__(self):
        base = f'{self.command} {self.center} {self.distance} {self.range}'
        if self.under is not None:
            ensure_nodes(self, 'height')
            return f'{base} {self.under} {self.height} {self.teams} ' \
                   f'{self.target}'
        return f'{base} {self.teams} {self.target}'


spreadplayers = Command('spreadplayers', parsed=ParsedSpreadplayersCommand)

# spreadplayers <center> <spreadDistance> <maxRange> <respectTeams> <targets>
spreadplayers.add_variation(
    Parser(Position2d(), 'center'),
    Parser(Double(), 'distance'),  # technically a float, not double
    Parser(Double(), 'range'),
    Parser(Union('true', 'false'), 'teams'),
    Parser(Entity(), 'target'),
)
# spreadplayers <center> <spreadDistance> <maxRange> under <maxHeight>
#   <respectTeams> <targets>
spreadplayers.add_variation(
    Parser(Position2d(), 'center'),
    Parser(Double(), 'distance'),
    Parser(Double(), 'range'),
    Parser(Literal('under'), 'under'),
    Parser(Double(), 'height'),
    Parser(Union('true', 'false'), 'teams'),
    Parser(Entity(), 'target'),
)
