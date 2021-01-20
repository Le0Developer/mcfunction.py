
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import IntegerNode, RawNode
from ...parser_types import Integer, Union


@dataclass()
class ParsedWeatherCommand(ParsedCommand):
    command: str

    weather: RawNode

    duration: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.weather}'
        if self.duration is not None:
            return f'{base} {self.duration}'
        return base


weather = Command('weather', parsed=ParsedWeatherCommand)

# weather (clear|rain|thunder) [<duration>]
#  - weather (clear|rain|thunder) <duration>
weather.add_variation(
    Parser(Union('clear', 'rain', 'thunder'), 'weather'),
    Parser(Integer(), 'duration'),
)
#  - weather (clear|rain|thunder)
weather.add_variation(
    Parser(Union('clear', 'rain', 'thunder'), 'weather'),
)
