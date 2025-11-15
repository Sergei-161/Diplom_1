from unittest.mock import Mock
from praktikum.praktikum import Burger
import pytest


class TestBurger:

    def test_set_buns(self):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = 'black bun'
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient(self):
        burger = Burger()

        mock_ingredient = Mock()
        mock_ingredient.get_name.return_value = 'hot sauce'
        mock_ingredient.get_price.return_value = 100
        mock_ingredient.get_type.return_value = 'SAUCE'

        burger.add_ingredient(mock_ingredient)

        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient
        assert burger.ingredients[0].get_name() == 'hot sauce'
        assert burger.ingredients[0].get_price() == 100

    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()

        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.remove_ingredient(0)

        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient2

    def test_move_ingredient(self):
        burger = Burger()
        mock_ingredient1 = Mock()
        mock_ingredient2 = Mock()
        mock_ingredient3 = Mock()

        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)

        burger.move_ingredient(2, 0)

        assert burger.ingredients[0] == mock_ingredient3
        assert burger.ingredients[1] == mock_ingredient1
        assert burger.ingredients[2] == mock_ingredient2

    def test_get_receipt(self):
        burger = Burger()

        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100

        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = "SAUCE"
        mock_ingredient.get_name.return_value = "hot sauce"
        mock_ingredient.get_price.return_value = 50

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()

        expected_receipt = "\n".join([
            "(==== black bun ====)",
            "= sauce hot sauce =",
            "(==== black bun ====)",
            "",
            "Price: 250"
        ])

        assert receipt == expected_receipt

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_total", [
        (100, [], 200),  # Только булочки
        (100, [50], 250),  # +1 ингредиент
        (100, [50, 50], 300),  # +2 одинаковых ингредиента
        (200, [100], 500),  # Булочка + 1 ингредиент
        (50, [10, 20, 30], 160),  # Булочка + 3 ингредиента
    ])
    def test_get_price_with_different_combinations(self, bun_price, ingredient_prices, expected_total):
        burger = Burger()

        # mock булочки
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        # mock ингредиентов
        for price in ingredient_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)

        assert burger.get_price() == expected_total