
from mcfunction.versions.mc_1_13.advancement import (
    advancement, ParsedAdvancementCommand
)
from mcfunction.nodes import EntityNode


def test_advancement_everything():
    parsed = advancement.parse('advancement grant @s everything')
    parsed: ParsedAdvancementCommand

    assert parsed.command == 'advancement'
    assert parsed.action.value == 'grant'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.mode.value == 'everything'

    assert str(parsed) == 'advancement grant @s everything'


def test_advancement_only():
    parsed = advancement.parse('advancement revoke @s only test:advancement')
    parsed: ParsedAdvancementCommand

    assert parsed.action.value == 'revoke'
    assert parsed.mode.value == 'only'
    assert parsed.advancement.namespace == 'test'
    assert parsed.advancement.name == 'advancement'

    assert str(parsed) == 'advancement revoke @s only test:advancement'


def test_advancement_only_criterion():
    parsed = advancement.parse('advancement revoke @s only test:advancement '
                               'criterion')
    parsed: ParsedAdvancementCommand

    assert parsed.criterion.value == 'criterion'

    assert str(parsed) == 'advancement revoke @s only test:advancement ' \
                          'criterion'


def test_advancement_from():
    parsed = advancement.parse('advancement grant @s from test:advancement')
    parsed: ParsedAdvancementCommand

    assert parsed.mode.value == 'from'

    assert str(parsed) == 'advancement grant @s from test:advancement'
