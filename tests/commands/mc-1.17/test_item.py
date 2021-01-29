
from mcfunction.versions.mc_1_17.item import item, ParsedItemCommand
from mcfunction.nodes import PositionNode


def test_item_copy():
    parsed = item.parse('item block 0 0 0 slot copy block 1 1 1 slot')
    parsed: ParsedItemCommand

    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.slot.value == 'slot'
    assert parsed.action.value == 'copy'
    assert parsed.source_type.value == 'block'
    assert isinstance(parsed.source, PositionNode)
    assert parsed.source_slot.value == 'slot'

    assert str(parsed) == 'item block 0 0 0 slot copy block 1 1 1 slot'


def test_item_copy_modifier():
    parsed = item.parse('item block 0 0 0 slot copy block 1 1 1 slot modifier')
    parsed: ParsedItemCommand

    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.slot.value == 'slot'
    assert parsed.action.value == 'copy'
    assert parsed.source_type.value == 'block'
    assert isinstance(parsed.source, PositionNode)
    assert parsed.source_slot.value == 'slot'
    assert parsed.modifier.value == 'modifier'

    assert str(parsed) == 'item block 0 0 0 slot copy block 1 1 1 slot ' \
                          'modifier'


def test_item_modify():
    parsed = item.parse('item block 0 0 0 slot modify modifier')
    parsed: ParsedItemCommand

    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.slot.value == 'slot'
    assert parsed.action.value == 'modify'
    assert parsed.modifier.value == 'modifier'

    assert str(parsed) == 'item block 0 0 0 slot modify modifier'


def test_item_replace():
    parsed = item.parse('item block 0 0 0 slot replace test:item')
    parsed: ParsedItemCommand

    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.slot.value == 'slot'
    assert parsed.action.value == 'replace'
    assert parsed.item.namespace == 'test'
    assert parsed.item.name == 'item'

    assert str(parsed) == 'item block 0 0 0 slot replace test:item'


def test_item_replace_count():
    parsed = item.parse('item block 0 0 0 slot replace test:item 42')
    parsed: ParsedItemCommand

    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.slot.value == 'slot'
    assert parsed.action.value == 'replace'
    assert parsed.item.namespace == 'test'
    assert parsed.item.name == 'item'
    assert parsed.count.value == 42

    assert str(parsed) == 'item block 0 0 0 slot replace test:item 42'
