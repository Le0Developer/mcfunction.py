
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import IntegerNode, RawNode
from ...parser_types import Integer, Union, Objective
from ...util import ensure_nodes


@dataclass()
class ParsedTriggerCommand(ParsedCommand):
    command: str

    objective: RawNode

    action: RawNode = None
    value: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.objective}'
        if self.action is not None:
            ensure_nodes(self, 'value')
            return f'{base} {self.action} {self.value}'
        return base


trigger = Command('trigger', parsed=ParsedTriggerCommand)

# trigger <objective>
trigger.add_variation(
    Parser(Objective(), 'objective')
)

# trigger <objective> add <value>
# trigger <objective> set <value>
trigger.add_variation(
    Parser(Objective(), 'objective'),
    Parser(Union('add', 'set'), 'action'),
    Parser(Integer(), 'value'),
)
