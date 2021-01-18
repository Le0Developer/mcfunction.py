
from mcfunction.commands.whitelist import whitelist, ParsedWhitelistCommand
from mcfunction.nodes import EntityNode


def test_whitelist_add():
    parsed = whitelist.parse('whitelist add @s')
    parsed: ParsedWhitelistCommand

    assert parsed.action.value == 'add'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'whitelist add @s'


def test_whitelist_list():
    parsed = whitelist.parse('whitelist list')
    parsed: ParsedWhitelistCommand

    assert parsed.action.value == 'list'

    assert str(parsed) == 'whitelist list'
