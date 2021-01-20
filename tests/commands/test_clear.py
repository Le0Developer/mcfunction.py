
from mcfunction.versions.mc_1_8.clear import clear, ParsedClearCommand
from mcfunction.nodes import EntityNode


def test_clear():
    parsed = clear.parse('clear')
    parsed: ParsedClearCommand

    assert parsed.target is None

    assert str(parsed) == 'clear'


def test_clear_entity():
    parsed = clear.parse('clear @e')
    parsed: ParsedClearCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'clear @e'


def test_clear_item():
    parsed = clear.parse('clear @e test:item')
    parsed: ParsedClearCommand

    assert parsed.item.namespace == 'test'
    assert parsed.item.name == 'item'

    assert str(parsed) == 'clear @e test:item'


def test_clear_count():
    parsed = clear.parse('clear @e test:item 69')
    parsed: ParsedClearCommand

    assert parsed.count.value == 69

    assert str(parsed) == 'clear @e test:item 69'
