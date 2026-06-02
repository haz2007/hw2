import pytest # type: ignore
from reps import Ingredient, Recipe, ShoppingList, DietaryRecipe
#для Ingredient
def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"
def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"
def test_ingredient_eq_same():
    a = Ingredient("Мука", 100, "г")
    b = Ingredient("Мука", 200, "г")
    assert a == b
def test_ingredient_eq_different_name():
    a = Ingredient("Мука", 100, "г")
    b = Ingredient("Сахар", 100, "г")
    assert a != b
def test_ingredient_eq_different_unit():
    a = Ingredient("Мука", 100, "г")
    b = Ingredient("Мука", 100, "кг")
    assert a != b
def test_ingredient_invalid_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -1, "г")

#для Recipe
def test_recipe_creation():
    r = Recipe("Пицца")
    assert r.title == "Пицца"
    assert r.ingredients == []
def test_recipe_add_ingredient():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    assert len(r) == 1
def test_recipe_add_ingredient_duplicate():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 300, "г"))
    r.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(r) == 1
    assert r.ingredients[0].quantity == 500.0
def test_recipe_scale():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled = r.scale(2)
    assert r.ingredients[0].quantity == 500.0
    assert scaled.ingredients[0].quantity == 1000.0
    assert scaled is not r
def test_recipe_scale_invalid():
    r = Recipe("Пицца")
    with pytest.raises(ValueError):
        r.scale(-1)
def test_recipe_len():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    r.add_ingredient(Ingredient("Соль", 10, "г"))
    assert len(r) == 2

#для ShoppingList
def test_shopping_add_recipe():
    sl = ShoppingList()
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    sl.add_recipe(r, 2)
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].quantity == 1000.0
def test_shopping_add_recipe_invalid_portions():
    sl = ShoppingList()
    r = Recipe("Пицца")
    with pytest.raises(ValueError):
        sl.add_recipe(r, 0)
def test_shopping_remove_recipe():
    sl = ShoppingList()
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    sl.add_recipe(r, 1)
    sl.remove_recipe("Пицца")
    assert sl.get_list() == []
def test_shopping_remove_nonexistent():
    sl = ShoppingList()
    sl.remove_recipe("Несуществующий")
def test_shopping_get_list_sums():
    sl = ShoppingList()
    r1 = Recipe("Пицца")
    r1.add_ingredient(Ingredient("Мука", 300, "г"))
    r2 = Recipe("Хлеб")
    r2.add_ingredient(Ingredient("Мука", 200, "г"))
    sl.add_recipe(r1, 1)
    sl.add_recipe(r2, 1)
    result = sl.get_list()
    assert result[0].name == "Мука"
    assert result[0].quantity == 500.0
def test_shopping_get_list_sorted():
    sl = ShoppingList()
    r = Recipe("Блюдо")
    r.add_ingredient(Ingredient("Яйца", 3, "шт"))
    r.add_ingredient(Ingredient("Мука", 200, "г"))
    sl.add_recipe(r, 1)
    result = sl.get_list()
    assert result[0].name == "Мука"
    assert result[1].name == "Яйца"
def test_shopping_add_two_lists():
    sl1 = ShoppingList()
    r1 = Recipe("Пицца")
    r1.add_ingredient(Ingredient("Мука", 500, "г"))
    sl1.add_recipe(r1, 1)
    sl2 = ShoppingList()
    r2 = Recipe("Хлеб")
    r2.add_ingredient(Ingredient("Соль", 5, "г"))
    sl2.add_recipe(r2, 1)
    sl3 = sl1 + sl2
    result = sl3.get_list()
    assert len(result) == 2
    assert len(sl1.get_list()) == 1
    assert len(sl2.get_list()) == 1

#для DietaryRecipe
def test_dietary_recipe_creation():
    r = DietaryRecipe("Пицца Маргарита", "веган")
    assert r.title == "Пицца Маргарита"
    assert r.diet_type == "веган"
    assert r.ingredients == []
def test_dietary_recipe_str():
    r = DietaryRecipe("Пицца Маргарита", "веган")
    assert str(r).startswith("[веган]")
def test_dietary_recipe_scale_returns_dietary():
    r = DietaryRecipe("Пицца", "кето")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled = r.scale(2)
    assert isinstance(scaled, DietaryRecipe)
def test_dietary_recipe_scale_keeps_diet_type():
    r = DietaryRecipe("Пицца", "кето")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled = r.scale(2)
    assert scaled.diet_type == "кето"
def test_dietary_recipe_scale_multiplies():
    r = DietaryRecipe("Пицца", "веган")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    scaled = r.scale(3)
    assert scaled.ingredients[0].quantity == 1500.0
def test_dietary_recipe_does_not_change_original():
    r = DietaryRecipe("Пицца", "веган")
    r.add_ingredient(Ingredient("Мука", 500, "г"))
    r.scale(2)
    assert r.ingredients[0].quantity == 500.0