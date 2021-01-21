
from mcfunction.versions.mc_1_8.blockdata import (
    blockdata, ParsedBlockdataCommand
)
from mcfunction.nodes import PositionNode


def test_blockdata():
    parsed = blockdata.parse('blockdata 0 0 0 {test:successful}')
    parsed: ParsedBlockdataCommand

    assert isinstance(parsed.position, PositionNode)
    assert parsed.data.value == '{test:successful}'

    assert str(parsed) == 'blockdata 0 0 0 {test:successful}'
