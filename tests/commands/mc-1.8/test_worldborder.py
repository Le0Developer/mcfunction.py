
from mcfunction.versions.mc_1_8.worldborder import (
    worldborder, ParsedWordborderCommand
)
from mcfunction.nodes import Position2dNode


def test_worldborder_add():
    parsed = worldborder.parse('worldborder add 69')
    parsed: ParsedWordborderCommand

    assert parsed.action.value == 'add'
    assert parsed.distance.value == 69

    assert str(parsed) == 'worldborder add 69'


def test_worldborder_add_time():
    parsed = worldborder.parse('worldborder add 69 1337')
    parsed: ParsedWordborderCommand

    assert parsed.time.value == 1337

    assert str(parsed) == 'worldborder add 69 1337'


def test_worldborder_center():
    parsed = worldborder.parse('worldborder center 0 0')
    parsed: ParsedWordborderCommand

    assert parsed.action.value == 'center'
    assert isinstance(parsed.center, Position2dNode)

    assert str(parsed) == 'worldborder center 0 0'


def test_worldborder_damage_amount():
    parsed = worldborder.parse('worldborder damage amount 42')
    parsed: ParsedWordborderCommand

    assert parsed.action.value == 'damage'
    assert parsed.name.value == 'amount'
    assert parsed.value.value == 42

    assert str(parsed) == 'worldborder damage amount 42'


def test_worldborder_damage_buffer():
    parsed = worldborder.parse('worldborder damage buffer 69')
    parsed: ParsedWordborderCommand

    assert parsed.name.value == 'buffer'
    assert parsed.value.value == 69

    assert str(parsed) == 'worldborder damage buffer 69'


def test_worldborder_get():
    parsed = worldborder.parse('worldborder get')
    parsed: ParsedWordborderCommand

    assert parsed.action.value == 'get'

    assert str(parsed) == 'worldborder get'
