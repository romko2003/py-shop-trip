import json
import math
import os
import datetime  # Змінено: імпортуємо весь модуль datetime

from .shop import Shop
from .customer import Customer
from .car import Car
from typing import List, Dict, Any


# Допоміжна функція для розрахунку Евклідової відстані
def calculate_distance(loc1: List[float], loc2: List[float]) -> float:
    """Calculates the Euclidean distance between two 2D points."""
    return math.sqrt((loc2[0] - loc1[0]) ** 2 + (loc2[1] - loc1[1]) ** 2)


def shop_trip():
    # Отримуємо абсолютний шлях до директорії, де знаходиться поточний скрипт (main.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Будуємо повний шлях до config.json
    config_path = os.path.join(script_dir, "config.json")

    # Завантажуємо конфігурацію з config.json
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: config.json not found at {config_path}. Please ensure it's in the 'app' directory.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding config.json: {e}")
        return

    FUEL_PRICE = config.get("FUEL_PRICE", 0.0)
    customers_data = config.get("customers", [])
    shops_data = config.get("shops", [])

    # Створюємо об'єкти Shop на основі даних з конфігурації
    shops: List[Shop] = []
    for s_data in shops_data:
        shops.append(Shop(s_data['name'], s_data['location'], s_data['products']))

    # Створюємо об'єкти Customer на основі даних з конфігурації
    customers: List[Customer] = []
    for c_data in customers_data:
        customer_car = Car(c_data['car']['fuel_consumption'])
        customers.append(Customer(
            c_data['name'],
            c_data['product_cart'],
            c_data['location'],  # current_location
            c_data['money'],
            customer_car
        ))

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")

        cheapest_total_trip_cost = float('inf')
        best_shop_for_customer: Shop = None

        # Зберігаємо інформацію про вартість поїздок до всіх магазинів для подальшого виведення
        all_shop_trip_costs_for_printing: List[tuple[str, float]] = []

        for shop in shops:
            distance_to_shop = calculate_distance(customer.current_location, shop.location)

            # Розрахунок витрат на паливо для поїздки туди й назад
            fuel_liters_one_way = customer.car.calculate_fuel_liters_for_distance(distance_to_shop)
            fuel_cost_round_trip = (fuel_liters_one_way * 2) * FUEL_PRICE

            products_cost_at_shop = 0.0
            can_fulfill_cart = True

            # Розрахунок вартості товарів та перевірка, чи магазин може виконати все замовлення
            for product, quantity in customer.product_cart.items():
                if product not in shop.products:
                    can_fulfill_cart = False
                    break  # Магазин не може виконати це замовлення
                products_cost_at_shop += shop.products[product] * quantity

            # Загальна вартість поїздки до магазину (для друку)
            total_trip_cost_for_printing = fuel_cost_round_trip + products_cost_at_shop
            all_shop_trip_costs_for_printing.append((shop.name, total_trip_cost_for_printing))

            # Розглядаємо магазин для покупки, тільки якщо він може виконати замовлення
            # і у клієнта вистачає грошей
            if can_fulfill_cart and customer.money >= total_trip_cost_for_printing:
                if total_trip_cost_for_printing < cheapest_total_trip_cost:
                    cheapest_total_trip_cost = total_trip_cost_for_printing
                    best_shop_for_customer = shop

        # Виводимо вартість поїздок до всіх магазинів (як в прикладі)
        for shop_name, cost in all_shop_trip_costs_for_printing:
            print(f"{customer.name}'s trip to the {shop_name} costs {cost:.2f}")

        # Перевіряємо, чи був обраний магазин
        if best_shop_for_customer is None:
            print(f"{customer.name} doesn't have enough money to make a purchase in any shop")
            print()
            continue

        # Клієнт їде до обраного магазину
        print(f"{customer.name} rides to {best_shop_for_customer.name}")
        print()

        # Оновлюємо поточне місцезнаходження клієнта
        customer.current_location = best_shop_for_customer.location

        # Виводимо квитанцію про покупку
        # datetime.datetime.now() буде повертати змодельований час з тесту
        now_str = datetime.datetime.now().strftime(
            "%m/%d/%Y %H:%M:%S")  # Змінено: використовуємо datetime.datetime.now()
        print(f"Date: {now_str}")
        print(f"Thanks, {customer.name}, for your purchase!")
        print("You have bought:")

        receipt_products_total_cost = 0.0
        for product, quantity in customer.product_cart.items():
            price = best_shop_for_customer.products[product]
            cost_item = price * quantity
            receipt_products_total_cost += cost_item

            # Форматуємо вартість товару (ціле число, якщо немає дробової частини)
            formatted_item_cost = int(cost_item) if cost_item == int(cost_item) else cost_item
            print(f"{quantity} {product}s for {formatted_item_cost} dollars")

        # "Total cost" у квитанції стосується лише вартості товарів
        formatted_receipt_total = int(receipt_products_total_cost) if \
            receipt_products_total_cost == int(receipt_products_total_cost) else \
            receipt_products_total_cost
        print(f"Total cost is {formatted_receipt_total} dollars")
        print("See you again!")
        print()  # Новий рядок після квитанції

        # Клієнт повертається додому та підраховує залишок грошей
        print(f"{customer.name} rides home")

        # Розраховуємо повну суму, витрачену на поїздку (товари + паливо туди й назад)
        # Використовуємо initial_location для розрахунку відстані додому
        distance_for_fuel_deduction = calculate_distance(customer.initial_location, best_shop_for_customer.location)
        fuel_liters_deduction = customer.car.calculate_fuel_liters_for_distance(distance_for_fuel_deduction) * 2
        fuel_cost_deduction = fuel_liters_deduction * FUEL_PRICE

        total_money_spent_on_trip = receipt_products_total_cost + fuel_cost_deduction
        customer.money -= total_money_spent_on_trip

        # Виводимо залишок грошей, округлений до двох знаків після коми
        print(f"{customer.name} now has {customer.money:.2f} dollars")
        print()