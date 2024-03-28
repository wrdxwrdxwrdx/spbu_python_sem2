from store_module import *


def main() -> None:
    bread = Product("Bread", 100, 4.5, 100)
    water = Product("Water", 40.99, 3.2, 25)
    cheese = Product("Cheese", 173.2, 4.3, 5)

    store = Store([bread, water, cheese])
    print(store)
    print()
    print(f"most_expensive: {store.get_most_expensive()}")
    print(f"cheapest: {store.get_cheapest()}")
    print(f"highest_rating: {store.get_highest_rating().__repr__()}")
    print(f"lowest_rating: {store.get_lowest_rating().__repr__()}")
    store.create_cart("for work")
    store.create_cart("for home")

    store.buy_product("for work", bread, 100)
    store.buy_product("for work", water, 3)
    print()
    store.view_cart("for work")
    print(water in store.carts["for work"].cart)
    store.buy_cart("for work")
    print()

    print(store)

    store.buy_product("for home", bread, 1)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
