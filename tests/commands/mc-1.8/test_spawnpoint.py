
from mcfunction.versions.mc_1_8.spawnpoint import (
    spawnpoint, ParsedSpawnpointCommand
)
from mcfunction.nodes import EntityNode, PositionNode


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
