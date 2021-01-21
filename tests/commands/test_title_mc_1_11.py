
from mcfunction.versions.mc_1_11.title import title, ParsedTitleCommand
from mcfunction.nodes import EntityNode


def test_title_clear():
    parsed = title.parse('title @s clear')
    parsed: ParsedTitleCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'clear'

    assert str(parsed) == 'title @s clear'


def test_title_title():
    parsed = title.parse('title @s actionbar {"text":"test successful"}')
    parsed: ParsedTitleCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'actionbar'
    assert parsed.title.object['text'] == 'test successful'

    assert str(parsed) == 'title @s actionbar {"text":"test successful"}'


def test_title_times():
    parsed = title.parse('title @s times 0 69 0')
    parsed: ParsedTitleCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.action.value == 'times'
    assert parsed.fadein.value == 0
    assert parsed.stay.value == 69
    assert parsed.fadeout.value == 0

    assert str(parsed) == 'title @s times 0 69 0'
