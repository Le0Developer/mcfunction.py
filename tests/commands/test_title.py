
from mcfunction.commands.title import title, ParsedTitleCommand
from mcfunction.nodes import EntityNode


def test_title_clear():
    parsed = title.parse('title @s clear')
    parsed: ParsedTitleCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'clear'

    assert str(parsed) == 'title @s clear'


def test_title_title():
    parsed = title.parse('title @s title {"text":"test successful"}')
    parsed: ParsedTitleCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'title'
    assert parsed.title.object['text'] == 'test successful'

    assert str(parsed) == 'title @s title {"text":"test successful"}'


def test_title_times():
    parsed = title.parse('title @s times 0 69 0')
    parsed: ParsedTitleCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'times'
    assert parsed.fadein.value == 0
    assert parsed.stay.value == 69
    assert parsed.fadeout.value == 0

    assert str(parsed) == 'title @s times 0 69 0'
