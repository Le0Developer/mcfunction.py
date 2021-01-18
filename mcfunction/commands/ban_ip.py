
from dataclasses import dataclass
import typing as t

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, RawNode
from ..parser_types import Entity, GreedyAny, IPAddress


@dataclass()
class ParsedIPBanCommand(ParsedCommand):
    command: str

    target: t.Union[RawNode, EntityNode]

    reason: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.target}'
        if self.reason is not None:
            return f'{base} {self.reason}'
        return base


ban_ip = Command('ban-ip', commandblock=False, parsed=ParsedIPBanCommand)

# target referring to an ip address

# ban-ip <targets> [<reason>]
#  - ban-ip <targets> <reason>
ban_ip.add_variation(
    Parser(IPAddress(), 'target'),
    Parser(GreedyAny(), 'reason'),
)
#  - ban-ip <targets>
ban_ip.add_variation(
    Parser(IPAddress(), 'target'),
)

# with target referring to a player

# ban-ip <targets> [<reason>]
#  - ban-ip <targets> <reason>
ban_ip.add_variation(
    Parser(Entity(), 'target'),
    Parser(GreedyAny(), 'reason'),
)
#  - ban-ip <targets>
ban_ip.add_variation(
    Parser(Entity(), 'target'),
)
