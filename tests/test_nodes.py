
from mcfunction import nodes


class TestBlockNode:
    def test_name(self):
        node = nodes.BlockNode(False, None, 'block', None, None)
        assert str(node) == 'block'

    def test_namespace(self):
        node = nodes.BlockNode(False, 'test', 'block', None, None)
        assert str(node) == 'test:block'

    def test_tag(self):
        node = nodes.BlockNode(True, 'test', 'block', None, None)
        assert str(node) == '#test:block'

    def test_blockstates(self):
        node = nodes.BlockNode(False, 'test', 'block', '[power=69]', None)
        assert str(node) == 'test:block[power=69]'

    def test_datatags(self):
        node = nodes.BlockNode(False, 'test', 'block', None, '{value:69}')
        assert str(node) == 'test:block{value:69}'

    def test_blockstates_datatags(self):
        node = nodes.BlockNode(False, 'test', 'block', '[power=69]',
                               '{value:69}')
        assert str(node) == 'test:block[power=69]{value:69}'


class TestCoordinateNode:
    def test_normal(self):
        node = nodes.CoordinateNode(42)
        assert str(node) == '42'

    def test_relative(self):
        node = nodes.CoordinateNode(42, relative=True)
        assert str(node) == '~42'

    def test_local(self):
        node = nodes.CoordinateNode(4.2, local=True)
        assert str(node) == '^4.2'


class TestEntityNode:
    def test_username(self):
        entity = nodes.EntityNode('testuser', None)
        assert str(entity) == 'testuser'
        assert entity.is_username()

    def test_selector(self):
        entity = nodes.EntityNode('@a', None)
        assert str(entity) == '@a'
        assert not entity.is_username()

    def test_conditions(self):
        entity = nodes.EntityNode('@e', [
            nodes.EntitySelectorConditionNode('type', 'player'),
            nodes.EntitySelectorConditionNode('distance', '..3')
        ])
        assert str(entity) == '@e[type=player,distance=..3]'


class TestFunctionNode:
    def test_namespace(self):
        function = nodes.FunctionNode(False, 'test', 'function')
        assert str(function) == 'test:function'

    def test_tag(self):
        function = nodes.FunctionNode(True, 'test', 'function')
        assert str(function) == '#test:function'


class TestItemNode:
    def test_name(self):
        item = nodes.ItemNode(False, None, 'item', None)
        assert str(item) == 'item'

    def test_namespace(self):
        item = nodes.ItemNode(False, 'test', 'item', None)
        assert str(item) == 'test:item'

    def test_tag(self):
        item = nodes.ItemNode(True, 'test', 'item', None)
        assert str(item) == '#test:item'

    def test_datatags(self):
        item = nodes.ItemNode(False, 'test', 'item', '{value:69}')
        assert str(item) == 'test:item{value:69}'


def test_json_node():
    json = nodes.JSONNode({'text': 'test successful'})
    assert str(json) == '{"text":"test successful"}'


class TestNamespaceIDNode:
    def test_name(self):
        namespaceid = nodes.NamespaceIDNode(None, 'name')
        assert str(namespaceid) == 'name'

    def test_namespace(self):
        namespaceid = nodes.NamespaceIDNode('namespace', 'name')
        assert str(namespaceid) == 'namespace:name'


class TestParticle:
    def test_name(self):
        particle = nodes.ParticleNode(None, 'name', None)
        assert str(particle) == 'name'

    def test_namespace(self):
        particle = nodes.ParticleNode('namespace', 'name', None)
        assert str(particle) == 'namespace:name'

    def test_arguments(self):
        particle = nodes.ParticleNode('namespace', 'name', (
            nodes.RawNode('stay'),
            nodes.RawNode('safe'),
        ))
        assert str(particle) == 'namespace:name stay safe'


def test_position_node():
    position = nodes.PositionNode(
        nodes.CoordinateNode(0),
        nodes.CoordinateNode(1),
        nodes.CoordinateNode(2)
    )
    assert str(position) == '0 1 2'


def test_position2d_node():
    position2d = nodes.Position2dNode(
        nodes.CoordinateNode(0),
        nodes.CoordinateNode(1)
    )
    assert str(position2d) == '0 1'


def test_raw_node():
    raw = nodes.RawNode('anything can be here')
    assert str(raw) == 'anything can be here'


def test_rotation_node():
    rotation = nodes.RotationNode(
        nodes.CoordinateNode(0),
        nodes.CoordinateNode(1)
    )
    assert str(rotation) == '0 1'


def test_value_node():
    value = nodes.ValueNode(1.23)
    assert str(value) == '1.23'
