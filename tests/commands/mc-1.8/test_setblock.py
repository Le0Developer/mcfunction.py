
from mcfunction.versions.mc_1_8.setblock import setblock, ParsedSetblockCommand
from mcfunction.nodes import PositionNode


def test_setblock():
    parsed = setblock.parse('setblock 0 0 0 test:block')
    parsed: ParsedSetblockCommand

    assert isinstance(parsed.position, PositionNode)
    assert parsed.block.namespace == 'test'
    assert parsed.block.name == 'block'

    assert str(parsed) == 'setblock 0 0 0 test:block'


def test_setblock_action():
    parsed = setblock.parse('setblock 0 0 0 test:block destroy')
    parsed: ParsedSetblockCommand

    assert parsed.action.value == 'destroy'

    assert str(parsed) == 'setblock 0 0 0 test:block destroy'
