from __future__ import annotations

import json
import typing as t

from .abc import Node
from .util import clean


class BlockNode(Node):
    def __init__(self, is_tag: bool, namespace: t.Optional[str],
                 name: t.Optional[str], blockstates: t.Optional[str],
                 datatags: t.Optional[str]):
        self.is_tag = is_tag
        self.namespace = namespace
        self.name = name
        self.blockstates = blockstates
        self.datatags = datatags

    def __str__(self):
        base = '#' if self.is_tag else ''
        if self.namespace is None:
            base = f'{base}{self.name}'
        else:
            base = f'{base}{self.namespace}:{self.name}'
        if self.blockstates is not None:
            base = f'{base}{self.blockstates}'
        if self.datatags is None:
            return base
        return f'{base}{self.datatags}'


class CoordinateNode:
    def __init__(self, value: float, relative: bool = False,
                 local: bool = False):
        self.value = value
        self.relative = relative
        self.local = local

    def __str__(self):
        if self.relative:
            return clean(f'~{self.value:f}') if self.value else '~'
        elif self.local:
            return clean(f'^{self.value:f}') if self.value else '^'
        return clean(f'{self.value:f}')


class EntityNode(Node):
    def __init__(self, selector: str,
                 conditions: t.Optional[t.List[EntitySelectorConditionNode]]):
        self.selector = selector
        self.conditions = conditions

    def is_username(self):
        return not self.selector.startswith('@')

    def __str__(self):
        if self.conditions:
            conditions = ','.join(str(x) for x in self.conditions)
            return f'{self.selector}[{conditions}]'
        return self.selector


class EntitySelectorConditionNode(Node):
    def __init__(self, name: str, value: t.Any):
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.name}={self.value}'


class FunctionNode(Node):
    def __init__(self, is_tag: bool, namespace: str, name: str):
        self.is_tag = is_tag
        self.namespace = namespace
        self.name = name

    def __str__(self):
        base = '#' if self.is_tag else ''
        return f'{base}{self.namespace}:{self.name}'


class ItemNode(Node):
    def __init__(self, is_tag: bool, namespace: t.Optional[str], name: str,
                 datatags: t.Optional[str]):
        self.is_tag = is_tag
        self.namespace = namespace
        self.name = name
        self.datatags = datatags

    def __str__(self):
        base = '#' if self.is_tag else ''
        if self.namespace is None:
            base = f'{base}{self.name}'
        else:
            base = f'{base}{self.namespace}:{self.name}'
        if self.datatags is None:
            return base
        return f'{base}{self.datatags}'


class JSONNode(Node):
    def __init__(self, object):
        self.object = object

    def __str__(self):
        return json.dumps(self.object, separators=(',', ':'),
                          ensure_ascii=False)


class NamespaceIDNode(Node):
    def __init__(self, namespace: t.Optional[str], name: str):
        self.namespace = namespace
        self.name = name

    def __str__(self):
        if self.namespace is None:
            return self.name
        return f'{self.namespace}:{self.name}'


class ParticleNode(NamespaceIDNode):
    def __init__(self, namespace: t.Optional[str], name: str,
                 arguments: t.Optional[t.Sequence[Node]]):
        super().__init__(namespace, name)
        self.arguments = arguments

    def __str__(self):
        base = super().__str__()
        if self.arguments:
            arguments = ' '.join(str(x) for x in self.arguments)
            return f'{base} {arguments}'
        return base


class PositionNode(Node):
    def __init__(self, x: CoordinateNode, y: CoordinateNode,
                 z: CoordinateNode):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'{self.x} {self.y} {self.z}'


class Position2dNode(Node):
    def __init__(self, x: CoordinateNode, z: CoordinateNode):
        self.x = x
        self.z = z

    def __str__(self):
        return f'{self.x} {self.z}'


class RawNode(Node):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value


class RotationNode(Node):
    def __init__(self, yaw: CoordinateNode, pitch: CoordinateNode):
        self.yaw = yaw
        self.pitch = pitch

    def __str__(self):
        return f'{self.yaw} {self.pitch}'


class ValueNode(Node):
    def __init__(self, value: t.Any):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class DoubleNode(ValueNode):
    value: float

    def __str__(self):
        return clean(f'{self.value:.14f}')


class IntegerNode(ValueNode):
    value: int
