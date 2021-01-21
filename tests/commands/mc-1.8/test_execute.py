
from mcfunction.versions.mc_1_8.execute import execute, ParsedExecuteCommand
from mcfunction.nodes import EntityNode, PositionNode


def test_execute():
    parsed = execute.parse('execute @p ~ ~ ~ help')
    parsed: ParsedExecuteCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.position, PositionNode)
    assert parsed.run.command == 'help'

    assert str(parsed) == 'execute @p ~ ~ ~ help'


def test_execute_detect():
    parsed = execute.parse('execute @p ~ ~ ~ detect ~ ~ ~ minecraft:air 0 '
                           'help')
    parsed: ParsedExecuteCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.position, PositionNode)
    assert parsed.detect.value == 'detect'
    assert isinstance(parsed.detect_position, PositionNode)
    assert parsed.block.namespace == 'minecraft'
    assert parsed.block.name == 'air'
    assert parsed.data.value == 0
    assert parsed.run.command == 'help'

    assert str(parsed) == 'execute @p ~ ~ ~ detect ~ ~ ~ minecraft:air 0 help'
