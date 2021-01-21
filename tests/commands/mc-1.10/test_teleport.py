
from mcfunction.versions.mc_1_10.teleport import (
    teleport, ParsedTeleportCommand
)
from mcfunction.nodes import EntityNode, PositionNode, RotationNode


def test_teleport():
    parsed = teleport.parse('teleport @r')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'teleport @r'


def test_teleport_position():
    parsed = teleport.parse('teleport @s 0 0 0')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'teleport @s 0 0 0'


def test_teleport_rotation():
    parsed = teleport.parse('teleport @s 0 0 0 1 1')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.position, PositionNode)
    assert isinstance(parsed.rotation, RotationNode)

    assert str(parsed) == 'teleport @s 0 0 0 1 1'
