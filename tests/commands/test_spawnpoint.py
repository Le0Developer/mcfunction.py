
from mcfunction.commands.spawnpoint import spawnpoint, ParsedSpawnpointCommand
from mcfunction.nodes import EntityNode, PositionNode, RotationNode


def test_spawnpoint():
    parsed = spawnpoint.parse('spawnpoint')
    parsed: ParsedSpawnpointCommand

    assert str(parsed) == 'spawnpoint'


def test_spawnpoint_target():
    parsed = spawnpoint.parse('spawnpoint @s')
    parsed: ParsedSpawnpointCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'spawnpoint @s'


def test_spawnpoint_position():
    parsed = spawnpoint.parse('spawnpoint @s 0 0 0')
    parsed: ParsedSpawnpointCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'spawnpoint @s 0 0 0'


def test_spawnpoint_angle():
    parsed = spawnpoint.parse('spawnpoint @s 0 0 0 1 1')
    parsed: ParsedSpawnpointCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.position, PositionNode)
    assert isinstance(parsed.angle, RotationNode)

    assert str(parsed) == 'spawnpoint @s 0 0 0 1 1'
