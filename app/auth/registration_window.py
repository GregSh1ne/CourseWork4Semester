# app/auth/registration_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_SIZE

class RegistrationWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Регистрация пациента")
        self.geometry("900x1800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Регистрация нового пациента", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        fields = [
            ("Фамилия", 0),
            ("Имя", 1),
            ("Отчество", 2),
            ("Номер телефона", 3),
            ("Пароль", 4),
            ("Дата рождения", 5),
            ("Адрес", 6)
        ]
        
        self.entries = {}
        for text, row in fields:
            ttk.Label(form_frame, text=text+":").grid(row=row, column=0, padx=15, pady=10, sticky='e')
            entry = ttk.Entry(form_frame, width=35)
            entry.grid(row=row, column=1, padx=15, pady=10)
            self.entries[text] = entry
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Зарегистрироваться", command=self.submit, width=20).pack(side=tk.LEFT, padx=20)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=20).pack(side=tk.LEFT, padx=20)
    
    def submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        if all(data.values()):
            messagebox.showinfo("Успех", "Регистрация завершена!")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
