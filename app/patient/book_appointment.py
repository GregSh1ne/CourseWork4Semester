# app/patient/book_appointment.py
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

        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Записать", 
                  command=self.book_appointment, width=15).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", 
                  command=self.destroy, width=15).pack(side=tk.LEFT, padx=15)
    
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
