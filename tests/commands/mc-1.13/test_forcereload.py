
from mcfunction.versions.mc_1_13.forcereload import (
    forcereload, ParsedForcereloadCommand
)
from mcfunction.nodes import Position2dNode


def test_forcereload_add():
    parsed = forcereload.parse('forcereload add 0 0')
    parsed: ParsedForcereloadCommand

    assert parsed.action.value == 'add'
    assert isinstance(parsed.start, Position2dNode)
    assert parsed.end is None

    assert str(parsed) == 'forcereload add 0 0'


def test_forcereload_add_to():
    parsed = forcereload.parse('forcereload add 0 0 16 16')
    parsed: ParsedForcereloadCommand

    assert isinstance(parsed.start, Position2dNode)
    assert isinstance(parsed.end, Position2dNode)

    assert str(parsed) == 'forcereload add 0 0 16 16'


def test_forcereload_remove_all():
    parsed = forcereload.parse('forcereload remove all')
    parsed: ParsedForcereloadCommand

    assert parsed.action.value == 'remove'
    assert parsed.start.value == 'all'

    assert str(parsed) == 'forcereload remove all'


def test_forcereload_query():
    parsed = forcereload.parse('forcereload query')
    parsed: ParsedForcereloadCommand

    assert parsed.action.value == 'query'

    assert str(parsed) == 'forcereload query'


def test_forcereload_query_pos():
    parsed = forcereload.parse('forcereload query 0 0')
    parsed: ParsedForcereloadCommand

    assert parsed.action.value == 'query'
    assert isinstance(parsed.start, Position2dNode)

    assert str(parsed) == 'forcereload query 0 0'
