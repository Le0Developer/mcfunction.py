
from mcfunction.commands.replaceitem import (
    replaceitem, ParsedReplaceitemCommand
)
from mcfunction.nodes import EntityNode, PositionNode


def test_replaceitem_block():
    parsed = replaceitem.parse('replaceitem block 0 0 0 '
                               'hotbar.slot_number.0 test:item')
    parsed: ParsedReplaceitemCommand

    assert parsed.action.value == 'block'
    assert isinstance(parsed.position, PositionNode)
    assert parsed.slot.value == 'hotbar.slot_number.0'
    assert parsed.item.namespace == 'test'
    assert parsed.item.name == 'item'

    assert str(parsed) == 'replaceitem block 0 0 0 hotbar.slot_number.0 ' \
                          'test:item'


def test_replaceitem_block_count():
    parsed = replaceitem.parse('replaceitem block 0 0 0 '
                               'hotbar.slot_number.0 test:item 64')
    parsed: ParsedReplaceitemCommand

    assert parsed.count.value == 64

    assert str(parsed) == 'replaceitem block 0 0 0 hotbar.slot_number.0 ' \
                          'test:item 64'


def test_replaceitem_entity():
    parsed = replaceitem.parse('replaceitem entity @s hotbar.slot_number.0 '
                               'test:item')
    parsed: ParsedReplaceitemCommand

    assert parsed.action.value == 'entity'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.slot.value == 'hotbar.slot_number.0'
    assert parsed.item.namespace == 'test'
    assert parsed.item.name == 'item'

    assert str(parsed) == 'replaceitem entity @s hotbar.slot_number.0 ' \
                          'test:item'


def test_replaceitem_entity_count():
    parsed = replaceitem.parse('replaceitem entity @s hotbar.slot_number.0 '
                               'test:item 64')
    parsed: ParsedReplaceitemCommand

    assert parsed.count.value == 64

    assert str(parsed) == 'replaceitem entity @s hotbar.slot_number.0 ' \
                          'test:item 64'
