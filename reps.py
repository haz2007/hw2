class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []
    def add_ingredient(self, ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    @staticmethod
    def is_valid_ratio(ratio):
        try:
            return float(ratio) > 0
        except (TypeError, ValueError):
            return False
    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        new_ingredients = [
            Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            for ing in self.ingredients
        ]
        return Recipe(self.title, new_ingredients)
    def __len__(self):
        return len(self.ingredients)
    def __str__(self):
        lines = [f"Рецепт: {self.title}"] + [f"  - {ing}" for ing in self.ingredients]
        return "\n".join(lines)

class ShoppingList:
    def __init__(self):
        self._items = []
    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))
    def remove_recipe(self, title):
        self._items = [(ing, t) for ing, t in self._items if t != title]
    def get_list(self):
        totals = {}
        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            totals[key] = totals.get(key, 0) + ing.quantity
        result = [Ingredient(name, qty, unit) for (name, unit), qty in totals.items()]
        result.sort(key=lambda x: x.name)
        return result
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    def scale(self, ratio):
        scaled = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled.ingredients)
    def __str__(self):
        return f"[{self.diet_type}] " + super().__str__()