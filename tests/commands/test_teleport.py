
from mcfunction.versions.mc_1_13.teleport import (
    teleport, ParsedTeleportCommand
)
from mcfunction.nodes import EntityNode, PositionNode, RotationNode


def test_teleport_destination():
    parsed = teleport.parse('teleport @s')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.destination, EntityNode)

    assert str(parsed) == 'teleport @s'


def test_teleport_location():
    parsed = teleport.parse('teleport 0 0 0')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.destination, PositionNode)

    assert str(parsed) == 'teleport 0 0 0'


def test_teleport_target_destination():
    parsed = teleport.parse('teleport @s @s')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, EntityNode)

    assert str(parsed) == 'teleport @s @s'


def test_teleport_target_location():
    parsed = teleport.parse('teleport @s 0 0 0')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, PositionNode)

    assert str(parsed) == 'teleport @s 0 0 0'


def test_teleport_target_location_rotation():
    parsed = teleport.parse('teleport @s 0 0 0 1 1')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, PositionNode)
    assert isinstance(parsed.rotation, RotationNode)

    assert str(parsed) == 'teleport @s 0 0 0 1 1'


def test_teleport_target_location_facing_location():
    parsed = teleport.parse('teleport @s 0 0 0 facing 1 1 1')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, PositionNode)
    assert isinstance(parsed.facing, PositionNode)

    assert str(parsed) == 'teleport @s 0 0 0 facing 1 1 1'


def test_teleport_target_location_facing_entity():
    parsed = teleport.parse('teleport @s 0 0 0 facing entity @s')
    parsed: ParsedTeleportCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, PositionNode)
    assert isinstance(parsed.facing, EntityNode)

    assert str(parsed) == 'teleport @s 0 0 0 facing entity @s'


def test_teleport_target_location_facing_entity_anchor():
    parsed = teleport.parse('teleport @s 0 0 0 facing entity @s eyes')
    parsed: ParsedTeleportCommand

    assert parsed.anchor.value == 'eyes'

    assert str(parsed) == 'teleport @s 0 0 0 facing entity @s eyes'
