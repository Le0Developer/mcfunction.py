
from mcfunction.commands.give import give, ParsedGiveCommand
from mcfunction.nodes import EntityNode


def test_give():
    parsed = give.parse('give @s test:item')
    parsed: ParsedGiveCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.item.namespace == 'test'
    assert parsed.item.name == 'item'

    assert str(parsed) == 'give @s test:item'


def test_give_64():
    parsed = give.parse('give @s test:item 64')
    parsed: ParsedGiveCommand

    assert parsed.count.value == 64

    assert str(parsed) == 'give @s test:item 64'
