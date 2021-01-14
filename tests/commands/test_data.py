
from mcast.commands.data import data, ParsedDataCommand
from mcast.nodes import EntityNode, PositionNode


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


def test_data_get_storage():
    parsed = data.parse('data get storage test:storage')
    parsed: ParsedDataCommand

    assert parsed.target_type.value == 'storage'
    assert parsed.target.namespace == 'test'
    assert parsed.target.name == 'storage'

    assert str(parsed) == 'data get storage test:storage'


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


def test_data_modify_append_from():
    parsed = data.parse('data modify block 0 0 0 a.b.c append '
                        'from block 0 0 0')
    parsed: ParsedDataCommand

    assert parsed.action.value == 'modify'
    assert parsed.target_type.value == 'block'
    assert parsed.path.value == 'a.b.c'
    assert parsed.modification.value == 'append'
    assert parsed.modification_source.value == 'from'
    assert parsed.source_type.value == 'block'

    assert str(parsed) == 'data modify block 0 0 0 a.b.c append ' \
                          'from block 0 0 0'


def test_data_modify_append_from_path():
    parsed = data.parse('data modify block 0 0 0 a.b.c append '
                        'from block 0 0 0 d.e.f')
    parsed: ParsedDataCommand

    assert parsed.source_path.value == 'd.e.f'

    assert str(parsed) == 'data modify block 0 0 0 a.b.c append ' \
                          'from block 0 0 0 d.e.f'


def test_data_modify_append_value():
    parsed = data.parse('data modify block 0 0 0 a.b.c append value 1337')
    parsed: ParsedDataCommand

    assert parsed.modification_source.value == 'value'
    assert parsed.source_path.value == 1337

    assert str(parsed) == 'data modify block 0 0 0 a.b.c append value 1337'


def test_data_modify_insert():
    parsed = data.parse('data modify block 0 0 0 a.b.c insert 0 value 1337')
    parsed: ParsedDataCommand

    assert parsed.modification.value == 'insert'
    assert parsed.index.value == 0
    assert parsed.modification_source.value == 'value'
    assert parsed.source_path.value == 1337

    assert str(parsed) == 'data modify block 0 0 0 a.b.c insert 0 value 1337'


def test_data_remove():
    parsed = data.parse('data remove block 0 0 0 a.b.c')
    parsed: ParsedDataCommand

    assert parsed.action.value == 'remove'
    assert parsed.target_type.value == 'block'

    assert str(parsed) == 'data remove block 0 0 0 a.b.c'
