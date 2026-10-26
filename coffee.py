import numpy as np
import pandas as pd

# Показывать все колонки таблицы
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# 1. Чтение данных
try:
    df = pd.read_excel("Coffee Shop Sales.xlsx", sheet_name="Transactions")
except FileNotFoundError:
    print("Файл Coffee Shop Sales.xlsx не найден. Положите его в папку с программой.")
    exit()

print("Первые 5 строк:")
print(df.head())
print("\nОбщая информация:")
df.info()
print("\nСтатистика:")
print(df.describe())


# 2. Фильтрация
while True:
    try:
        threshold = float(input("\nВведите порог цены (например, 3): "))
        break
    except ValueError:
        print("Ошибка: нужно ввести число.")

# Спрашиваем категорию, пока не введут существующую
categories = df["product_category"].unique()
print("Категории:", ", ".join(categories))
while True:
    category = input("Введите категорию: ")
    if category in categories:
        break
    print("Ошибка: такой категории нет.")

filtered = df[(df["unit_price"] > threshold) & (df["product_category"] == category)]
print("\nКоличество строк после фильтрации:", len(filtered))
print(filtered.head())

# 3. Группировка по категории
grouped = df.groupby("product_category").agg(
    transactions=("transaction_id", "count"),
    avg_price=("unit_price", "mean"),
    total_qty=("transaction_qty", "sum"),
    max_price=("unit_price", "max"),
)
grouped = grouped.sort_values("avg_price", ascending=False)
print("\nГруппировка по категориям:")
print(grouped)

# 4. Новый столбец
mean_price = df["unit_price"].mean()
df["price_level"] = np.where(df["unit_price"] > mean_price, "выше среднего", "ниже или равно")
print("\nСредняя цена:", round(mean_price, 2))
print(df[["unit_price", "price_level"]].head())

prices = df["unit_price"].to_numpy()
print("\nСреднее:", prices.mean())
print("Стандартное отклонение:", prices.std())
print("Максимум:", prices.max())
print("Минимум:", prices.min())

normalized = (prices - prices.min()) / (prices.max() - prices.min())
print("Первые 5 нормализованных значений:", normalized[:5])


# 6. Сохранение
df.to_csv("processed_coffee.csv", index=False)
print("\nФайл processed_coffee.csv сохранён.")


# Ответы на вопросы
print("\nСтрок после фильтрации:", len(filtered))
print("Самая высокая средняя цена у категории:", grouped.index[0])
