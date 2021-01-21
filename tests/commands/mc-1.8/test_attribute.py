
from mcfunction.versions.mc_1_16.attribute import (
    attribute, ParsedAttributeCommand
)
from mcfunction.nodes import EntityNode


def test_attribute_get():
    parsed = attribute.parse('attribute @s test:attribute get')
    parsed: ParsedAttributeCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.attribute.namespace == 'test'
    assert parsed.attribute.name == 'attribute'
    assert parsed.action.value == 'get'

    assert str(parsed) == 'attribute @s test:attribute get'


def test_attribute_get_scale():
    parsed = attribute.parse('attribute @s test:attribute get 1337')
    parsed: ParsedAttributeCommand

    assert parsed.scale.value == 1337

    assert str(parsed) == 'attribute @s test:attribute get 1337'


def test_attribute_base_get():
    parsed = attribute.parse('attribute @s test:attribute base get')
    parsed: ParsedAttributeCommand

    assert parsed.action.value == 'base'
    assert parsed.base_action.value == 'get'
    assert parsed.scale is None

    assert str(parsed) == 'attribute @s test:attribute base get'


def test_attribute_base_get_scale():
    parsed = attribute.parse('attribute @s test:attribute base get 1337')
    parsed: ParsedAttributeCommand

    assert parsed.scale.value == 1337

    assert str(parsed) == 'attribute @s test:attribute base get 1337'


def test_attribute_base_set():
    parsed = attribute.parse('attribute @s test:attribute base set 1337')
    parsed: ParsedAttributeCommand

    assert parsed.action.value == 'base'
    assert parsed.base_action.value == 'set'
    assert parsed.value.value == 1337.0

    assert str(parsed) == 'attribute @s test:attribute base set 1337'


def test_attribute_modifier_add():
    parsed = attribute.parse('attribute @s test:attribute modifier add '
                             '1-2-3-4-5 name 1337 multiply')
    parsed: ParsedAttributeCommand

    assert parsed.action.value == 'modifier'
    assert parsed.modifier_action.value == 'add'
    assert parsed.uuid.value == '1-2-3-4-5'
    assert parsed.name.value == 'name'
    assert parsed.value.value == 1337.0
    assert parsed.modifier_action2.value == 'multiply'

    assert str(parsed) == 'attribute @s test:attribute modifier add ' \
                          '1-2-3-4-5 name 1337 multiply'


def test_attribute_modifier_remove():
    parsed = attribute.parse('attribute @s test:attribute modifier remove '
                             '1-2-3-4-5')
    parsed: ParsedAttributeCommand

    assert parsed.action.value == 'modifier'
    assert parsed.modifier_action.value == 'remove'
    assert parsed.uuid.value == '1-2-3-4-5'

    assert str(parsed) == 'attribute @s test:attribute modifier remove ' \
                          '1-2-3-4-5'


def test_attribute_modifier_get():
    parsed = attribute.parse('attribute @s test:attribute modifier get '
                             '1-2-3-4-5')
    parsed: ParsedAttributeCommand

    assert parsed.action.value == 'modifier'
    assert parsed.modifier_action.value == 'get'
    assert parsed.uuid.value == '1-2-3-4-5'

    assert str(parsed) == 'attribute @s test:attribute modifier get ' \
                          '1-2-3-4-5'


def test_attribute_modifier_get_scale():
    parsed = attribute.parse('attribute @s test:attribute modifier get '
                             '1-2-3-4-5 1337')
    parsed: ParsedAttributeCommand

    assert parsed.scale.value == 1337

    assert str(parsed) == 'attribute @s test:attribute modifier get ' \
                          '1-2-3-4-5 1337'
