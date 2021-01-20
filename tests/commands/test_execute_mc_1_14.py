
from mcfunction.versions.mc_1_14.execute import (
    execute, ParsedExecuteCommand, ParsedExecuteCondition
)
from mcfunction.nodes import EntityNode, PositionNode, RotationNode


class TestConditions:
    def test_align(self):
        condition, = execute.parse('execute align xyz run help').conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'align'
        assert condition.axes.value == 'xyz'

        assert str(condition) == 'align xyz'

    def test_anchored(self):
        condition, = execute.parse('execute anchored eyes run help').conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'anchored'
        assert condition.anchor.value == 'eyes'

        assert str(condition) == 'anchored eyes'

    def test_as(self):
        condition, = execute.parse('execute as @e run help').conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'as'
        assert isinstance(condition.target, EntityNode)

        assert str(condition) == 'as @e'

    def test_at(self):
        condition, = execute.parse('execute at @s run help').conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'at'
        assert isinstance(condition.target, EntityNode)

        assert str(condition) == 'at @s'

    def test_facing(self):
        condition, = execute.parse('execute facing 0 0 0 run help').conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'facing'
        assert isinstance(condition.position, PositionNode)

        assert str(condition) == 'facing 0 0 0'

    def test_facing_entity(self):
        condition, = execute.parse(
            'execute facing entity @s eyes run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'facing'
        assert condition.is_entity.value == 'entity'
        assert isinstance(condition.target, EntityNode)
        assert condition.anchor.value == 'eyes'

        assert str(condition) == 'facing entity @s eyes'

    def test_in(self):
        condition, = execute.parse(
            'execute in test:the_test run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'in'
        assert condition.dimension.namespace == 'test'
        assert condition.dimension.name == 'the_test'

        assert str(condition) == 'in test:the_test'

    def test_positioned(self):
        condition, = execute.parse(
            'execute positioned 0 0 0 run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'positioned'
        assert isinstance(condition.position, PositionNode)

        assert str(condition) == 'positioned 0 0 0'

    def test_positioned_as(self):
        condition, = execute.parse(
            'execute positioned as @e run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'positioned'
        assert condition.is_entity.value == 'as'
        assert isinstance(condition.target, EntityNode)

        assert str(condition) == 'positioned as @e'

    def test_rotated(self):
        condition, = execute.parse(
            'execute rotated 0 0 run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'rotated'
        assert isinstance(condition.rotation, RotationNode)

        assert str(condition) == 'rotated 0 0'

    def test_rotated_as(self):
        condition, = execute.parse(
            'execute rotated as @e run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'rotated'
        assert condition.is_entity.value == 'as'
        assert isinstance(condition.target, EntityNode)

        assert str(condition) == 'rotated as @e'

    def test_store_block(self):
        condition, = execute.parse(
            'execute store success block 0 0 0 a.b.c byte 1 run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'store'
        assert condition.condition.value == 'success'
        assert condition.mode.value == 'block'
        assert isinstance(condition.destination, PositionNode)
        assert condition.path.value == 'a.b.c'
        assert condition.type.value == 'byte'
        assert condition.scale.value == 1

        assert str(condition) == 'store success block 0 0 0 a.b.c byte 1'

    def test_store_bossbar(self):
        condition, = execute.parse(
            'execute store success bossbar test:bossbar value run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.mode.value == 'bossbar'
        assert condition.destination.namespace == 'test'
        assert condition.destination.name == 'bossbar'
        assert condition.path.value == 'value'

        assert str(condition) == 'store success bossbar test:bossbar value'

    def test_store_entity(self):
        condition, = execute.parse(
            'execute store success entity @e a.b.c byte 1 run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.mode.value == 'entity'
        assert isinstance(condition.destination, EntityNode)

        assert str(condition) == 'store success entity @e a.b.c byte 1'

    def test_store_score(self):
        condition, = execute.parse(
            'execute store success score @s testobjective run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.mode.value == 'score'
        assert isinstance(condition.target, EntityNode)
        assert condition.target_objective.value == 'testobjective'

        assert str(condition) == 'store success score @s testobjective'

    def test_if_block(self):
        condition, = execute.parse(
            'execute if block 0 0 0 test:block run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.action.value == 'if'
        assert condition.condition.value == 'block'
        assert isinstance(condition.position, PositionNode)
        assert condition.block.namespace == 'test'
        assert condition.block.name == 'block'

        assert str(condition) == 'if block 0 0 0 test:block'

    def test_if_blocks(self):
        condition, = execute.parse(
            'execute if blocks 0 0 0 1 1 1 2 2 2 all run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.condition.value == 'blocks'
        assert isinstance(condition.start, PositionNode)
        assert isinstance(condition.end, PositionNode)
        assert isinstance(condition.destination, PositionNode)
        assert condition.mode.value == 'all'

        assert str(condition) == 'if blocks 0 0 0 1 1 1 2 2 2 all'

    def test_if_data(self):
        condition, = execute.parse(
            'execute if data block 0 0 0 a.b.c run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.condition.value == 'data'
        assert condition.source_type.value == 'block'
        assert isinstance(condition.source, PositionNode)
        assert condition.path.value == 'a.b.c'

        assert str(condition) == 'if data block 0 0 0 a.b.c'

    def test_if_entity(self):
        condition, = execute.parse('execute if entity @e run help').conditions
        condition: ParsedExecuteCondition

        assert condition.condition.value == 'entity'
        assert isinstance(condition.target, EntityNode)

        assert str(condition) == 'if entity @e'

    def test_if_score(self):
        condition, = execute.parse(
            'execute if score @s testobjective1 = @s testobjective2 run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.condition.value == 'score'
        assert isinstance(condition.target, EntityNode)
        assert condition.target_objective.value == 'testobjective1'
        assert condition.comparison.value == '='
        assert isinstance(condition.source, EntityNode)
        assert condition.source_objective.value == 'testobjective2'

        assert str(condition) == 'if score @s testobjective1 = ' \
                                 '@s testobjective2'

    def test_if_score_matches(self):
        condition, = execute.parse(
            'execute if score @s testobjective matches 69..1337 run help'
        ).conditions
        condition: ParsedExecuteCondition

        assert condition.comparison.value == 'matches'
        assert condition.range.value == '69..1337'

        assert str(condition) == 'if score @s testobjective matches 69..1337'


def test_execute():
    parsed = execute.parse('execute run help')
    parsed: ParsedExecuteCommand

    assert not parsed.conditions
    assert parsed.run.command == 'help'

    assert str(parsed) == 'execute run help'


def test_execute_condition():
    parsed = execute.parse('execute as @e run help')
    parsed: ParsedExecuteCommand

    assert len(parsed.conditions) == 1
    assert parsed.run.command == 'help'

    assert str(parsed) == 'execute as @e run help'
