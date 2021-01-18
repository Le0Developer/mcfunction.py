
import types

import pytest

from mcfunction import nodes, util
from mcfunction.exceptions import ConstructionException, ParserException


class TestTokenize:
    def test_spaces(self):
        tokenized = tuple(util.tokenize('stay home; stay safe', ' '))
        assert tokenized == ('stay', 'home;', 'stay', 'safe')

    def test_parentheses(self):
        tokenized = tuple(util.tokenize('(stay home) (stay safe)', ' '))
        assert tokenized == ('(stay home)', '(stay safe)')

    def test_backslash(self):
        with pytest.raises(ParserException, match=r"unclosed '\)'"):
            tuple(util.tokenize('stay safe (:', ' '))

        tokenized = tuple(util.tokenize(r'stay safe \(:', ' '))
        assert tokenized == ('stay', 'safe', r'\(:')


def test_get():
    parts = iter(range(7))

    assert util.get(parts) == 0
    assert util.get(parts) == 1
    assert util.get(parts, 1) == [2]
    assert util.get(parts, 4) == [3, 4, 5, 6]


def test_ensure_nodes():
    object = types.SimpleNamespace(
        value_0=nodes.RawNode('value'),
        value_1=None
    )

    util.ensure_nodes(object, 'value_0')

    with pytest.raises(ConstructionException,
                       match='expected .* to be Node, not .*'):
        util.ensure_nodes(object, 'value_0', 'value_1')

    with pytest.raises(ConstructionException,
                       match='expected .* to be Node, not .*'):
        util.ensure_nodes(object, 'value_2')


def test_clean():
    assert util.clean('0.0') == '0'
    assert util.clean('0.1') == '0.1'
    assert util.clean('0.2000000') == '0.2'
