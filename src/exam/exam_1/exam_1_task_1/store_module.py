from typing import List, Optional


class Product:
    def __init__(self, name: str, price: float, rating: float, quantity: int) -> None:
        self.name = name
        self.price = price
        self.rating = rating
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}(price:{self.price})"

    def __repr__(self) -> str:
        return f"{self.name}(price:{self.price},rating:{self.rating},quantity:{self.quantity})"

    def decrease_quantity(self, number: int = 1) -> None:
        if number < 0:
            raise ValueError(f"Can not decrease on negative value")
        if self.quantity >= number:
            self.quantity -= number

        else:
            raise ValueError(f"Not enough product: {self.name}")


class Cart:
    def __init__(self) -> None:
        self.cart: List[Product] = list()

    def __str__(self) -> str:
        return ", ".join(str(product) for product in self.cart)

    def get_total_cost(self) -> float:
        cost = 0.0
        for product in self.cart:
            cost += product.price
        return cost

    def add_product(self, product: Product) -> None:
        self.cart.append(product)

    def remove_product(self, product: Product) -> None:
        if not product in self.cart:
            raise ValueError(f"There are no {product.name} in the cart")
        self.cart.remove(product)

    def clear(self) -> None:
        self.cart = []


class Store:
    def __init__(self, products: Optional[List[Product]] = None):
        self.carts: dict[str, Cart] = {}
        self.products: List[Product] = products if products is not None else []

    def get_most_expensive(self) -> Product:
        if len(self.products) == 0:
            raise ValueError("No products in Store")
        most_expensive_product = None
        for product in self.products:
            if product.quantity > 0 and most_expensive_product is None:
                most_expensive_product = product
            if (
                most_expensive_product is not None
                and product.price > most_expensive_product.price
                and product.quantity > 0
            ):
                most_expensive_product = product
        if most_expensive_product is None:
            raise ValueError("No products in Store")
        return most_expensive_product

    def get_cheapest(self) -> Product:
        if len(self.products) == 0:
            raise ValueError("No products in Store")
        cheapest_product = None
        for product in self.products:
            if product.quantity > 0 and cheapest_product is None:
                cheapest_product = product
            if cheapest_product is not None and product.price < cheapest_product.price and product.quantity > 0:
                cheapest_product = product
        if cheapest_product is None:
            raise ValueError("No products in Store")
        return cheapest_product

    def get_highest_rating(self) -> Product:
        if len(self.products) == 0:
            raise ValueError("No products in Store")
        highest_rating_product = None
        for product in self.products:
            if product.quantity > 0 and highest_rating_product is None:
                highest_rating_product = product
            if (
                highest_rating_product is not None
                and product.rating > highest_rating_product.rating
                and product.quantity > 0
            ):
                highest_rating_product = product
        if highest_rating_product is None:
            raise ValueError("No products in Store")

        return highest_rating_product

    def get_lowest_rating(self) -> Product:
        if len(self.products) == 0:
            raise ValueError("No products in Store")
        lowest_rating_product = None
        for product in self.products:
            if product.quantity > 0 and lowest_rating_product is None:
                lowest_rating_product = product
            if (
                lowest_rating_product is not None
                and product.rating < lowest_rating_product.rating
                and product.quantity > 0
            ):
                lowest_rating_product = product
        if lowest_rating_product is None:
            raise ValueError("No products in Store")

        return lowest_rating_product

    def create_cart(self, name: str) -> None:
        if name in self.carts:
            raise ValueError(f"It is not possible to create 2 carts with the same name ({name})")
        else:
            self.carts[name] = Cart()

    def buy_product(self, cart_name: str, product: Product, quantity: int) -> None:
        if cart_name not in self.carts:
            raise ValueError(f"There is no cart with a name {cart_name}")
        product.decrease_quantity(quantity)
        for _ in range(quantity):
            self.carts[cart_name].add_product(product)

    def remove_product(self, cart_name: str, product: Product, quantity: int) -> None:
        if cart_name not in self.carts:
            raise ValueError(f"There is no cart with a name {cart_name}")
        if self.carts[cart_name].cart.count(product) >= quantity:
            for _ in range(quantity):
                self.carts[cart_name].remove_product(product)
        else:
            raise ValueError(f"There are no {quantity} of {product.name} in the basket")

    def buy_cart(self, cart_name: str) -> None:
        if cart_name not in self.carts:
            raise ValueError(f"There is no cart with a name {cart_name}")
        self.carts[cart_name].clear()

    def view_cart(self, cart_name: str) -> None:
        if cart_name not in self.carts:
            raise ValueError(f"There is no cart with a name {cart_name}")
        print(self.carts[cart_name])

    def __str__(self) -> str:
        products_str = ",".join(product.__repr__() for product in self.products)
        return f"Products: {products_str}"
