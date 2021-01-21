
from mcfunction.versions.mc_1_8.playsound import (
    playsound, ParsedPlaysoundCommand
)
from mcfunction.nodes import EntityNode, PositionNode


def test_playsound():
    parsed = playsound.parse('playsound test:sound @s')
    parsed: ParsedPlaysoundCommand

    assert parsed.sound.namespace == 'test'
    assert parsed.sound.name == 'sound'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'playsound test:sound @s'


def test_playsound_position():
    parsed = playsound.parse('playsound test:sound @s 0 0 0')
    parsed: ParsedPlaysoundCommand

    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'playsound test:sound @s 0 0 0'


def test_playsound_volume():
    parsed = playsound.parse('playsound test:sound @s 0 0 0 1')
    parsed: ParsedPlaysoundCommand

    assert parsed.volume.value == 1

    assert str(parsed) == 'playsound test:sound @s 0 0 0 1'


def test_playsound_pitch():
    parsed = playsound.parse('playsound test:sound @s 0 0 0 1 1')
    parsed: ParsedPlaysoundCommand

    assert parsed.pitch.value == 1

    assert str(parsed) == 'playsound test:sound @s 0 0 0 1 1'


def test_playsound_min_volume():
    parsed = playsound.parse('playsound test:sound @s 0 0 0 1 1 0.1')
    parsed: ParsedPlaysoundCommand

    assert parsed.minimum_volume.value == 0.1

    assert str(parsed) == 'playsound test:sound @s 0 0 0 1 1 0.1'
