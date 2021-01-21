
from mcfunction.versions.mc_1_13.data import data, ParsedDataCommand
from mcfunction.nodes import EntityNode, PositionNode


def test_data_get_block():
    parsed = data.parse('data get block 0 0 0 a.b.c')
    parsed: ParsedDataCommand

    assert parsed.action.value == 'get'
    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.path.value == 'a.b.c'

    assert str(parsed) == 'data get block 0 0 0 a.b.c'


def test_data_get_entity():
    parsed = data.parse('data get entity @e')
    parsed: ParsedDataCommand

    assert parsed.target_type.value == 'entity'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'data get entity @e'


def test_data_get_scale():
    parsed = data.parse('data get block 0 0 0 a.b.c 1337')
    parsed: ParsedDataCommand

    assert parsed.scale.value == 1337

    assert str(parsed) == 'data get block 0 0 0 a.b.c 1337'


def test_data_merge():
    parsed = data.parse('data merge block 0 0 0 {Test:1b}')
    parsed: ParsedDataCommand

    assert parsed.action.value == 'merge'
    assert parsed.nbt.value == '{Test:1b}'

    assert str(parsed) == 'data merge block 0 0 0 {Test:1b}'


def test_data_remove():
    parsed = data.parse('data remove block 0 0 0 a.b.c')
    parsed: ParsedDataCommand

    assert parsed.action.value == 'remove'
    assert parsed.target_type.value == 'block'

    assert str(parsed) == 'data remove block 0 0 0 a.b.c'
