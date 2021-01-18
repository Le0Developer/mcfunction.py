
from mcfunction.commands.locatebiome import locatebiome, ParsedLocatebiomeCommand


def test_locatebiome():
    parsed = locatebiome.parse('locatebiome test:biome')
    parsed: ParsedLocatebiomeCommand

    assert parsed.biome.namespace == 'test'
    assert parsed.biome.name == 'biome'

    assert str(parsed) == 'locatebiome test:biome'


def test_locatebiome_id():
    parsed = locatebiome.parse('locatebiome 69')
    parsed: ParsedLocatebiomeCommand

    assert parsed.biome.value == 69

    assert str(parsed) == 'locatebiome 69'
