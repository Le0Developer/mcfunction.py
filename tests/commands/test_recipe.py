
from mcfunction.versions.mc_1_12.recipe import recipe, ParsedRecipeCommand
from mcfunction.nodes import EntityNode


def test_recipe():
    parsed = recipe.parse('recipe give @s test:recipe')
    parsed: ParsedRecipeCommand

    assert parsed.action.value == 'give'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.recipe.namespace == 'test'
    assert parsed.recipe.name == 'recipe'

    assert str(parsed) == 'recipe give @s test:recipe'


def test_recipe_everything():
    parsed = recipe.parse('recipe take @s *')
    parsed: ParsedRecipeCommand

    assert parsed.action.value == 'take'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.recipe.value == '*'

    assert str(parsed) == 'recipe take @s *'
