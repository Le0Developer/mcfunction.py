
from mcfunction.versions.mc_1_8.achievement import (
    achievement, ParsedAchievementCommand
)
from mcfunction.nodes import EntityNode


def test_achievement():
    parsed = achievement.parse('achievement give test:achievement')
    parsed: ParsedAchievementCommand

    assert parsed.action.value == 'give'
    assert parsed.achievement.namespace == 'test'
    assert parsed.achievement.name == 'achievement'

    assert str(parsed) == 'achievement give test:achievement'


def test_achievement_star_target():
    parsed = achievement.parse('achievement take * @p')
    parsed: ParsedAchievementCommand

    assert parsed.action.value == 'take'
    assert parsed.achievement.value == '*'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'achievement take * @p'
