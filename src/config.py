from pathlib import Path

# 1. Находим корень проекта
# __file__ — это путь к ТЕКУЩЕМУ файлу (src/config.py)
# .resolve() — делает путь абсолютным
# .parent — поднимается на папку выше (в src)
# .parent.parent — поднимается еще на уровень выше (в корень Project1)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Динамические пути к директориям
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"

# 3. Пути к конкретным файлам
RAW_DATASET_PATH = RAW_DATA_DIR / "housing.csv"

# 4. Настройки и гиперпараметры для ML
RANDOM_STATE = 42  # Фиксируем генератор случайных чисел для воспроизводимости
TEST_SIZE = 0.2    # 20% данных уходит на тест, 80% на обучение

# from typing import List, Optional, Dict
# students = [
#     {"name": "Анна", "age": 20, "grades": [5, 4, 5]},  # Dict[str, any]
#     {"name": "Борис", "age": 21, "grades": [3, 4, 3]}, # Dict[str, any]
# ]
# def find_student(students: List[Dict[str, any]], name: str) -> Optional[Dict]:
#     for student in students:
#         if student["name"] == name:
#             return student
#     return None
# print(find_student(students, "Анна"))
# # students: List[Dict[str, any]]
# # "Анна": str

# from typing import List, Dict, Optional, Union
#
# # 1. Создай переменную numbers — список целых чисел
# # 2. Создай переменную names — список строк
# # 3. Создай переменную ages — словарь {str: int}
# # 4. Создай переменную maybe_age — Optional[int] = None
# # 5. Создай переменную value — Union[int, str] = "текст"
#
# # Твой код:
# numbers: int = [1, 2, 3]
# names: List[str] = ["Анна", "Борис"]
# ages: Dict[str, any] = {"Анна": 20, "Борис": 25}
# maybe_age: Optional[int] = None
# value: Union[int | str] = "текст"
#
# from typing import List, Dict, Optional
#
# # Создай функцию find_product:
# # Принимает:
# #   - products: список словарей с товарами
# #   - product_name: строку
# # Возвращает:
# #   - словарь товара, если найден
# #   - None, если не найден
#
# def find_product(products: List[Dict[str, any]], product_name: str) -> Optional[Dict]:
#     for product in products:
#         if product['name'] == product_name:
#             return product
#     return None
#     pass  # твой код
#
# # Тесты:
# products = [
#     {"name": "ноутбук", "price": 50000},
#     {"name": "мышка", "price": 2000},
# ]
#
# result = find_product(products, "ноутбук")
# print(result)  # {'name': 'ноутбук', 'price': 50000}
#
# result = find_product(products, "стол")
# print(result)  # None
#
# from typing import Union
#
# # Создай функцию parse_value:
# # Принимает Union[int, str]
# # Если int — возвращает квадрат числа
# # Если str — возвращает строку в верхнем регистре
#
# def parse_value(value: Union[int, str]) -> Union[int, str]:
#     if type(value) == int: return value ** 2
#     else: return value.upper()
#     pass  # твой код
#
# # Тесты:
# print(parse_value(5))       # 25
# print(parse_value("hello")) # HELLO
from typing import List, Dict, Optional, Union

def get_expensive_products(products: List[Dict[str, int]], min_price = int) -> Optional[Dict]:
    return [product for product in products if product['price'] > min_price]

products = [
    {"name": "ноутбук", "price": 50000},
    {"name": "мышка", "price": 2000},
    {"name": "клавиатура", "price": 3000},
    {"name": "монитор", "price": 25000},
    {"name": "наушники", "price": 5000},
]

min_price = 10000
# Ожидаемый результат: товары дороже 10000
# [{'name': 'ноутбук', 'price': 50000}, {'name': 'монитор', 'price': 25000}]
print(get_expensive_products(products, min_price))

# 2. Создай функцию calculate_stats:
#    Принимает список чисел
#    Возвращает Dict[str, float] с ключами "avg", "max", "min"
def calculate_stats(numbers: Dict[int]):
    avge = sum(numbers) / len(numbers)
    maxs = max(numbers)
    mins = min(numbers)
    return {'avg': avge, 'max': maxs, 'min': mins}
numbers = [5, 12, 8, 3, 15, 7, 10, 2]
# Ожидаемый результат:
# {"avg": 7.75, "max": 15, "min": 2}

# 3. Создай функцию safe_divide:
#    Принимает два числа
#    Возвращает результат деления или None, если деление на ноль
#    Тип возврата: Optional[float]
def safe_divide(a = int, b = int)->Optional[float]:
    if a != 0 and b != 0:
        return a / b
    else:
        return None
a = 10
b = 2
# Ожидаемый результат: 5.0
a = 10
b = 0
# Ожидаемый результат: None
print(safe_divide(a, b))