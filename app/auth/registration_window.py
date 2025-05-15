# app/auth/registration_window.py
import re
import tkinter as tk
from tkinter import ttk, messagebox
from app.database import read_csv, write_csv, get_next_id

class RegistrationWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Регистрация пациента")
        self.geometry("500x500")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        # Поля формы согласно структуре patients.csv
        fields = [
            ("Телефон*", 0),
            ("Пароль*", 1),
            ("Фамилия*", 2),
            ("Имя*", 3),
            ("Отчество", 4),
            ("Дата рождения (ДД.ММ.ГГГГ)", 5),
            ("Адрес", 6)
        ]
        
        self.entries = {}
        for text, row in fields:
            ttk.Label(main_frame, text=text).grid(row=row, column=0, pady=5, sticky='w')
            entry = ttk.Entry(main_frame)
            entry.grid(row=row, column=1, pady=5, padx=10, sticky='ew')
            self.entries[text.replace('*', '').strip()] = entry

        ttk.Button(
            main_frame, 
            text="Зарегистрироваться", 
            command=self.submit
        ).grid(row=7, column=0, columnspan=2, pady=20)

    def submit(self):
        data = {
            'phone': self.entries['Телефон'].get().strip(),
            'password': self.entries['Пароль'].get(),
            'surname': self.entries['Фамилия'].get().strip(),
            'name': self.entries['Имя'].get().strip(),
            'patronymic': self.entries['Отчество'].get().strip(),
            'birth_date': self.entries['Дата рождения (ДД.ММ.ГГГГ)'].get().strip(),
            'address': self.entries['Адрес'].get().strip()
        }

        # Проверка обязательных полей
        required_fields = ['phone', 'password', 'surname', 'name']
        if not all(data[field] for field in required_fields):
            messagebox.showerror("Ошибка", "Заполните обязательные поля (*)")
            return

        # Нормализация телефона
        cleaned_phone = ''.join(filter(str.isdigit, data['phone']))
        if len(cleaned_phone) not in [10, 11]:
            messagebox.showerror("Ошибка", "Некорректный формат телефона")
            return
        data['phone'] = f"+7{cleaned_phone[-10:]}"

        # Проверка формата даты
        if data['birth_date'] and not re.match(r"^\d{2}\.\d{2}\.\d{4}$", data['birth_date']):
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ДД.ММ.ГГГГ")
            return

        # Проверка существующего номера
        patients = read_csv("patients.csv")
        if any(p['phone'] == data['phone'] for p in patients):
            messagebox.showerror("Ошибка", "Этот номер уже зарегистрирован")
            return

        try:
            # Создание новой записи
            new_patient = {
                'patient_id': get_next_id("patients.csv"),
                **data
            }
            
            patients.append(new_patient)
            write_csv("patients.csv", patients)
            
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")