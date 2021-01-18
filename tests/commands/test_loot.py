
from mcfunction.commands.loot import loot, ParsedLootCommand
from mcfunction.nodes import EntityNode, PositionNode


def test_loot_spawn():
    parsed = loot.parse('loot spawn 0 0 0 kill @e')
    parsed: ParsedLootCommand

    assert parsed.target_type.value == 'spawn'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.source_type.value == 'kill'
    assert isinstance(parsed.source, EntityNode)

    assert str(parsed) == 'loot spawn 0 0 0 kill @e'


def test_loot_replace():
    parsed = loot.parse('loot replace entity @s hotbar.slot_number.0 9 '
                        'kill @e')
    parsed: ParsedLootCommand

    assert parsed.target_type.value == 'replace'
    assert parsed.target_type2.value == 'entity'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.slot.value == 'hotbar.slot_number.0'
    assert parsed.count.value == 9

    assert str(parsed) == 'loot replace entity @s hotbar.slot_number.0 9 ' \
                          'kill @e'


def test_loot_fish():
    parsed = loot.parse('loot spawn 0 0 0 fish test:loot_table 0 0 0')
    parsed: ParsedLootCommand

    assert parsed.source_type.value == 'fish'
    assert parsed.source.namespace == 'test'
    assert parsed.source.name == 'loot_table'
    assert isinstance(parsed.source_position, PositionNode)

    assert str(parsed) == 'loot spawn 0 0 0 fish test:loot_table 0 0 0'


def test_loot_fish_tool():
    parsed = loot.parse('loot spawn 0 0 0 fish test:loot_table 0 0 0 mainhand')
    parsed: ParsedLootCommand

    assert parsed.source_tool.value == 'mainhand'

    assert str(parsed) == 'loot spawn 0 0 0 fish test:loot_table 0 0 0 ' \
                          'mainhand'


def test_loot_mine():
    parsed = loot.parse('loot spawn 0 0 0 mine 0 0 0 mainhand')
    parsed: ParsedLootCommand

    assert parsed.source_tool.value == 'mainhand'

    assert str(parsed) == 'loot spawn 0 0 0 mine 0 0 0 mainhand'
