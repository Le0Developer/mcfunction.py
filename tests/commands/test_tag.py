
from mcast.commands.tag import tag, ParsedTagCommand
from mcast.nodes import EntityNode


def test_tag_add():
    parsed = tag.parse('tag @s add testtag')
    parsed: ParsedTagCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'add'
    assert parsed.name.value == 'testtag'

    assert str(parsed) == 'tag @s add testtag'


def test_tag_list():
    parsed = tag.parse('tag @s list')
    parsed: ParsedTagCommand

    assert parsed.action.value == 'list'

    assert str(parsed) == 'tag @s list'
