# from collections import namedtuple
#
# # Создай namedtuple "Point" с полями x и y
# # Создай две точки и сложи их координаты
#
# # from collections import namedtuple
# #
# # Point = namedtuple('Point', ['x', 'y'])
# #
# # x1 = input('Введите х первой кординаты: ')
# # y1 = input('Введите y первой кординаты: ')
# #
# # x2 = input('Введите х второй кординаты: ')
# # y2 = input('Введите y второй кординаты: ')
# #
# # p1 = Point(int(x1), int(y1))
# # p2 = Point(int(x2), int(y2))
# #
# # p3 = Point(p1.x + p2.x, p1.y + p2.y)
# # print(p3)
#
# # import time
# #
# # huge_list = list(range(10000000))
# # huge_set = set(range(10000000))
# #
# # # Поиск в конце списка (самый худший случай)
# # start = time.time()
# # print(9999999 in huge_list)  # True
# # print(f"Список: {time.time() - start:.4f} сек")
# #
# # start = time.time()
# # print(9999999 in huge_set)   # True
# # print(f"Множество: {time.time() - start:.4f} сек")
#
# # d = {frozenset({1, 2}): "это множество {1,2}"}
# # print(d[frozenset({1, 2})])  # "это множество {1,2}"
# #
# # # И положить в обычное множество:
# # s = {frozenset({1, 2}), frozenset({3, 4})}
# # print(s)
#
# # Даны данные
# # users_a = {"Анна", "Борис", "Вика", "Глеб"}
# # users_b = {"Вика", "Глеб", "Дима", "Елена"}
# # all_users = {"Анна", "Борис", "Вика", "Глеб", "Дима", "Елена", "Жанна"}
# # #1
# # print(users_a & users_b)
# # #2
# # print(users_a | users_b)
# # #3
# # print(users_a - users_b)
# # #4
# # print(users_a ^ users_b)
# # #5
# # #i dont know
# # #6
# # k = 0
# # ml = len(users_a)
# # for i in all_users:
# #     if i in users_a:
# #         k+=1
# # if k == ml:
# #     print("Все пользователи на месте")
# # #7, 8
# # d = {frozenset(users_a): "Name server"}
#
#
# # 1. Кто пользуется ОБОИМИ сервисами? (пересечение)
# # 2. Кто пользуется ХОТЯ БЫ одним? (объединение)
# # 3. Кто есть в A, но нет в B? (разность)
# # 4. Кто пользуется ТОЛЬКО одним сервисом? (симметрическая разность)
# # 5. Есть ли среди пользователей A — "Дима"? (проверка за O(1))
# # 6. Проверь, что все пользователи A есть в all_users (подмножество)
# # 7. Создай frozenset из users_a
# # 8. Создай словарь, где ключ — frozenset пользователей сервиса,
# #    а значение — название
# # сервиса
#
# # Данные о заказах
# # orders = [
# #     {"id": 1, "товар": "ноутбук", "цена": 50000},
# #     {"id": 2, "товар": "мышка", "цена": 2000},
# #     {"id": 3, "товар": "клавиатура", "цена": 3000},
# #     {"id": 4, "товар": "монитор", "цена": 25000},
# #     {"id": 5, "товар": "мышка", "цена": 1500},
# # ]
# #
# # #1
# # max_item = max(orders, key=lambda o: o["цена"])
# # print(max_item)
# # #2
# #
# # # 1. Найди заказ с максимальной ценой (через max с key)
# # # 2. Сгруппируй заказы по товару: {"ноутбук": [заказ1], "мышка": [заказ2, заказ5], ...}
# # #    Используй setdefault
# # # 3. То же самое через defaultdict(list)
# # # 4. Посчитай общую сумму всех заказов
# # # 5. Создай словарь {товар: общая_сумма} через defaultdict(float) или defaultdict(int)
#
# # # Данные о товарах
# # products = [
# #     {"название": "ноутбук", "категория": "электроника", "цена": 50000, "остаток": 5},
# #     {"название": "мышка", "категория": "электроника", "цена": 2000, "остаток": 0},
# #     {"название": "стол", "категория": "мебель", "цена": 15000, "остаток": 3},
# #     {"название": "стул", "категория": "мебель", "цена": 8000, "остаток": 10},
# #     {"название": "лампа", "категория": "свет", "цена": 3000, "остаток": 0},
# # ]
# #
# # #1
# # names = [name["название"] for name in products]
# # print(names)
# # #2
# # over_price = [(name["название"], price["цена"]) for name in products for price in products if price["цена"] >= 5000]
# # print(over_price)
# # #3
# # ost = [(name["название"], price["цена"], ostat["остаток"]) for name in products for price in products for ostat in products if ostat > 0]
# # print(ost)
# # #4
# #
# # # 1. Создай список названий ВСЕХ товаров (list comprehension)
# # # 2. Создай список товаров дороже 5000 (list comprehension с фильтром)
# # # 3. Создай список товаров с остатком > 0, в формате "Название: Цена₽"
# # # 4. Создай множество уникальных категорий (set comprehension)
# # # 5. Создай словарь {название: цена} для товаров дороже 3000
# # # 6. Создай список категорий, где есть товары с остатком 0 (сложное)
# # # 7*. Создай словарь {категория: [названия товаров]} через comprehension
#
# # 1. Напиши функцию calculate, которая принимает:
# #    - обязательный аргумент operation (строка)
# #    - *args (числа)
# #    - **kwargs (дополнительные настройки)
# #    Возвращает результат операции над числами
# #    operation может быть "sum", "multiply", "average"
# #    kwargs может содержать "round_to" — округление
# import math
# def calculate(operation, *args, **kwargs):
#     if operation == 'sum':
#         result = sum(args)
#     if operation == "multiply":
#         result = math.prod(args)
#     if operation == 'average':
#         result = sum(args) / len(args)
#     round_to = kwargs.get('round_to')
#     if round_to is not None:
#         result = round(result, round_to)
#     return result
#
# # Тесты:
# print(calculate("sum", 1, 2, 3))           # 6
# print(calculate("multiply", 2, 3, 4))      # 24
# print(calculate("average", 1, 2, 3))       # 2.0
# print(calculate("sum", 1.234, 2.345, round_to=1))  # 3.6
from html.parser import interesting_normal
from urllib.parse import uses_relative

# # Данные о животных
# animals = ["лев", "слон", "жираф", "пингвин"]
# weights = [190, 5000, 1200, 40]  # кг
# habitats = ["саванна", "саванна", "саванна", "антарктида"]
# diet = ["мясо", "растения", "растения", "рыба"]
#
# #1
# result = list(zip(animals, weights))
# print(result)
# #2
# d = dict(zip(animals, weights))
# print(d)
# #3
# for anim, wei in zip(animals, weights):
#     print(f'{anim}: {wei}')
# #4
# spis = list(zip(animals, weights, habitats))
# print(spis)
# #5
# maxd = list(zip(animals, weights))
# for m, x in maxd:
#     if x == max(weights):
#         print(f"{m}: {x}")
# #6
# sortd = list(zip(animals, weights))
# print(sorted(sortd, key=lambda o: -o[1]))
# #7
# for y, o, p, e in zip(animals, weights, habitats, diet):
#     print(f'Название животного: {y}, Вес: {o}, Зона обитания: {p}, Диета: {e}')
# # 1. Создай список кортежей (животное, вес) через zip
# # 2. Создай словарь {животное: вес}
# # 3. Создай список строк "животное: вес кг"
# # 4. Создай список кортежей (животное, вес, среда обитания)
# # 5. Найди животное с максимальным весом (через max с key по zip-парам)
# # 6. Отсортируй животных по весу (по убыванию)
# # 7*. Транспонируй данные: из списка строк в список столбцов

# employees = {
#     "Анна": {"должность": "разработчик", "зарплата": 150000, "отдел": "IT"},
#     "Борис": {"должность": "дизайнер", "зарплата": 120000, "отдел": "Дизайн"},
#     "Вика": {"должность": "аналитик", "зарплата": 130000, "отдел": "Аналитика"},
#     "Глеб": {"должность": "разработчик", "зарплата": 160000, "отдел": "IT"},
# }
#
# # 1. Имя: должность
# for name, data in employees.items():
#     print(f"{name}: {data['должность']}")
#
# # 2. Максимальная зарплата
# max_employee = max(employees.items(), key=lambda item: item[1]["зарплата"])
# print(f"Максимум: {max_employee[0]} — {max_employee[1]['зарплата']}₽")
#
# # 3. Средняя зарплата
# salaries = [data["зарплата"] for data in employees.values()]
# avg = sum(salaries) / len(salaries)
# print(f"Средняя: {avg:.0f}₽")
#
# # 4. Словарь {отдел: [имена]}
# departments = {}
# for name, data in employees.items():
#     dept = data["отдел"]
#     departments.setdefault(dept, []).append(name)
# print(departments)
#
# # 5. Сортировка по зарплате
# sorted_employees = sorted(employees.items(), key=lambda item: item[1]["зарплата"], reverse=True)
# for name, data in sorted_employees:
#     print(f"{name}: {data['зарплата']}₽")
#
# # 6. Только разработчики
# devs = [name for name, data in employees.items() if data["должность"] == "разработчик"]
# print(f"Разработчики: {devs}")

# students = {
#     "Анна": {"оценки": [5, 4, 5], "группа": "А"},
#     "Борис": {"оценки": [3, 4, 3], "группа": "Б"},
#     "Вика": {"оценки": [5, 5, 4], "группа": "А"},
# }
#
# # 1. Выведи средний балл каждого студента
# # (подсказка: sum(оценки) / len(оценки))
#
# for name, data in students.items():
#     grades = data["оценки"]  # список оценок
#     total = sum(grades)      # сумма всех оценок
#     count = len(grades)      # количество оценок
#     avg = total / count      # средний балл
#     print(f"{name}: средний балл {round(avg, 1),}")
#
# # 2. Найди студента с максимальным средним баллом
# # (подсказка: max с key, внутри key считаешь средний балл)
# d = []
# for name, data in students.items():
#     grades = data["оценки"]  # список оценок
#     total = sum(grades)      # сумма всех оценок
#     count = len(grades)      # количество оценок
#     avg = total / count      # средний балл
#     d.append([name, avg])
# #хз
# # 3. Сгруппируй студентов по группам
# # (подсказка: setdefault)

# d = []
# for x in open('/home/ansel/Project1/src/students.txt', 'r', encoding='utf-8'):
#     d.append(x.strip())
# with open("students.txt", "r", encoding="utf-8") as file:
#     content = file.read()
# lines = content.strip().split('\n')
# for line in lines:
#     parts = line.split(',')
#     name = parts[0]        # 'Анна'
#     age = int(parts[1])    # 20 (число)
#     grade = int(parts[2])  # 5 (число)
#     print(f"{name}: балл {grade}")
# dds = []
# ddx = []
# with open('students.txt', 'r', encoding='utf-8') as file:
#     next(file)
#     content = file.read()
# lines = content.strip().split('\n')
# for line in lines:
#     parts = line.split(',')
#     name = parts[0]
#     coll = int(parts[1])
#     price = int(parts[2])
#     v = coll * price
#     ddx.append(v)
#     print(f'Товар: {name}. Выручка: {v} руб.')
#     dds.append([name, coll, price, v])
# print(max(dds, key=lambda o: o[2]))
# print(f'Общая выручка: {sum(ddx)}')
# print(sorted(dds, key=lambda o: -o[3])[:3])

# with open('students.txt', 'r', encoding='utf-8') as file:
#     next(file)
#     content = file.read()
# dds = []
# len_zp = 0
# lines = content.strip().split('\n')
# for line in lines:
#     len_zp += 1
#     parts = line.split(',')
#     ids = int(parts[0])
#     name = parts[1]
#     otdel = parts[2]
#     zp = int(parts[3])
#     age = int(parts[4])
#     dds.append({'id': ids, 'имя': name, 'отдел': otdel, 'зарплата': zp, 'возраст': age})
#     print(f'Имя {name} зарплата {zp} руб')
# print(max(dds, key=lambda o: o['зарплата']))
# print(sum(student['зарплата'] / len_zp for student in dds))
# print(sorted(dds, key=lambda o: o['отдел']))
# print(sorted(dds, key=lambda o: -o['зарплата']))
# print(sorted(dds, key=lambda o: -o['зарплата'])[:3])
# print(list(filter(lambda o: o['возраст'] > 30, dds)))

# import requests
# import json
#
# url = "https://api.bybit.com/v5/market/tickers"
# params = {"category": "spot"}
#
# response = requests.get(url, params=params)
# data = response.json()
#
# # Красиво вывести JSON
# #print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
#
# # Получить список тикеров
# tickers = data["result"]["list"]
#
# # Первый тикер
# first = tickers[0]
# print(first["symbol"])      # "BTCUSDT"
# print(first["lastPrice"])   # "65000.00" (строка!)
# print(float(first["lastPrice"]))  # 65000.0 (число)

# import requests
# import json
#
# # 1. Получи данные о спотовых тикерах
# url = "https://api.bybit.com/v5/market/tickers"
# params = {"category": "spot"}
#
# response = requests.get(url, params=params)
# data = response.json()
#
# # 2. Достань список тикеров
# tickers = data["result"]["list"]
#
# # 3. Выведи первые 5 тикеров
# print("=== Первые 5 тикеров ===")
# for ticker in tickers[:5]:
#     symbol = ticker["symbol"]
#     price = float(ticker["lastPrice"])
#     print(f"{symbol}: ${price:.2f}")
#
# # 4. Найди BTCUSDT
# print("\n=== BTCUSDT ===")
# for ticker in tickers:
#     if ticker["symbol"] == "BTCUSDT":
#         print(f"Цена: ${float(ticker['lastPrice']):.2f}")
#         break
#
# # 5. Топ-5 по объёму торгов
# print("\n=== Топ-5 по объёму ===")
# sorted_tickers = sorted(tickers, key=lambda t: float(t["volume24h"]), reverse=True)
# for ticker in sorted_tickers[:5]:
#     symbol = ticker["symbol"]
#     volume = float(ticker["volume24h"])
#     print(f"{symbol}: ${volume:,.0f}")
#
# with open("bybit_data.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=2, ensure_ascii=False)
#
# try:
#     response = requests.get(url, params=params)
#     response.raise_for_status()  # проверит на ошибки HTTP
#     data = response.json()
# except requests.RequestException as e:
#     print(f"Ошибка запроса: {e}")

# import requests
# import json
#
# # Задача 1: Получи данные с Bybit
# url = "https://api.bybit.com/v5/market/tickers"
# params = {"category": "spot"}
#
# response = requests.get(url, params=params)
# data = response.json()
#
# tickers = data["result"]["list"]
#
# # 1. Выведи общее количество тикеров
# print(f"Всего тикеров: {len(tickers)}")
#
# # 2. Найди все тикеры, заканчивающиеся на USDT
# usdt_pairs = [t for t in tickers if t["symbol"].endswith("USDT")]
# print(f"USDT пар: {len(usdt_pairs)}")
#
# # 3. Найди самый дорогой тикер (по lastPrice)
# d =[]
# for tik in tickers:
#     name = tik["symbol"]
#     price = float(tik["lastPrice"])
#     d.append([name, price])
# print(max(d, key=lambda o: o[1]))
# # 4. Найди самый дешёвый тикер
# u =[]
# for tok in tickers:
#     name = tok["symbol"]
#     price = float(tok["lastPrice"])
#     u.append([name, price])
# print(min(u, key=lambda o: o[1]))
# # 5. Выведи топ-10 по highPrice24h
# high_prices = [[t["symbol"], float(t["highPrice24h"])] for t in tickers]
# top10 = sorted(high_prices, key=lambda o: o[1], reverse=True)[:10]
# print(top10)
# # 6. Сохрани все USDT пары в отдельный JSON файл
# usdt_pairs = [t for t in tickers if t["symbol"].endswith("USDT")]
#
# with open("test_config.json", "w", encoding="utf-8") as f:
#     json.dump(usdt_pairs, f, indent=2, ensure_ascii=False)
#
# # 7. Найди все пары с объёмом > 1,000,000 USDT
# obm = [t["symbol"] for t in usdt_pairs if float(t["volume24h"]) > 1_000_000]
# print(obm)
# # 8. Отсортируй USDT пары по цене (по убыванию)
# prc = [[t["symbol"], float(t["lastPrice"])] for t in usdt_pairs]
# print(sorted(prc, key=lambda o: o[1], reverse=True))
# # 9. Найди среднюю цену всех USDT пар
# obm1 = [float(t["lastPrice"]) for t in usdt_pairs]
# k = 0
# for n in obm1:
#     if n in obm1:
#         k+=1
# print(sum(obm1) / k)
# # 10. Создай словарь {символ: цена} для топ-100 по объёму
# top_100_by_volume = sorted(
#     usdt_pairs,
#     key=lambda t: float(t["volume24h"]),
#     reverse=True
# )[:100]
#
# # Создай словарь {символ: объём}
# volume_dict = {t["symbol"]: float(t["volume24h"]) for t in top_100_by_volume}
# print(volume_dict)

#1
# Создай класс Rectangle (прямоугольник)
# Конструктор принимает width и height
# Метод area() возвращает площадь
# Метод perimeter() возвращает периметр
# Метод is_square() возвращает True, если это квадрат

# class Rectangle:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#     def area(self):
#         return self.width * self.height
#     def perimeter(self):
#         return (self.height + self.width) * 2
#     def is_square(self):
#         if self.width == self.height:
#             return True
#     pass  # твой код здесь
#
# # Тесты:
# rect = Rectangle(5, 3)
# print(rect.area())       # 15
# print(rect.perimeter())  # 16
# print(rect.is_square())  # False
#
# square = Rectangle(4, 4)
# print(square.is_square()) # True
#
# #2
# # Создай класс Student
# # Конструктор: name, grades (список оценок)
# # Метод average() — средний балл
# # Метод add_grade(grade) — добавить оценку
# # Метод is_excellent() — True, если средний балл >= 4.5
#
# class Student:
#     def __init__(self, name, grades):
#         self.name = name
#         self.grades = grades
#     def average(self):
#         return round(sum(self.grades) / len(self.grades), 2)
#     def add_grade(self, number):
#         self.grades.append(number)
#     def is_excellent(self):
#         if self.average() >= 4.5:
#             return True
#         else:
#             False
#     pass  # твой код здесь
#
# # Тесты:
# s = Student("Анна", [5, 4, 5])
# print(s.average())      # 4.67
# s.add_grade(3)
# print(s.average())      # 4.25
# print(s.is_excellent()) # False

# class User:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
# u = User("Анна", 20)
#
# # Пользователь вводит, какое поле показать:
# field = input("Какое поле показать? (name/age): ")
# print(getattr(u, field))  # динамически достаём!

# # Задача 1: @staticmethod
# class Temperature:
#     @staticmethod
#     def c_to_f(celsius):
#         return celsius * 9 / 5 + 32
#
#     @staticmethod
#     def f_to_c(fahrenheit):
#         return (fahrenheit - 32) * 5 / 9
#
#
# # Вызови без создания объекта:
# print(Temperature.c_to_f(25))  # 77.0
# print(Temperature.f_to_c(77))  # 25.0
#
#
# # Задача 2: @classmethod
# class Employee:
#     company = "Tech Inc"
#
#     def __init__(self, name):
#         self.name = name
#
#     @classmethod
#     def change_company(cls, new_name):
#         cls.company = new_name
#
#
# # Измени company через classmethod и проверь:
# Employee.change_company("New Corp")
# print(Employee.company)  # ???
#
#
# # Задача 3: getattr/setattr
# class Config:
#     pass
#
#
# # Создай объект и динамически добавь атрибуты из словаря:
# data = {"host": "localhost", "port": 8080, "debug": True}
# # Твой код здесь

# Создай класс Animal:
# - __init__(name) — сохраняет имя
# - speak() — возвращает "Животное издаёт звук"

# class Animal:
#     def __init__(self, name):
#         self.name = name
#     def speak(self):
#         return "Какое-то животное издаёт звук"
#     pass  # твой код
#
# # Создай класс Dog, наследующий от Animal:
# # - speak() — возвращает "Гав-гав!"
#
# class Dog(Animal):
#     def speak(self):
#         return 'Гав-гав!'
#     pass  # твой код
#
# # Создай класс Cat, наследующий от Animal:
# # - speak() — возвращает "Мяу!"
#
# class Cat(Animal):
#     def speak(self):
#         return 'Мяу!'
#     pass  # твой код
#
# # Тесты:
# dog = Dog("Шарик")
# cat = Cat("Мурка")
# print(dog.name)    # Шарик
# print(dog.speak()) # Гав-гав!
# print(cat.name)    # Мурка
# print(cat.speak()) # Мяу!
#
# # Создай класс BankAccount:
# # - __init__(owner, balance) — сохраняет владельца и баланс
# # - deposit(amount) — увеличивает баланс
# # - withdraw(amount) — уменьшает баланс (если достаточно средств)
# # - info() — возвращает "Владелец: ..., Баланс: ..."
#
# class BankAccount:
#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.balance = balance
#     def deposit(self, ammount):
#         self.ammount = ammount
#         return self.balance + ammount
#     def withdraw(self, ammount):
#         self.ammount = ammount
#         if self.balance > ammount:
#             self.balance - ammount
#         else:
#             return 'Недостаточно средств'
#     def info(self):
#         return f'Владелец: {self.owner}, Баланс: {self.balance}'
#     pass  # твой код
#
# # Создай класс SavingsAccount, наследующий от BankAccount:
# # - __init__(owner, balance, interest_rate) — вызывает super().__init__()
# # - add_interest() — увеличивает баланс на balance * interest_rate
#
# class SavingsAccount(BankAccount):
#     def __init__(self, name, balance, interest_rate):
#         super().__init__(name, balance)
#         self.interest_rate = interest_rate
#     def add_interest(self):
#         self.balance = self.balance * self.interest_rate
#     pass  # твой код
#
# # Тесты:
# acc = SavingsAccount("Анна", 1000, 0.1)
# print(acc.info())      # Владелец: Анна, Баланс: 1000
# acc.add_interest()
# print(acc.info())      # Владелец: Анна, Баланс: 1100

# Исправь и допиши:
#
# class Wallet:
#     def __init__(self, money):
#         self.money = money
#
#     def add(self, amount):
#         self.money += amount
#     def spend(self, amount):
#         if self.money >= amount:
#             self.money -= amount
#         else:
#             return 'Недостаточно средств'
#     # если достаточно денег — вычти, иначе верни "Недостаточно средств"
#
#     def check(self):
#         return f'Ваш текущий баланс {self.money}'
#
# # верни текущий баланс
#
# # Тесты:
# w = Wallet(100)
# w.add(50)
# print(w.check())  # 150
# w.spend(30)
# print(w.check())  # 120
# print(w.spend(200))  # Недостаточно средств

# Создай класс Point:
# - __init__(x, y)
# - __str__ — возвращает "Point(x, y)"
# - __repr__ — возвращает "Point(x, y)"
# - __add__ — складывает координаты
# - __eq__ — сравнивает координаты
# - __len__ — возвращает 2

# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def __str__(self):
#         return f'Point({self.x}, {self.y})'
#     def __repr__(self):
#         return f'Point({self.x}, {self.y})'
#     def __add__(self, other):
#         return self.x + other.x, self.y + other.y
#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y
#     def __len__(self):
#         return 2
#     pass  # твой код
#
# # Тесты:
# p1 = Point(1, 2)
# p2 = Point(3, 4)
# print(p1)          # Point(1, 2)
# p3 = p1 + p2
# print(p3)          # Point(4, 6)
# print(p1 == p2)    # False
# print(len(p1))     # 2
#
# # Создай класс Student:
# # - __init__(name, grades)
# # - __str__ — возвращает "Name: средний балл"
# # - __lt__ — сравнивает по среднему баллу
# # - __eq__ — сравнивает по среднему баллу
#
# class Student:
#     def __init__(self, name, grades):
#         self.name = name
#         self.grades = grades
#     def __str__(self):
#         return f'{self.name}: {sum(self.grades)/len(self.grades)}'
#     def __lt__(self, other):
#         return sum(self.grades)/len(self.grades) < sum(other.grades)/len(other.grades)
#     def __eq__(self, other):
#         return sum(self.grades)/len(self.grades) == sum(other.grades)/len(other.grades)
#     pass  # твой код
#
# # Тесты:
# s1 = Student("Анна", [5, 4, 5])
# s2 = Student("Борис", [3, 4, 3])
# print(s1)          # Анна: 4.67
# print(s1 < s2)     # False
# print(s1 == s2)    # False

# from dataclasses import dataclass, field
#
# # Создай dataclass Book:
# # - title: str
# # - author: str
# # - pages: int
# # - genre: str = "литература"
# # Добавь метод is_long() — True, если pages > 300
#
# @dataclass
# class Book:
#     title: str
#     author: str
#     pages: int
#     genre: str = "литература"
#     def is_long(self):
#         if self.pages > 300:
#             return True
#         else:
#             return False
#
#     pass  # твой код
#
# # Тесты:
# b1 = Book("Война и мир", "Толстой", 1225)
# b2 = Book("Колобок", "народ", 10, "сказка")
# print(b1)          # Book(title='Война и мир', author='Толстой', pages=1225, genre='литература')
# print(b1.is_long())  # True
# print(b2.is_long())  # False

# from dataclasses import dataclass, field
#
# # Создай dataclass Product:
# # - name: str
# # - price: float
# # - tags: list = field(default_factory=list)
# # Добавь метод add_tag(tag) — добавляет тег
#
# @dataclass
# class Product:
#     name: str
#     price: float
#     tags: list = field(default_factory=list)
#     def add_tag(self, tag):
#         self.tags.append(tag)
#     pass  # твой код
#
# # Тесты:
# p1 = Product("ноутбук", 50000)
# p1.add_tag("электроника")
# p1.add_tag("техника")
# print(p1)  # Product(name='ноутбук', price=50000, tags=['электроника', 'техника'])

from dataclasses import dataclass, field

# Создай dataclass User:
# - username: str (обязательное)
# - email: str (обязательное)
# - age: int = 18 (по умолчанию)
# - hobbies: list = field(default_factory=list) (по умолчанию пустой список)
# - settings: dict = field(default_factory=dict) (по умолчанию пустой словарь)
# Метод add_hobby(hobby) — добавляет в hobbies
#
# @dataclass
# class User:
#     username: str
#     email: str
#     age: int = 18
#     hobbies: list = field(default_factory=list)
#     settings: dict = field(default_factory=dict)
#     def add_hobby(self, hobby):
#         self.hobbies.append(hobby)
#     pass  # твой код
#
# # Тесты:
# u1 = User("anna", "anna@example.com")
# u1.add_hobby("чтение")
# print(u1)
# # User(username='anna', email='anna@example.com', age=18, hobbies=['чтение'], settings={})

from typing import Optional

# def find_user(users: list, name: str) -> Optional[str]:
#     for user in users:
#         if user == name:
#             return user  # нашли — возвращаем строку
#     return None  # не нашли — возвращаем None
#
# result = find_user(["Анна", "Борис"], "Вика")
# print(result)  # None — не нашли

print("hello world")