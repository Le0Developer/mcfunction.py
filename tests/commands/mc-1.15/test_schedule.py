
from mcfunction.versions.mc_1_15.schedule import (
    schedule, ParsedScheduleCommand
)


def test_schedule_function():
    parsed = schedule.parse('schedule function test:function 69t')
    parsed: ParsedScheduleCommand

    assert parsed.action.value == 'function'
    assert parsed.name.namespace == 'test'
    assert parsed.name.name == 'function'
    assert parsed.time.value == '69t'

    assert str(parsed) == 'schedule function test:function 69t'


def test_schedule_function_append():
    parsed = schedule.parse('schedule function test:function 69t append')
    parsed: ParsedScheduleCommand

    assert parsed.mode.value == 'append'

    assert str(parsed) == 'schedule function test:function 69t append'


def test_schedule_clear():
    parsed = schedule.parse('schedule clear test:function')
    parsed: ParsedScheduleCommand

    assert parsed.action.value == 'clear'
    assert parsed.name.namespace == 'test'
    assert parsed.name.name == 'function'

    assert str(parsed) == 'schedule clear test:function'
