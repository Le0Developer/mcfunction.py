
from mcfunction.versions.mc_1_8.experience import (
    experience, ParsedExperienceCommand
)
from mcfunction.nodes import EntityNode


def test_experience():
    parsed = experience.parse('experience 69')
    parsed: ParsedExperienceCommand

    assert parsed.amount.value == 69
    assert parsed.target is None

    assert str(parsed) == 'experience 69'


def test_experience_target():
    parsed = experience.parse('experience 69 @p')
    parsed: ParsedExperienceCommand

    assert parsed.amount.value == 69
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'experience 69 @p'


def test_experience_levels():
    parsed = experience.parse('experience 69L')
    parsed: ParsedExperienceCommand

    assert parsed.amount.value == '69L'
    assert parsed.target is None

    assert str(parsed) == 'experience 69L'


def test_experience_target_levels():
    parsed = experience.parse('experience 69L @p')
    parsed: ParsedExperienceCommand

    assert parsed.amount.value == '69L'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'experience 69L @p'

