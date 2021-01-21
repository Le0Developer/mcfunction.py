
from mcfunction.versions.mc_1_16.setworldspawn import (
    setworldspawn, ParsedSetworldspawnCommand
)
from mcfunction.nodes import PositionNode, RotationNode


def test_setworldspawn():
    parsed = setworldspawn.parse('setworldspawn')
    parsed: ParsedSetworldspawnCommand

    assert str(parsed) == 'setworldspawn'


def test_setworldspawn_position():
    parsed = setworldspawn.parse('setworldspawn 0 0 0')
    parsed: ParsedSetworldspawnCommand

    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'setworldspawn 0 0 0'


def test_setworldspawn_angle():
    parsed = setworldspawn.parse('setworldspawn 0 0 0 1 1')
    parsed: ParsedSetworldspawnCommand

    assert isinstance(parsed.position, PositionNode)
    assert isinstance(parsed.angle, RotationNode)

    assert str(parsed) == 'setworldspawn 0 0 0 1 1'
