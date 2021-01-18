
from mcfunction.commands.datapack import datapack, ParsedDatapackCommand


def test_datapack_enable():
    parsed = datapack.parse('datapack enable test')
    parsed: ParsedDatapackCommand

    assert parsed.action.value == 'enable'
    assert parsed.name.value == 'test'

    assert str(parsed) == 'datapack enable test'


def test_datapack_enable_first():
    parsed = datapack.parse('datapack enable test first')
    parsed: ParsedDatapackCommand

    assert parsed.action.value == 'enable'
    assert parsed.mode.value == 'first'

    assert str(parsed) == 'datapack enable test first'


def test_datapack_enable_before():
    parsed = datapack.parse('datapack enable test before vanilla')
    parsed: ParsedDatapackCommand

    assert parsed.existing.value == 'vanilla'

    assert str(parsed) == 'datapack enable test before vanilla'


def test_datapack_disable():
    parsed = datapack.parse('datapack disable test')
    parsed: ParsedDatapackCommand

    assert parsed.action.value == 'disable'
    assert parsed.name.value == 'test'

    assert str(parsed) == 'datapack disable test'


def test_datapack_list():
    parsed = datapack.parse('datapack list')
    parsed: ParsedDatapackCommand

    assert parsed.action.value == 'list'

    assert str(parsed) == 'datapack list'


def test_datapack_list_available():
    parsed = datapack.parse('datapack list available')
    parsed: ParsedDatapackCommand

    assert parsed.action.value == 'list'
    assert parsed.mode.value == 'available'

    assert str(parsed) == 'datapack list available'
