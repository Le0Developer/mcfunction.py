
from mcast.commands.experience import experience, ParsedExperienceCommand
from mcast.nodes import EntityNode


def test_experience_add():
    parsed = experience.parse('experience add @s 69')
    parsed: ParsedExperienceCommand

    assert parsed.action.value == 'add'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.amount.value == 69

    assert str(parsed) == 'experience add @s 69'


def test_experience_add_levels():
    parsed = experience.parse('experience add @s 69 levels')
    parsed: ParsedExperienceCommand

    assert parsed.unit.value == 'levels'

    assert str(parsed) == 'experience add @s 69 levels'


def test_experience_query():
    parsed = experience.parse('experience query @s levels')
    parsed: ParsedExperienceCommand

    assert parsed.action.value == 'query'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.unit.value == 'levels'

    assert str(parsed) == 'experience query @s levels'
