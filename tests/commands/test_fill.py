
from mcfunction.commands.fill import fill, ParsedFillCommand
from mcfunction.nodes import PositionNode


def test_fill():
    parsed = fill.parse('fill 0 0 0 1 1 1 test:block')
    parsed: ParsedFillCommand

    assert isinstance(parsed.start, PositionNode)
    assert isinstance(parsed.end, PositionNode)
    assert parsed.block.namespace == 'test'
    assert parsed.block.name == 'block'

    assert str(parsed) == 'fill 0 0 0 1 1 1 test:block'


def test_fill_replace():
    parsed = fill.parse('fill 0 0 0 1 1 1 test:block replace')
    parsed: ParsedFillCommand

    assert parsed.action.value == 'replace'
    assert parsed.filter is None

    assert str(parsed) == 'fill 0 0 0 1 1 1 test:block replace'


def test_fill_replace_filter():
    parsed = fill.parse('fill 0 0 0 1 1 1 test:block replace test:other_block')
    parsed: ParsedFillCommand

    assert parsed.action.value == 'replace'
    assert parsed.filter.namespace == 'test'
    assert parsed.filter.name == 'other_block'

    assert str(parsed) == 'fill 0 0 0 1 1 1 test:block ' \
                          'replace test:other_block'
