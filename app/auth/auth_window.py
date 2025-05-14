# app/auth/auth_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_SIZE
from app.auth.registration_window import RegistrationWindow
from app.database import read_csv

class AuthWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Авторизация")
        self.geometry("800x600")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Система управления поликлиникой", 
                 font=('Arial', FONT_SIZE+4)).pack(pady=30)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=30)
        
        # Поля ввода
        ttk.Label(main_frame, text="Телефон:").pack(pady=5)
        self.phone_entry = ttk.Entry(main_frame)
        self.phone_entry.pack(pady=5)
        
        ttk.Label(main_frame, text="Пароль:").pack(pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(pady=5)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Регистрация", command=self.open_registration).pack(side=tk.LEFT, padx=10)
    
    def login(self):
        phone = self.phone_entry.get().strip()  # Используем правильное имя
        password = self.password_entry.get()
        
        # Нормализация номера телефона
        cleaned_phone = ''.join([c for c in phone if c.isdigit()])
        normalized_phone = None
        
        if len(cleaned_phone) == 10:
            normalized_phone = f"+7{cleaned_phone}"
        elif len(cleaned_phone) == 11:
            normalized_phone = f"+{cleaned_phone}"
        else:
            normalized_phone = f"+7{cleaned_phone[-10:]}"  # Попытка восстановления номера

        # Проверка администратора
        if normalized_phone == "+79991231122" and password == "321":
            self.app.current_user = {'role': 'admin', 'phone': normalized_phone}
            self.app.show_main_menu("Главный врач")
            self.destroy()
            return
        
        # Проверка регистратуры
        if normalized_phone == "+78005553535" and password == "123":
            self.app.current_user = {'role': 'registry', 'phone': normalized_phone}
            self.app.show_main_menu("Регистратура")
            self.destroy()
            return
        
        # Проверка врачей
        doctors = read_csv("doctors.csv")
        user = next((d for d in doctors if d['phone'] == normalized_phone and d['password'] == password), None)
        if user:
            self.app.current_user = user
            self.app.show_main_menu("Врач")
            self.destroy()
            return
        
        # Проверка пациентов
        patients = read_csv("patients.csv") 
        patient = next((p for p in patients if p['phone'] == normalized_phone and p['password'] == password), None)
        if patient:
            self.app.current_user = patient
            self.app.show_main_menu("Пациент")
            self.destroy()
            return
        
        messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def open_registration(self):
        RegistrationWindow(self.app)
