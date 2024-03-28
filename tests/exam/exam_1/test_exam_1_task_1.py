import pytest

from src.exam.exam_1.exam_1_task_1.store_module import *


class TestProduct:
    @pytest.mark.parametrize("quantity,decreasing_quantity,expected", [(5, 2, 3), (10, 3, 7), (20, 20, 0)])
    def test_decrease_quantity(self, quantity, decreasing_quantity, expected):
        product = Product("name", 1, 1, quantity)
        product.decrease_quantity(decreasing_quantity)
        assert product.quantity == expected

    @pytest.mark.parametrize("quantity,decreasing_quantity", [(5, -5), (10, 123), (20, 22)])
    def test_decrease_quantity_exception(self, quantity, decreasing_quantity):
        product = Product("name", 1, 1, quantity)
        with pytest.raises(ValueError):
            product.decrease_quantity(decreasing_quantity)


class TestCart:
    @pytest.mark.parametrize("prices,expected", [((1, 2, 3), 6), ((10, 3), 13), ((20, 20), 40)])
    def test_get_total_cost(self, prices, expected):
        cart = Cart()
        for price in prices:
            cart.add_product(Product("", price, 1, 1))
        assert cart.get_total_cost() == expected

    @pytest.mark.parametrize("name,price,rating,quantity", [("q", 1, 2, 3), ("asd", 4, 2, 1)])
    def test_add_product(self, name, price, rating, quantity):
        cart = Cart()
        product = Product(name, price, rating, quantity)
        cart.add_product(product)
        assert product in cart.cart

    @pytest.mark.parametrize("name,price,rating,quantity", [("q", 1, 2, 3), ("asd", 4, 2, 1)])
    def test_remove_product(self, name, price, rating, quantity):
        cart = Cart()
        product = Product(name, price, rating, quantity)
        cart.add_product(product)
        assert product in cart.cart
        cart.remove_product(product)
        assert product not in cart.cart

    @pytest.mark.parametrize("name,price,rating,quantity", [("q", 1, 2, 3), ("asd", 4, 2, 1)])
    def test_clear(self, name, price, rating, quantity):
        cart = Cart()
        product = Product(name, price, rating, quantity)
        cart.add_product(product)
        assert product in cart.cart
        cart.clear()
        assert cart.cart == []


class TestStore:
    def create_store(self, product_parameters):
        items = []
        for i in product_parameters:
            name, price, rating, quantity = i
            product = Product(name, price, rating, quantity)
            items.append(product)
        store = Store(items)
        return store

    def test_create_cart(self):
        store = Store()
        store.create_cart("asd")
        assert store.carts

    @pytest.mark.parametrize(
        "products,expected", [((("q", 1, 2, 3), ("asd", 4, 2, 1)), 4), ((("q", 1, 2, 3), ("asd", 4, 2, 0)), 1)]
    )
    def test_get_most_expensive(self, products, expected):
        store = self.create_store(products)

        assert store.get_most_expensive().price == expected

    @pytest.mark.parametrize(
        "products,expected", [((("q", 1, 2, 3), ("asd", 4, 2, 1)), 1), ((("q", 1, 2, 0), ("asd", 4, 2, 1)), 4)]
    )
    def test_get_cheapest(self, products, expected):
        store = self.create_store(products)
        assert store.get_cheapest().price == expected

    @pytest.mark.parametrize(
        "products,expected", [((("q", 1, 100, 3), ("asd", 4, 2, 1)), 100), ((("q", 1, 100, 0), ("asd", 4, 2, 1)), 2)]
    )
    def test_get_highest_rating(self, products, expected):
        store = self.create_store(products)

        assert store.get_highest_rating().rating == expected

    @pytest.mark.parametrize(
        "products,expected", [((("q", 1, 100, 3), ("asd", 4, 2, 1)), 2), ((("q", 1, 100, 3), ("asd", 4, 2, 0)), 100)]
    )
    def test_get_lowest_rating(self, products, expected):
        store = self.create_store(products)

        assert store.get_lowest_rating().rating == expected

    @pytest.mark.parametrize("products", [(("q", 1, 100, 3), ("asd", 4, 2, 1)), (("q", 1, 100, 3), ("asd", 4, 2, 0))])
    def test_buy_product(self, products):
        store = self.create_store(products)
        product = store.products[0]
        store.create_cart("test")
        store.buy_product("test", product, product.quantity)
        assert product in store.carts["test"].cart

    @pytest.mark.parametrize("products", [(("q", 1, 100, 3), ("asd", 4, 2, 1)), (("q", 1, 100, 3), ("asd", 4, 2, 0))])
    def test_remove_product(self, products):
        store = self.create_store(products)
        product = store.products[0]
        store.create_cart("test")
        quantity = product.quantity
        store.buy_product("test", product, quantity)
        assert product in store.carts["test"].cart
        store.remove_product("test", product, quantity)
        assert product not in store.carts["test"].cart

    @pytest.mark.parametrize("products", [(("q", 1, 100, 3), ("asd", 4, 2, 1)), (("q", 1, 100, 3), ("asd", 4, 2, 0))])
    def test_buy_cart(self, products):
        store = self.create_store(products)
        product = store.products[0]
        store.create_cart("test")
        quantity = product.quantity
        store.buy_product("test", product, quantity)
        store.buy_cart("test")
        assert len(store.carts["test"].cart) == 0

    def test_get_most_expensive_exception(self):
        store = Store()
        with pytest.raises(ValueError):
            store.get_most_expensive()

    def test_get_cheapest_exception(self):
        store = Store()
        with pytest.raises(ValueError):
            store.get_cheapest()

    def test_get_highest_rating_exception(self):
        store = Store()
        with pytest.raises(ValueError):
            store.get_highest_rating()

    def test_get_lowest_rating_exception(self):
        store = Store()
        with pytest.raises(ValueError):
            store.get_lowest_rating()
