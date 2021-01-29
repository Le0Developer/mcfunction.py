
import pytest

from mcfunction import nodes, parser_types
from mcfunction.exceptions import ParserException
from mcfunction.util import get


def test_any():
    any = parser_types.Any()
    parts = iter(('part0', 'part1'))

    node = any.parse(parts)
    assert node.value == 'part0'

    assert get(parts) == 'part1'


def test_block():
    block = parser_types.Block()
    parts = iter((
        'test:block',
        'test:block[power=69]{value:69}',
        '#test:blocks',
        'not quite valid block'
    ))

    node = block.parse(parts)
    assert not node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'block'
    assert node.blockstates is None
    assert node.datatags is None

    node = block.parse(parts)
    assert not node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'block'
    assert node.blockstates == '[power=69]'
    assert node.datatags == '{value:69}'

    node = block.parse(parts)
    assert node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'blocks'
    assert node.blockstates is None
    assert node.datatags is None

    with pytest.raises(ParserException, match='expected valid block, not .*'):
        block.parse(parts)


# TODO: Coordinate test
# NOTE: it already has 100% coverage thanks to Position(), Position2d(), ...
#   tests


def test_greedyany():
    greedyany = parser_types.GreedyAny()
    parts = iter(('part0', 'part1'))

    node = greedyany.parse(parts)
    assert node.value == 'part0 part1'

    with pytest.raises(ParserException, match='too few arguments'):
        greedyany.parse(parts)

    # ensure all parts have been used
    with pytest.raises(StopIteration):
        get(parts)


def test_double():
    double = parser_types.Double()
    parts = iter(('69', '6.9', 'not a double'))

    node = double.parse(parts)
    assert node.value == 69

    node = double.parse(parts)
    assert node.value == 6.9

    with pytest.raises(ParserException, match='expected double, not .*'):
        double.parse(parts)


def test_entity():
    entity = parser_types.Entity()
    parts = iter((
        'TestUser',
        '0-0-0-0-0',
        '@r',
        '@e[type=player]',
        '@everyone',
        'a',
        'something invalid',
        'TestUser['
    ))

    node = entity.parse(parts)
    assert node.selector == 'TestUser'
    assert not node.conditions

    node = entity.parse(parts)
    assert node.selector == '0-0-0-0-0'
    assert not node.conditions

    node = entity.parse(parts)
    assert node.selector == '@r'
    assert not node.conditions

    node = entity.parse(parts)
    assert node.selector == '@e'
    assert node.conditions[0].name == 'type'
    assert node.conditions[0].value == 'player'

    # @everyone
    with pytest.raises(ParserException, match='invalid selector: .*'):
        entity.parse(parts)

    # a  (too short)
    with pytest.raises(ParserException, match='invalid username: .*'):
        entity.parse(parts)
    # something invalid  (space)
    with pytest.raises(ParserException, match='invalid username: .*'):
        entity.parse(parts)

    # TestUser[  (malformed)
    with pytest.raises(ParserException,
                       match='expected \']\' at the end of valid entity: .*'):
        entity.parse(parts)


def test_function():
    function = parser_types.Function()
    parts = iter((
        'test:function',
        'test:directory/function',
        '#test:events/on_tick',
        'something invalid'
    ))

    node = function.parse(parts)
    assert not node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'function'

    node = function.parse(parts)
    assert not node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'directory/function'

    node = function.parse(parts)
    assert node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'events/on_tick'

    with pytest.raises(ParserException):
        function.parse(parts)


def test_ip_address():
    ip = parser_types.IPAddress()
    parts = iter((
        '127.0.0.1',
        '0.0.0.0',
        '255.255.255.255',
        '256.255.255.255',
        '-1.0.0.0',
        'i.i.i.i',
        'invalid'
    ))

    node = ip.parse(parts)
    assert node.value == '127.0.0.1'
    node = ip.parse(parts)
    assert node.value == '0.0.0.0'
    node = ip.parse(parts)
    assert node.value == '255.255.255.255'

    with pytest.raises(ParserException, match='invalid ip address'):
        ip.parse(parts)
    with pytest.raises(ParserException, match='invalid ip address'):
        ip.parse(parts)

    with pytest.raises(ParserException, match='non number in ip address'):
        ip.parse(parts)

    with pytest.raises(ParserException, match='malformed ip address'):
        ip.parse(parts)


def test_integer():
    integer = parser_types.Integer()
    parts = iter((
        '69',
        '6.9',
        'not a number'
    ))

    node = integer.parse(parts)
    assert node.value == 69

    with pytest.raises(ParserException, match='expected integer, not .*'):
        integer.parse(parts)
    with pytest.raises(ParserException, match='expected integer, not .*'):
        integer.parse(parts)


def test_item():
    item = parser_types.Item()
    parts = iter((
        'test:item',
        'test:item{value:69}',
        '#test:items',
        'not valid'
    ))

    node = item.parse(parts)
    assert not node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'item'
    assert node.datatags is None

    node = item.parse(parts)
    assert not node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'item'
    assert node.datatags == '{value:69}'

    node = item.parse(parts)
    assert node.is_tag
    assert node.namespace == 'test'
    assert node.name == 'items'
    assert node.datatags is None

    with pytest.raises(ParserException, match='expected valid item, not .*'):
        item.parse(parts)


def test_json():
    json = parser_types.JSON()
    parts = iter((
        '"test successful"',
        '{"text":"test successful"}',
        'test fails'
    ))

    node = json.parse(parts)
    assert node.object == 'test successful'

    node = json.parse(parts)
    assert node.object == {'text': 'test successful'}

    with pytest.raises(ParserException, match='expected valid json, not .*'):
        json.parse(parts)


def test_literal():
    literal = parser_types.Literal('valid')
    parts = iter((
        'valid',
        'not valid'
    ))

    node = literal.parse(parts)
    assert node.value == 'valid'

    with pytest.raises(ParserException, match='expected .*, not .*'):
        literal.parse(parts)


def test_namespaceid():
    namespaceid = parser_types.NamespaceID()
    parts = iter((
        'namespace_is_optional',
        'namespace:name',
        'test:a/b/c',
        'INVALID'
    ))

    node = namespaceid.parse(parts)
    assert node.namespace is None
    assert node.name == 'namespace_is_optional'

    node = namespaceid.parse(parts)
    assert node.namespace == 'namespace'
    assert node.name == 'name'

    node = namespaceid.parse(parts)
    assert node.namespace == 'test'
    assert node.name == 'a/b/c'

    with pytest.raises(ParserException,
                       match='expected valid namespace identifier, not .*'):
        namespaceid.parse(parts)


def test_objective():
    objective = parser_types.Objective()
    parts = iter((
        'testobjective',
        'waaaaay-tooo-looooooong',
        'invalid-character:'
    ))

    node = objective.parse(parts)
    assert node.value == 'testobjective'

    with pytest.raises(ParserException,
                       match='expected valid objective, not .*'):
        objective.parse(parts)
    with pytest.raises(ParserException,
                       match='expected valid objective, not .*'):
        objective.parse(parts)


def test_particle():
    particle = parser_types.Particle()
    parts = iter((
        'test:particle',
        'test:dust',
        'minecraft:dust', '0', '1', '2', '3',
        'minecraft:block', 'test:block',
        'minecraft:falling_dust', 'test:block',
        'minecraft:item', 'test:item',
        'minecraft:vibration', '0', '0', '0', '1', '1', '1', '2',
        'minecraft:dust_color_transition', '0', '1', '2', '3', '4', '5', '6',
        'invalid particle',
        'minecraft:dust'
    ))

    node = particle.parse(parts)
    assert node.namespace == 'test'
    assert node.name == 'particle'
    assert not node.arguments

    node = particle.parse(parts)
    assert node.namespace == 'test'
    assert node.name == 'dust'
    assert not node.arguments

    node = particle.parse(parts)
    assert node.namespace == 'minecraft'
    assert node.name == 'dust'
    assert [x.value for x in node.arguments] == [0, 1, 2, 3]

    node = particle.parse(parts)
    assert node.namespace == 'minecraft'
    assert node.name == 'block'
    assert isinstance(node.arguments[0], nodes.BlockNode)

    node = particle.parse(parts)
    assert node.namespace == 'minecraft'
    assert node.name == 'falling_dust'
    assert isinstance(node.arguments[0], nodes.BlockNode)

    node = particle.parse(parts)
    assert node.namespace == 'minecraft'
    assert node.name == 'item'
    assert isinstance(node.arguments[0], nodes.NamespaceIDNode)

    node = particle.parse(parts)
    assert node.namespace == 'minecraft'
    assert node.name == 'vibration'
    assert isinstance(node.arguments[0], nodes.PositionNode)
    assert isinstance(node.arguments[1], nodes.PositionNode)
    assert isinstance(node.arguments[2], nodes.IntegerNode)

    node = particle.parse(parts)
    assert node.namespace == 'minecraft'
    assert node.name == 'dust_color_transition'
    assert [x.value for x in node.arguments] == [0, 1, 2, 3, 4, 5, 6]

    with pytest.raises(ParserException,
                       match='expected valid particle, not .*'):
        particle.parse(parts)

    with pytest.raises(StopIteration):
        particle.parse(parts)


def test_position():
    position = parser_types.Position()
    parts = iter((
        '0', '0', '0',
        '~', '~', '~',
        '^.1', '^0.1', '^0.00000000001',
        'a',
        '1'
    ))

    node = position.parse(parts)
    assert node.x.value == 0
    assert not node.x.relative and not node.x.local
    assert node.y.value == 0
    assert not node.y.relative and not node.y.local
    assert node.z.value == 0
    assert not node.z.relative and not node.z.local

    node = position.parse(parts)
    assert node.x.value == 0
    assert node.x.relative and not node.x.local
    assert node.y.value == 0
    assert node.y.relative and not node.y.local
    assert node.z.value == 0
    assert node.z.relative and not node.z.local

    node = position.parse(parts)
    assert node.x.value == 0.1
    assert not node.x.relative and node.x.local
    assert node.y.value == 0.1
    assert not node.y.relative and node.y.local
    assert node.z.value == 0.00000000001
    assert not node.z.relative and node.z.local

    with pytest.raises(ParserException, match='invalid coordinate: .*'):
        position.parse(parts)

    with pytest.raises(StopIteration):
        position.parse(parts)


def test_position2d():
    position2d = parser_types.Position2d()
    parts = iter((
        '0', '0',
        '~', '~',
        '^.1', '^0.1',
        'a',
        '1'
    ))

    node = position2d.parse(parts)
    assert node.x.value == 0
    assert not node.x.relative and not node.x.local
    assert node.z.value == 0
    assert not node.z.relative and not node.z.local

    node = position2d.parse(parts)
    assert node.x.value == 0
    assert node.x.relative and not node.x.local
    assert node.z.value == 0
    assert node.z.relative and not node.z.local

    node = position2d.parse(parts)
    assert node.x.value == 0.1
    assert not node.x.relative and node.x.local
    assert node.z.value == 0.1
    assert not node.z.relative and node.z.local

    with pytest.raises(ParserException, match='invalid coordinate: .*'):
        position2d.parse(parts)

    with pytest.raises(StopIteration):
        position2d.parse(parts)


def test_scoreboardentity():
    scoreboardentity = parser_types.ScoreboardEntity()
    parts = iter((
        'Player',
        '*',
        'A' * 256,
        '⨁',
        ''
    ))

    node = scoreboardentity.parse(parts)
    assert node.selector == 'Player'

    node = scoreboardentity.parse(parts)
    assert node.selector == '*'

    node = scoreboardentity.parse(parts)
    assert node.selector == 'A' * 256

    node = scoreboardentity.parse(parts)
    assert node.selector == '⨁'

    with pytest.raises(ParserException, match='invalid username: .*'):
        scoreboardentity.parse(parts)


def test_rotation():
    rotation = parser_types.Rotation()
    parts = iter((
        '0', '0',
        '~', '~',
        '^.1', '^0.1',
        'a',
        '1'
    ))

    node = rotation.parse(parts)
    assert node.yaw.value == 0
    assert not node.yaw.relative and not node.yaw.local
    assert node.pitch.value == 0
    assert not node.pitch.relative and not node.pitch.local

    node = rotation.parse(parts)
    assert node.pitch.value == 0
    assert node.pitch.relative and not node.pitch.local
    assert node.pitch.value == 0
    assert node.pitch.relative and not node.pitch.local

    node = rotation.parse(parts)
    assert node.pitch.value == 0.1
    assert not node.pitch.relative and node.pitch.local
    assert node.pitch.value == 0.1
    assert not node.pitch.relative and node.pitch.local

    with pytest.raises(ParserException, match='invalid coordinate: .*'):
        rotation.parse(parts)

    with pytest.raises(StopIteration):
        rotation.parse(parts)


def test_union():
    union = parser_types.Union('valid', 'valid_too', 'valid_three')
    parts = iter((
        'valid',
        'valid_too',
        'valid_three',
        'valid_four'
    ))

    node = union.parse(parts)
    assert node.value == 'valid'
    node = union.parse(parts)
    assert node.value == 'valid_too'
    node = union.parse(parts)
    assert node.value == 'valid_three'

    with pytest.raises(ParserException, match='expected any of .*, not .*'):
        union.parse(parts)


def test_uuid():
    uuid = parser_types.UUID()
    parts = iter((
        '2eb4b815-7a3c-4cf2-8845-bbc03b10ee35',
        '1-2-3-4-5',
        'a-b-c-d-e',
        'A-B-C-D-E',
        'invalid'
    ))

    node = uuid.parse(parts)
    assert node.value == '2eb4b815-7a3c-4cf2-8845-bbc03b10ee35'

    node = uuid.parse(parts)
    assert node.value == '1-2-3-4-5'

    node = uuid.parse(parts)
    assert node.value == 'a-b-c-d-e'

    node = uuid.parse(parts)
    assert node.value == 'A-B-C-D-E'

    with pytest.raises(ParserException, match='expected valid uuid, not .*'):
        uuid.parse(parts)
