
from mcfunction.versions.mc_1_8.setworldspawn import (
    setworldspawn, ParsedSetworldspawnCommand
)
from mcfunction.nodes import PositionNode


def test_setworldspawn():
    parsed = setworldspawn.parse('setworldspawn')
    parsed: ParsedSetworldspawnCommand

    assert str(parsed) == 'setworldspawn'


def test_setworldspawn_position():
    parsed = setworldspawn.parse('setworldspawn 0 0 0')
    parsed: ParsedSetworldspawnCommand

    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'setworldspawn 0 0 0'
