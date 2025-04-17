# app/admin/add_doctor.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.database import read_csv, write_csv, get_next_id
from config import COLUMN_WIDTHS, FONT_SIZE

class AddDoctorWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Добавление врача")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Добавление нового врача", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Поля формы
        fields = [
        ("Фамилия", 0),
        ("Имя", 1),
        ("Отчество", 2),
        ("Телефон", 3),
        ("Пароль", 4),  # Новое поле
        ("Специализация", 5),
        ("Квалификация", 6),
        ("Номер кабинета", 7)
        ]
        
        self.entries = {}
        for text, row in fields:
            ttk.Label(form_frame, text=text+":").grid(row=row, column=0, padx=15, pady=10, sticky='e')
            
            if text == "Специализация":
                entry = ttk.Combobox(form_frame, values=["Терапевт", "Хирург", "Кардиолог", "Офтальмолог", "Невролог"], width=32)
            elif text == "Квалификация":
                entry = ttk.Combobox(form_frame, values=["Высшая категория", "Первая категория", "Вторая категория", "Без категории"], width=32)
            else:
                entry = ttk.Entry(form_frame, width=35)
                
            entry.grid(row=row, column=1, padx=15, pady=10)
            self.entries[text] = entry
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.save_doctor, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Отмена", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)
    
    def save_doctor(self):
        # Сбор данных из полей ввода
        data = {
            "surname": self.entries["Фамилия"].get().strip(),
            "name": self.entries["Имя"].get().strip(),
            "patronymic": self.entries["Отчество"].get().strip(),
            "phone": self.entries["Телефон"].get().strip(),
            "password": self.entries["Пароль"].get().strip(),  # Новое поле
            "specialization": self.entries["Специализация"].get().strip(),
            "qualification": self.entries["Квалификация"].get().strip(),
            "office": self.entries["Номер кабинета"].get().strip()
        }

        # Валидация данных
        errors = []
        if not data["surname"] or not data["name"]:
            errors.append("Фамилия и имя обязательны для заполнения.")
        
        # Очистка номера телефона и проверка формата
        phone = data["phone"]
        cleaned_phone = "".join(filter(lambda c: c.isdigit() or c == "+", phone))
        
        # Проверка формата: +7XXXXXXXXXX (12 символов)
        if (
            not cleaned_phone.startswith("+7") 
            or len(cleaned_phone) != 12 
            or not cleaned_phone[1:].isdigit()
        ):
            errors.append("Некорректный номер телефона. Формат: +7XXXXXXXXXX")
        else:
            data["phone"] = cleaned_phone  # Сохраняем очищенный номер
        
        if not data["password"]:
            errors.append("Пароль не может быть пустым.")
        if not data["office"].isdigit():
            errors.append("Номер кабинета должен быть числом.")

        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return

        try:
            # Чтение существующих данных
            doctors = read_csv("doctors.csv")
            # Генерация нового ID
            new_id = get_next_id("doctors.csv")
            # Создание записи врача
            new_doctor = {
                "doctor_id": new_id,
                **data
            }
            doctors.append(new_doctor)
            # Сохранение в CSV
            write_csv("doctors.csv", doctors)
            messagebox.showinfo("Успех", "Врач успешно добавлен!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")