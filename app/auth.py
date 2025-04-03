import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_SIZE

class AuthWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Авторизация")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=80, padx=80, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Система управления поликлиникой", 
                 font=('Arial', FONT_SIZE+4)).pack(pady=30)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=30)
        
        ttk.Label(form_frame, text="Номер телефона:").grid(row=0, column=0, padx=15, pady=15, sticky='e')
        self.phone_entry = ttk.Entry(form_frame, width=25)
        self.phone_entry.grid(row=0, column=1, padx=15, pady=15)
        
        ttk.Label(form_frame, text="Пароль:").grid(row=1, column=0, padx=15, pady=15, sticky='e')
        self.password_entry = ttk.Entry(form_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=15, pady=15)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Войти", command=self.login, width=15).pack(side=tk.LEFT, padx=25)
        ttk.Button(btn_frame, text="Регистрация", command=self.open_registration, width=15).pack(side=tk.LEFT, padx=25)
    
    def login(self):
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        
        if phone and password:
            self.app.current_user = phone
            if phone == "admin" and password == "1234":
                self.app.show_main_menu("Главный врач")
            elif phone == "doctor" and password == "1234":
                self.app.show_main_menu("Врач")
            else:
                self.app.show_main_menu("Пациент")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")
    
    def open_registration(self):
        RegistrationWindow(self.app)

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
