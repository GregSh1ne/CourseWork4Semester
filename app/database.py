import csv
from pathlib import Path
from typing import List, Dict

# Путь к папке data (относительно расположения этого файла)
DATA_DIR = Path(__file__).parent / "data"


"""Читает данные из CSV-файла и возвращает список словарей."""
def read_csv(filename: str) -> List[Dict]:
    file_path = DATA_DIR / filename
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []  # Возвращаем пустой список, если файл не найден

"""Записывает данные в CSV-файл."""
def write_csv(filename: str, data: List[Dict]):
    file_path = DATA_DIR / filename
    if not data:
        return  # Не записываем пустые данные

    # Извлекаем заголовки из первого элемента данных
    fieldnames = data[0].keys()
    
    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

"""Генерирует следующий уникальный ID для новой записи."""
def get_next_id(filename: str) -> int:
    records = read_csv(filename)
    if not records:
        return 1  # Если файл пуст, начинаем с ID = 1
    # Предполагаем, что первый столбец — это ID (например, "patient_id", "doctor_id")
    first_column = list(records[0].keys())[0]
    return max(int(record[first_column]) for record in records) + 1