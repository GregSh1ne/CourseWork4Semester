# app/admin/add_doctor.py
import tkinter as tk
from tkinter import ttk, messagebox
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
            ("Специализация", 4),
            ("Квалификация", 5),
            ("Номер кабинета", 6)
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
        data = {
            'Фамилия': self.entries['Фамилия'].get(),
            'Имя': self.entries['Имя'].get(),
            'Отчество': self.entries['Отчество'].get(),
            'Телефон': self.entries['Телефон'].get(),
            'Специализация': self.entries['Специализация'].get(),
            'Квалификация': self.entries['Квалификация'].get(),
            'Номер кабинета': self.entries['Номер кабинета'].get()
        }
        
        # Валидация данных
        errors = []
        if not data['Фамилия'] or not data['Имя']:
            errors.append("ФИО обязательно для заполнения")
        
        if not data['Телефон'].isdigit() or len(data['Телефон']) != 11:
            errors.append("Некорректный номер телефона (11 цифр)")
        
        if not data['Номер кабинета'].isdigit():
            errors.append("Номер кабинета должен быть числом")
        
        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return
        
        # Здесь должна быть логика сохранения в БД
        messagebox.showinfo("Успех", "Врач успешно добавлен!")
        self.destroy()
