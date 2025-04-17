# app/patient/payment.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import COLUMN_WIDTHS, FONT_SIZE

class PaymentWindow(tk.Toplevel):
    def __init__(self, app, callback):
        super().__init__()
        self.app = app
        self.callback = callback
        self.title("Оплата")
        self.geometry("1200x900")
        
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH)
        
        # Создание полей ввода
        self.entries = {}
        fields = [
            ("Номер карты:", 0),
            ("Срок действия (ММ/ГГ):", 1),
            ("Владелец:", 2),
            ("CVC/CVV:", 3)
        ]
        
        for text, row in fields:
            ttk.Label(form_frame, text=text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(form_frame)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
            self.entries[text] = entry  # Сохраняем по тексту метки
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Оплатить", 
                  command=self.process_payment).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", 
                  command=self.destroy).pack(side=tk.LEFT, padx=10)
        
    def process_payment(self):
        card = self.entries["Номер карты:"].get().replace(" ", "")
        expiry = self.entries["Срок действия (ММ/ГГ):"].get()
        cvv = self.entries["CVC/CVV:"].get()
        
        # Проверка номера карты (16 цифр)
        if len(card) != 16 or not card.isdigit():
            messagebox.showerror("Ошибка", "Некорректный номер карты")
            return
        
        # Проверка срока действия (MM/YY)
        try:
            month, year = expiry.split('/')
            if len(month) != 2 or len(year) != 2 or int(month) > 12:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Некорректный срок действия")
            return
        
        # Проверка CVV (3 цифры)
        if len(cvv) != 3 or not cvv.isdigit():
            messagebox.showerror("Ошибка", "Некорректный CVV")
            return
        
        # После успешной оплаты
        if self.callback:
            self.callback("APT-1")  # Передаем реальный ID приема
        self.destroy()

class PaymentSelectionWindow(tk.Toplevel):
    def __init__(self, app, callback):
        super().__init__()
        self.app = app
        self.callback = callback
        self.title("Выбор услуг для оплаты")
        self.geometry("1200x800")
        
        # Таблица услуг
        self.tree = ttk.Treeview(self, columns=("Услуга", "Цена"), show="headings")
        self.tree.heading("Услуга", text="Услуга")
        self.tree.heading("Цена", text="Цена")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заполнение тестовыми данными
        services = [
            ("Консультация терапевта", "1500 руб"),
            ("Анализы крови", "2500 руб"),
            ("УЗИ обследование", "3500 руб")
        ]
        for service in services:
            self.tree.insert("", "end", values=service)
        
        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Оплатить", 
                  command=lambda: self.open_payment_window()).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", 
                  command=self.destroy).pack(side=tk.LEFT, padx=10)

    def open_payment_window(self):
        self.destroy()
        PaymentWindow(self.app, self.callback)
