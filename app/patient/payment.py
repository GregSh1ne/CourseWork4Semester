# app/patient/payment.py
import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime
from config import COLUMN_WIDTHS, FONT_SIZE
from app.database import read_csv, write_csv, get_next_id

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
    def __init__(self, main_menu, appointment_id, callback):
        super().__init__()
        self.main_menu = main_menu
        self.appointment_id = appointment_id
        self.callback = callback
        self.title("Выбор способа оплаты")
        self.geometry("300x200")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Выберите способ оплаты:").pack(pady=10)
        
        ttk.Button(main_frame, text="Банковской картой", 
                 command=self.open_card_payment).pack(pady=5)
        ttk.Button(main_frame, text="Наличными", 
                 command=lambda: self.process_payment("наличные")).pack(pady=5)
        ttk.Button(main_frame, text="Отмена", 
                 command=self.destroy).pack(pady=10)

    def open_card_payment(self):
        CardPaymentWindow(self.main_menu, self.appointment_id, self.callback)
        self.destroy()

    def process_payment(self, method):
        try:
            appointments = read_csv("appointments.csv")
            services = read_csv("services.csv")
            
            for appt in appointments:
                if appt['appointment_id'] == self.appointment_id:
                    if appt['status'] != 'Ожидается':
                        messagebox.showwarning("Ошибка", "Нельзя оплатить этот прием")
                        return
                    
                    # Получаем стоимость услуги
                    service = next((s for s in services if s['service_id'] == appt['service_id']), None)
                    if not service:
                        raise ValueError("Услуга не найдена")
                    
                    # Создаем запись об оплате
                    new_payment = {
                        "payment_id": get_next_id("payments.csv"),
                        "appointment_id": self.appointment_id,
                        "amount": service['price'],
                        "payment_method": method,
                        "payment_date": datetime.now().strftime("%d.%m.%Y")
                    }
                    
                    # Обновляем статус и сохраняем
                    appt['status'] = 'Оплачено'
                    write_csv("appointments.csv", appointments)
                    write_csv("payments.csv", read_csv("payments.csv") + [new_payment])
                    
                    break
            
            messagebox.showinfo("Успех", f"Оплата {method} прошла успешно!")
            self.callback(self.appointment_id)
            self.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка оплаты: {str(e)}")

class CardPaymentWindow(tk.Toplevel):
    def __init__(self, main_menu, appointment_id, callback):
        super().__init__()
        self.main_menu = main_menu
        self.appointment_id = appointment_id
        self.callback = callback
        self.title("Оплата картой")
        self.geometry("400x300")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Поля ввода
        fields = [
            ("Номер карты", "card_number", "16 цифр"),
            ("Срок действия", "expiry", "ММ/ГГ"),
            ("CVV/CVC", "cvv", "3 цифры"),
            ("Имя владельца", "name", "")
        ]
        
        self.entries = {}
        for idx, (label, key, hint) in enumerate(fields):
            full_label = f"{label} ({hint})" if hint else label
            ttk.Label(main_frame, text=full_label).grid(row=idx, column=0, sticky='w', pady=5)
            entry = ttk.Entry(main_frame)
            entry.grid(row=idx, column=1, sticky='ew', pady=5)
            self.entries[key] = entry
            
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Оплатить", command=self.process_card_payment).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Назад", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def process_card_payment(self):
        # Получение данных
        card_number = self.entries['card_number'].get().replace(" ", "")
        expiry = self.entries['expiry'].get()
        cvv = self.entries['cvv'].get()
        name = self.entries['name'].get().strip()
        
        # Валидация
        errors = []
        if not (len(card_number) == 16 and card_number.isdigit()):
            errors.append("Неверный номер карты")
        if not re.match(r"^(0[1-9]|1[0-2])\/?([0-9]{2})$", expiry):
            errors.append("Неверный формат срока действия")
        if not (len(cvv) == 3 and cvv.isdigit()):
            errors.append("Неверный CVV/CVC")
        if not name:
            errors.append("Введите имя владельца")
            
        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return
            
        # Обработка оплаты
        try:
            appointments = read_csv("appointments.csv")
            services = read_csv("services.csv")
            
            for appt in appointments:
                if appt['appointment_id'] == self.appointment_id:
                    service = next((s for s in services if s['service_id'] == appt['service_id']), None)
                    if not service:
                        raise ValueError("Услуга не найдена")
                    
                    new_payment = {
                        "payment_id": get_next_id("payments.csv"),
                        "appointment_id": self.appointment_id,
                        "amount": service['price'],
                        "payment_method": "карта",
                        "payment_date": datetime.now().strftime("%d.%m.%Y")
                    }
                    
                    appt['status'] = 'Оплачено'
                    
                    write_csv("appointments.csv", appointments)
                    write_csv("payments.csv", read_csv("payments.csv") + [new_payment])
            
            messagebox.showinfo("Успех", "Оплата картой прошла успешно!")
            self.callback(self.appointment_id)
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка оплаты: {str(e)}")
