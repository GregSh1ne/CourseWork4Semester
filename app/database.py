import csv
import sys
import os
from pathlib import Path
from typing import List, Dict

def resource_path(relative_path):
    """Возвращает корректный путь для ресурсов в dev и .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Обновляем путь к данным
DATA_DIR = resource_path(str(Path(__file__).parent / "data"))  # <-- Изменено


def read_csv(filename: str) -> List[Dict]:
    file_path = Path(DATA_DIR) / filename  # <-- Используем новый путь
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

def write_csv(filename: str, data: List[Dict]):
    file_path = Path(DATA_DIR) / filename  # <-- Используем новый путь
    if not data:
        return

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