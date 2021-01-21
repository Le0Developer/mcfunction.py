
from mcfunction.versions.mc_1_8.entitydata import (
    entitydata, ParsedEntitydataCommand
)
from mcfunction.nodes import EntityNode


def test_entitydata():
    parsed = entitydata.parse('entitydata @p {test:successful}')
    parsed: ParsedEntitydataCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.data.value == '{test:successful}'

    assert str(parsed) == 'entitydata @p {test:successful}'
