
import abc
import json
import re
import typing as t

from . import nodes
from .abc import Node
from .exceptions import ParserException
from .util import get, tokenize


class ParserType(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, parts: t.Iterator[str]) -> Node:
        raise NotImplementedError


class Any(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        return nodes.RawNode(get(parts))


class Block(ParserType):
    namespace = re.compile(
        r'(#?)([0-9a-z_.-]+:)?([0-9a-z_./-]+)(\[.*])?({.*})?'
    )

    def parse(self, parts: t.Iterator[str]) -> nodes.BlockNode:
        arg = get(parts)
        match = self.namespace.fullmatch(arg)
        if match is None:
            raise ParserException(
                f'expected valid block, not {arg!r}'
            )
        is_tag, namespace, name, blockstates, datatags = match.groups()
        if namespace is not None:
            namespace = namespace[:-1]  # remove ':'
        return nodes.BlockNode(bool(is_tag), namespace, name, blockstates,
                               datatags)


class Coordinate(ParserType):
    @classmethod
    def parse(cls, parts: t.Iterator[str]) -> nodes.CoordinateNode:
        arg = get(parts)
        try:
            if arg.startswith('~'):
                return nodes.CoordinateNode(
                    float(arg[1:]) if len(arg) > 1 else 0, relative=True
                )
            elif arg.startswith('^'):
                return nodes.CoordinateNode(
                    float(arg[1:]) if len(arg) > 1 else 0, local=True
                )
            return nodes.CoordinateNode(float(arg))
        except ValueError:
            raise ParserException(f'invalid coordinate: {arg!r}')


class GreedyAny(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        # return nodes.RawNode(' '.join(parts))
        seq = []
        for x in parts:
            seq.append(x)
        if not seq:
            raise ParserException('too few arguments')
        return nodes.RawNode(' '.join(seq))


class Double(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.DoubleNode:
        arg = get(parts)
        try:
            value = float(arg)
        except ValueError:
            raise ParserException(f'expected double, not {arg!r}')
        else:
            return nodes.DoubleNode(value)


class Entity(ParserType):
    valid_usernames = re.compile(r'[a-zA-Z0-9_]{3,16}')

    def parse(self, parts: t.Iterator[str]) -> nodes.EntityNode:
        arg = get(parts)
        selector = arg.split('[')[0]
        arguments = []

        if selector.startswith('@'):
            if selector[1:] not in 'aeprs':
                raise ParserException(f'invalid selector: {arg!r}')
        else:
            if (not self.valid_usernames.fullmatch(selector)
                    and not UUID.uuid.fullmatch(selector)):
                # may need some adjusting for chinese people
                raise ParserException(f'invalid username: {arg!r}')

        if '[' in arg:  # we got arguments
            if not arg.endswith(']'):
                raise ParserException(
                    f'expected \']\' at the end of valid entity: {arg!r}'
                )

            args = arg[len(selector) + 1:-1]
            arguments.extend(
                nodes.EntitySelectorConditionNode(*tokenize(name_value, '='))
                for name_value in tokenize(args, ',')
            )

        return nodes.EntityNode(selector, arguments)


class Function(ParserType):
    namespace = re.compile(r'(#?)([0-9a-z_.-]+):([0-9a-z_./-]+)')

    def parse(self, parts: t.Iterator[str]) \
            -> nodes.FunctionNode:
        arg = get(parts)
        match = self.namespace.fullmatch(arg)
        if match is None:
            raise ParserException(
                f'expected valid function, not {arg!r}'
            )
        is_tag, namespace, name = match.groups()
        return nodes.FunctionNode(bool(is_tag), namespace, name)


class IPAddress(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        arg = get(parts)
        ip_parts = arg.split('.')

        if len(ip_parts) != 4:
            raise ParserException('malformed ip address')

        try:
            ip_parts = [int(x) for x in ip_parts]
        except ValueError:
            raise ParserException('non number in ip address')

        if min(ip_parts) < 0 or max(ip_parts) > 255:
            raise ParserException('invalid ip address')

        return nodes.RawNode(arg)


class Integer(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.IntegerNode:
        arg = get(parts)
        try:
            value = int(arg)
        except ValueError:
            raise ParserException(f'expected integer, not {arg!r}')
        else:
            return nodes.IntegerNode(value)


class Item(ParserType):
    namespace = re.compile(r'(#?)([0-9a-z_.-]+:)?([0-9a-z_./-]+)({.*})?')

    def parse(self, parts: t.Iterator[str]) -> nodes.ItemNode:
        arg = get(parts)
        match = self.namespace.fullmatch(arg)
        if match is None:
            raise ParserException(
                f'expected valid item, not {arg!r}'
            )
        is_tag, namespace, name, datatags = match.groups()
        if namespace is not None:
            namespace = namespace[:-1]  # remove ':'
        return nodes.ItemNode(bool(is_tag), namespace, name, datatags)


class JSON(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.JSONNode:
        arg = get(parts)
        try:
            object = json.loads(arg)
        except json.JSONDecodeError:
            raise ParserException(f'expected valid json, not {arg!r}')

        return nodes.JSONNode(object)


class Literal(ParserType):
    def __init__(self, value: str):
        self._value = value

    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        arg = get(parts)
        if arg != self._value:
            raise ParserException(f'expected {self._value!r}, not {arg!r}')
        return nodes.RawNode(arg)


class NamespaceID(ParserType):
    namespace = re.compile(r'([0-9a-z_.-]+:)?([0-9a-z_./-]+)')

    def parse(self, parts: t.Iterator[str]) \
            -> nodes.NamespaceIDNode:
        arg = get(parts)
        match = self.namespace.fullmatch(arg)
        if match is None:
            raise ParserException(
                f'expected valid namespace identifier, not {arg!r}'
            )
        namespace, name = match.groups()
        if namespace is not None:
            namespace = namespace[:-1]  # remove ':'
        return nodes.NamespaceIDNode(namespace, name)


class Objective(ParserType):
    objective = re.compile(r'[a-zA-Z0-9_.+-]{,16}')

    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        arg = get(parts)
        match = self.objective.fullmatch(arg)
        if match is None:
            raise ParserException(f'expected valid objective, not {arg!r}')
        return nodes.RawNode(arg)


class Particle(ParserType):
    namespace = re.compile(r'([0-9a-z_.-]+:)?([0-9a-z_./-]+)')

    def parse(self, parts: t.Iterator[str]) -> nodes.ParticleNode:
        arg = get(parts)
        match = self.namespace.fullmatch(arg)
        if match is None:
            raise ParserException(
                f'expected valid particle, not {arg!r}'
            )
        namespace, name = match.groups()
        if namespace is not None:
            namespace = namespace[:-1]  # remove ':'

        arguments = None
        if namespace is None or namespace == 'minecraft':
            if name == 'dust':
                arguments = tuple(nodes.DoubleNode(float(x))
                                  for x in get(parts, 4))

            elif name in ('block', 'falling_dust'):
                match = Block.namespace.fullmatch(get(parts))
                arguments = (nodes.BlockNode(*match.groups()),)

            elif name == 'item':
                match = NamespaceID.namespace.fullmatch(get(parts))
                arguments = (nodes.NamespaceIDNode(*match.groups()),)

            elif name == 'vibration':
                arguments = (Position().parse(parts), Position().parse(parts),
                             Integer().parse(parts))

            elif name == 'dust_color_transition':
                arguments = tuple(nodes.DoubleNode(float(x))
                                  for x in get(parts, 7))

        return nodes.ParticleNode(namespace, name, arguments)


class Position(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.PositionNode:
        return nodes.PositionNode(Coordinate.parse(parts),
                                  Coordinate.parse(parts),
                                  Coordinate.parse(parts))


class Position2d(ParserType):
    def parse(self, parts: t.Iterator[str]) \
            -> nodes.Position2dNode:
        return nodes.Position2dNode(Coordinate.parse(parts),
                                    Coordinate.parse(parts))


class Rotation(ParserType):
    def parse(self, parts: t.Iterator[str]) -> nodes.RotationNode:
        return nodes.RotationNode(Coordinate.parse(parts),
                                  Coordinate.parse(parts))


class ScoreboardEntity(Entity):
    valid_usernames = re.compile(r'.+')


class Union(ParserType):
    def __init__(self, *options):
        self._options = options

    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        arg = get(parts)
        if arg not in self._options:
            raise ParserException(
                f'expected any of {self._options!r}, not {arg!r}'
            )
        return nodes.RawNode(arg)


class UUID(ParserType):
    uuid = re.compile('-'.join([r'[0-9a-fA-F]+'] * 5))

    def parse(self, parts: t.Iterator[str]) -> nodes.RawNode:
        arg = get(parts)
        match = self.uuid.fullmatch(arg)
        if match is None:
            raise ParserException(f'expected valid uuid, not {arg!r}')
        return nodes.RawNode(arg)
