
from mcfunction.commands.enchant import enchant, ParsedEnchantCommand
from mcfunction.nodes import EntityNode


def test_enchant():
    parsed = enchant.parse('enchant @s test:enchantment')
    parsed: ParsedEnchantCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.enchantment.namespace == 'test'
    assert parsed.enchantment.name == 'enchantment'

    assert str(parsed) == 'enchant @s test:enchantment'


def test_enchant_level():
    parsed = enchant.parse('enchant @s test:enchantment 69')
    parsed: ParsedEnchantCommand

    assert parsed.level.value == 69

    assert str(parsed) == 'enchant @s test:enchantment 69'
