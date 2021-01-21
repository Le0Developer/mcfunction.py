
from mcfunction.versions.mc_1_8.stats import stats, ParsedStatsCommand
from mcfunction.nodes import EntityNode, PositionNode


def test_stats_block_clear():
    parsed = stats.parse('stats block 0 0 0 clear AffectedBlocks')
    parsed: ParsedStatsCommand

    assert parsed.target_type.value == 'block'
    assert isinstance(parsed.target, PositionNode)
    assert parsed.mode.value == 'clear'
    assert parsed.stat.value == 'AffectedBlocks'

    assert str(parsed) == 'stats block 0 0 0 clear AffectedBlocks'


def test_stats_entity_set():
    parsed = stats.parse('stats entity @a set AffectedEntities count '
                         'testobjective')
    parsed: ParsedStatsCommand

    assert parsed.target_type.value == 'entity'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.mode.value == 'set'
    assert parsed.stat.value == 'AffectedEntities'
    assert isinstance(parsed.selector, EntityNode)
    assert parsed.objective.value == 'testobjective'

    assert str(parsed) == 'stats entity @a set AffectedEntities count ' \
                          'testobjective'
