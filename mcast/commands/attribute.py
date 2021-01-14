
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import DoubleNode, EntityNode, NamespaceIDNode, RawNode
from ..parser_types import (
    Any, Double, Entity, Literal, NamespaceID, Union, UUID
)
from ..util import ensure_nodes


@dataclass()
class ParsedAttributeCommand(ParsedCommand):
    command: str

    target: EntityNode
    attribute: NamespaceIDNode
    action: RawNode

    base_action: RawNode = None
    modifier_action: RawNode = None
    modifier_action2: RawNode = None

    name: RawNode = None
    value: DoubleNode = None
    uuid: RawNode = None
    scale: DoubleNode = None

    def __str__(self):
        base = f'{self.command} {self.target} {self.attribute} {self.action}'

        if self.action.value == 'get':
            if self.scale is not None:
                return f'{base} {self.scale}'
            return base

        elif self.action.value == 'base':
            command = f'{base} {self.base_action}'
            if self.base_action.value == 'set':
                ensure_nodes(self, 'value')
                return f'{command} {self.value}'

            elif self.base_action.value == 'get':
                if self.scale is not None:
                    return f'{command} {self.scale}'
                return command

            else:
                raise ConstructionException(
                    f'expected base_action to be \'set\' or \'get\', '
                    f'not {self.base_action.value!r}'
                )

        elif self.action.value == 'modifier':
            command = f'{base} {self.modifier_action}'
            if self.modifier_action.value == 'add':
                ensure_nodes(
                    self, 'uuid', 'name', 'value', 'modifier_action2'
                )
                return f'{command} {self.uuid} {self.name} {self.value} ' \
                       f'{self.modifier_action2}'

            elif self.modifier_action.value == 'remove':
                ensure_nodes(self, 'uuid')
                return f'{command} {self.uuid}'

            elif self.modifier_action.value == 'get':
                ensure_nodes(self, 'uuid')
                if self.scale is not None:
                    return f'{command} {self.uuid} {self.scale}'
                return f'{command} {self.uuid}'

            else:
                raise ConstructionException(
                    f'expected modifier_action to be \'add\', \'remove\' or '
                    f'\'get\', not {self.modifier_action.value!r}'
                )


attribute = Command('attribute', parsed=ParsedAttributeCommand)

# attribute <target> <attribute> get [<scale>]
#  - attribute <target> <attribute> get <scale>
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('get'), 'action'),
    Parser(Double(), 'scale'),
)
#  - attribute <target> <attribute> get
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('get'), 'action'),
)

# attribute <target> <attribute> base get [<scale>]
#  - attribute <target> <attribute> base get <scale>
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('base'), 'action'),
    Parser(Literal('get'), 'base_action'),
    Parser(Double(), 'scale'),
)
#  - attribute <target> <attribute> base get
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('base'), 'action'),
    Parser(Literal('get'), 'base_action'),
)

# attribute <target> <attribute> base set <value>
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('base'), 'action'),
    Parser(Literal('set'), 'base_action'),
    Parser(Double(), 'value')
)

# I am quite confused about this command's <name>, and why it uses <uuid>
#   instead of ... idk, namespace?
# attribute <target> <attribute> modifier add <uuid> <name> <value>
#   (add|multiply|multiply_base)
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('modifier'), 'action'),
    Parser(Literal('add'), 'modifier_action'),
    Parser(UUID(), 'uuid'),
    Parser(Any(), 'name'),  # <--- what does this even do
    Parser(Double(), 'value'),
    Parser(Union('add', 'multiply', 'multiply_base'), 'modifier_action2'),
)

# attribute <target> <attribute> modifier remove <uuid>
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('modifier'), 'action'),
    Parser(Literal('remove'), 'modifier_action'),
    Parser(UUID(), 'uuid'),
)

# attribute <target> <attribute> modifier value get <uuid> [<scale>]
#  - attribute <target> <attribute> modifier value get <uuid> <scale>
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('modifier'), 'action'),
    Parser(Literal('get'), 'modifier_action'),
    Parser(UUID(), 'uuid'),
    Parser(Double(), 'scale'),
)
#  - attribute <target> <attribute> modifier value get <uuid>
attribute.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'attribute'),
    Parser(Literal('modifier'), 'action'),
    Parser(Literal('get'), 'modifier_action'),
    Parser(UUID(), 'uuid'),
)
