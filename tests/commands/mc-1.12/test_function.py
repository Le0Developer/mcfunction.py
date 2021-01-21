
from mcfunction.versions.mc_1_12.function import (
    function, ParsedFunctionCommand
)
from mcfunction.nodes import EntityNode


def test_function():
    parsed = function.parse('function test:function')
    parsed: ParsedFunctionCommand

    assert parsed.name.namespace == 'test'
    assert parsed.name.name == 'function'

    assert str(parsed) == 'function test:function'


def test_function_if():
    parsed = function.parse('function test:function if @s')
    parsed: ParsedFunctionCommand

    assert parsed.name.namespace == 'test'
    assert parsed.name.name == 'function'
    assert parsed.condition.value == 'if'
    assert isinstance(parsed.selector, EntityNode)

    assert str(parsed) == 'function test:function if @s'
