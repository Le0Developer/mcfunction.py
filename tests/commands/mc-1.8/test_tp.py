
from mcfunction.versions.mc_1_8.tp import tp, ParsedTpCommand
from mcfunction.nodes import EntityNode, PositionNode, RotationNode


def test_tp_entity():
    parsed = tp.parse('tp @r')
    parsed: ParsedTpCommand

    assert isinstance(parsed.destination, EntityNode)

    assert str(parsed) == 'tp @r'


def test_tp_position():
    parsed = tp.parse('tp 0 0 0')
    parsed: ParsedTpCommand

    assert isinstance(parsed.destination, PositionNode)

    assert str(parsed) == 'tp 0 0 0'


def test_tp_position_rotation():
    parsed = tp.parse('tp 0 0 0 1 1')
    parsed: ParsedTpCommand

    assert isinstance(parsed.destination, PositionNode)
    assert isinstance(parsed.rotation, RotationNode)

    assert str(parsed) == 'tp 0 0 0 1 1'


def test_tp_target_entity():
    parsed = tp.parse('tp @p @r')
    parsed: ParsedTpCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, EntityNode)

    assert str(parsed) == 'tp @p @r'


def test_tp_target_position():
    parsed = tp.parse('tp @p 0 0 0')
    parsed: ParsedTpCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, PositionNode)

    assert str(parsed) == 'tp @p 0 0 0'


def test_tp_target_rotation():
    parsed = tp.parse('tp @p 0 0 0 1 1')
    parsed: ParsedTpCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.destination, PositionNode)
    assert isinstance(parsed.rotation, RotationNode)

    assert str(parsed) == 'tp @p 0 0 0 1 1'
