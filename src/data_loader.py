from src.config import BASE_DIR


def count_lines_in_file(file_name: str):
    """Считает количество строк в файле из папки data/raw/"""

    # Собираем путь к файлу через наш config
    file_path = BASE_DIR / "data" / "raw" / file_name

    # Открываем файл на чистом Python (без сторонних библиотек)
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return len(lines)


if __name__ == "__main__":
    # Проверяем работу функции
    total_lines = count_lines_in_file("test.txt")
    print(f"В файле строк: {total_lines}")