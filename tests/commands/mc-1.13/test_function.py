
from mcfunction.versions.mc_1_13.function import (
    function, ParsedFunctionCommand
)


def test_function():
    parsed = function.parse('function test:function')
    parsed: ParsedFunctionCommand

    assert parsed.name.namespace == 'test'
    assert parsed.name.name == 'function'

    assert str(parsed) == 'function test:function'
