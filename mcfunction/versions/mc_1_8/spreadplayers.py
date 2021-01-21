
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import DoubleNode, EntityNode, Position2dNode, RawNode
from ...parser_types import Double, Entity, Position2d, Union


@dataclass()
class ParsedSpreadplayersCommand(ParsedCommand):
    command: str

    center: Position2dNode
    distance: DoubleNode
    range: DoubleNode
    teams: RawNode
    target: EntityNode

    def __str__(self):
        return f'{self.command} {self.center} {self.distance} {self.range} ' \
               f'{self.teams} {self.target}'


spreadplayers = Command('spreadplayers', parsed=ParsedSpreadplayersCommand)

# spreadplayers <center> <spreadDistance> <maxRange> <respectTeams> <targets>
spreadplayers.add_variation(
    Parser(Position2d(), 'center'),
    Parser(Double(), 'distance'),
    Parser(Double(), 'range'),
    Parser(Union('true', 'false'), 'teams'),
    Parser(Entity(), 'target'),
)
