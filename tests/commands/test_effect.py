
from mcast.commands.effect import effect, ParsedEffectCommand
from mcast.nodes import EntityNode


def test_effect_clear():
    parsed = effect.parse('effect clear')
    parsed: ParsedEffectCommand

    assert parsed.action.value == 'clear'

    assert str(parsed) == 'effect clear'


def test_effect_clear_targets():
    parsed = effect.parse('effect clear @e')
    parsed: ParsedEffectCommand

    assert parsed.action.value == 'clear'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'effect clear @e'


def test_effect_clear_effect():
    parsed = effect.parse('effect clear @e test:effect')
    parsed: ParsedEffectCommand

    assert parsed.action.value == 'clear'
    assert parsed.effect.namespace == 'test'
    assert parsed.effect.name == 'effect'

    assert str(parsed) == 'effect clear @e test:effect'


def test_give():
    parsed = effect.parse('effect give @s test:effect')
    parsed: ParsedEffectCommand

    assert parsed.action.value == 'give'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.effect.namespace == 'test'
    assert parsed.effect.name == 'effect'

    assert str(parsed) == 'effect give @s test:effect'


def test_give_duration():
    parsed = effect.parse('effect give @s test:effect 60')
    parsed: ParsedEffectCommand

    assert parsed.seconds.value == 60

    assert str(parsed) == 'effect give @s test:effect 60'


def test_give_amplfier():
    parsed = effect.parse('effect give @s test:effect 60 2')
    parsed: ParsedEffectCommand

    assert parsed.seconds.value == 60
    assert parsed.amplifier.value == 2

    assert str(parsed) == 'effect give @s test:effect 60 2'


def test_give_particles():
    parsed = effect.parse('effect give @s test:effect 60 2 true')
    parsed: ParsedEffectCommand

    assert parsed.seconds.value == 60
    assert parsed.amplifier.value == 2
    assert parsed.hide_particles.value

    assert str(parsed) == 'effect give @s test:effect 60 2 true'
