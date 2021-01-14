
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, RawNode
from ..parser_types import Entity, Union
from ..util import ensure_nodes


@dataclass()
class ParsedWhitelistCommand(ParsedCommand):
    command: str

    action: RawNode

    target: EntityNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value in ('add', 'remove'):
            ensure_nodes(self, 'target')
            return f'{base} {self.target}'
        return base


whitelist = Command('whitelist', parsed=ParsedWhitelistCommand)

# whitelist (add|remove) <targets>
whitelist.add_variation(
    Parser(Union('add', 'remove'), 'action'),
    Parser(Entity(), 'target'),
)
# whitelist (list|off|on|reload)
whitelist.add_variation(
    Parser(Union('list', 'off', 'on', 'reload'), 'action'),
)
