
from mcfunction.versions.mc_1_8.trigger import trigger, ParsedTriggerCommand


def test_trigger():
    parsed = trigger.parse('trigger testobjective')
    parsed: ParsedTriggerCommand

    assert parsed.objective.value == 'testobjective'

    assert str(parsed) == 'trigger testobjective'


def test_trigger_add():
    parsed = trigger.parse('trigger testobjective add 69')
    parsed: ParsedTriggerCommand

    assert parsed.objective.value == 'testobjective'
    assert parsed.action.value == 'add'
    assert parsed.value.value == 69

    assert str(parsed) == 'trigger testobjective add 69'
