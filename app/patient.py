import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config import COLUMN_WIDTHS, FONT_SIZE

class BookAppointmentWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Запись на прием")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Запись на прием к врачу", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        # Выбор врача
        ttk.Label(form_frame, text="Выберите врача:").grid(row=0, column=0, padx=15, pady=15, sticky='e')
        self.doctor_var = tk.StringVar()
        self.doctor_combobox = ttk.Combobox(
            form_frame, 
            textvariable=self.doctor_var,
            values=[f"Доктор {i} ({spec})" for i, spec in enumerate(["Терапевт", "Хирург", "Кардиолог"], 1)],
            width=40
        )
        self.doctor_combobox.grid(row=0, column=1, padx=15, pady=15)
        
        # Выбор услуги
        ttk.Label(form_frame, text="Выберите услугу:").grid(row=1, column=0, padx=15, pady=15, sticky='e')
        self.service_var = tk.StringVar()
        self.service_combobox = ttk.Combobox(
            form_frame, 
            textvariable=self.service_var,
            values=[f"Консультация {i} ({500+i*100} руб.)" for i in range(1, 6)],
            width=40
        )
        self.service_combobox.grid(row=1, column=1, padx=15, pady=15)
        
        # Выбор даты и времени
        ttk.Label(form_frame, text="Дата приема:").grid(row=2, column=0, padx=15, pady=15, sticky='e')
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.grid(row=2, column=1, padx=15, pady=15)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        
        ttk.Label(form_frame, text="Время приема:").grid(row=3, column=0, padx=15, pady=15, sticky='e')
        self.time_combobox = ttk.Combobox(
            form_frame, 
            values=[f"{h:02d}:{m:02d}" for h in range(8, 20) for m in [0, 30]],
            width=10
        )
        self.time_combobox.grid(row=3, column=1, padx=15, pady=15)
        self.time_combobox.set("10:00")
        
        # Календарь (упрощенная реализация)
        ttk.Label(form_frame, text="Доступные даты:").grid(row=4, column=0, padx=15, pady=15, sticky='ne')
        self.calendar_frame = ttk.Frame(form_frame)
        self.calendar_frame.grid(row=4, column=1, padx=15, pady=15, sticky='w')
        
        for i, day in enumerate(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]):
            ttk.Button(self.calendar_frame, text=f"{day}\n{i+10}.07", width=8).grid(row=0, column=i, padx=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Записаться", command=self.book_appointment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)
    
    def book_appointment(self):
        data = {
            'doctor': self.doctor_var.get(),
            'service': self.service_var.get(),
            'date': self.date_entry.get(),
            'time': self.time_combobox.get()
        }
        
        if all(data.values()):
            try:
                datetime.strptime(data['date'], "%d.%m.%Y")
                datetime.strptime(data['time'], "%H:%M")
                messagebox.showinfo("Успех", "Вы успешно записаны на прием!")
                self.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты или времени")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

class PaymentWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Оплата услуг")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Оплата медицинских услуг", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        # Информация о платеже
        payment_info_frame = ttk.Frame(main_frame)
        payment_info_frame.pack(pady=20)
        
        ttk.Label(payment_info_frame, text="Сумма к оплате:").grid(row=0, column=0, padx=15, pady=10, sticky='e')
        ttk.Label(payment_info_frame, text="1500 руб.", font=('Arial', FONT_SIZE, 'bold')).grid(row=0, column=1, padx=15, pady=10, sticky='w')
        
        ttk.Label(payment_info_frame, text="Услуга:").grid(row=1, column=0, padx=15, pady=10, sticky='e')
        ttk.Label(payment_info_frame, text="Консультация терапевта").grid(row=1, column=1, padx=15, pady=10, sticky='w')
        
        # Данные карты
        card_frame = ttk.Frame(main_frame)
        card_frame.pack(pady=20)
        
        ttk.Label(card_frame, text="Номер карты:").grid(row=0, column=0, padx=15, pady=10)
        self.card_entry = ttk.Entry(card_frame, width=25)
        self.card_entry.grid(row=0, column=1, padx=15, pady=10)
        
        ttk.Label(card_frame, text="Срок действия (ММ/ГГ):").grid(row=1, column=0, padx=15, pady=10)
        self.expiry_entry = ttk.Entry(card_frame, width=10)
        self.expiry_entry.grid(row=1, column=1, padx=15, pady=10)
        
        ttk.Label(card_frame, text="CVV/CVC:").grid(row=2, column=0, padx=15, pady=10)
        self.cvv_entry = ttk.Entry(card_frame, width=5, show="*")
        self.cvv_entry.grid(row=2, column=1, padx=15, pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Оплатить", command=self.process_payment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)
    
    def process_payment(self):
        card = self.card_entry.get().replace(" ", "")
        expiry = self.expiry_entry.get()
        cvv = self.cvv_entry.get()
        
        if len(card) != 16 or not card.isdigit():
            messagebox.showerror("Ошибка", "Некорректный номер карты")
            return
        
        try:
            month, year = expiry.split('/')
            if len(month) != 2 or len(year) != 2 or not (1 <= int(month) <= 12):
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Некорректный срок действия")
            return
        
        if len(cvv) != 3 or not cvv.isdigit():
            messagebox.showerror("Ошибка", "Некорректный CVV")
            return
        
        messagebox.showinfo("Успех", "Оплата прошла успешно!")
        self.destroy()
