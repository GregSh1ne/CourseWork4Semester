# app/patient/book_appointment.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.database import read_csv, write_csv, get_next_id
from config import COLUMN_WIDTHS, FONT_SIZE

class BookAppointmentWindow(tk.Toplevel):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.title("Запись на прием")
        self.geometry("600x400")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Выбор врача
        ttk.Label(main_frame, text="Врач:").grid(row=0, column=0, sticky='w', pady=5)
        self.doctor_combo = ttk.Combobox(main_frame, state="readonly")
        self.doctor_combo.grid(row=0, column=1, sticky='ew', pady=5)
        
        # Выбор услуги
        ttk.Label(main_frame, text="Услуга:").grid(row=1, column=0, sticky='w', pady=5)
        self.service_combo = ttk.Combobox(main_frame, state="readonly")
        self.service_combo.grid(row=1, column=1, sticky='ew', pady=5)
        
        # Дата приема
        ttk.Label(main_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=2, column=0, sticky='w', pady=5)
        self.date_entry = ttk.Entry(main_frame)
        self.date_entry.grid(row=2, column=1, sticky='ew', pady=5)
        
        # Время приема
        ttk.Label(main_frame, text="Время (ЧЧ:ММ):").grid(row=3, column=0, sticky='w', pady=5)
        self.time_entry = ttk.Entry(main_frame)
        self.time_entry.grid(row=3, column=1, sticky='ew', pady=5)
        
        # Кнопка записи
        ttk.Button(main_frame, text="Записаться", command=self.submit).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Загрузка данных
        self.load_doctors()
        self.load_services()
    

    def load_doctors(self):
        doctors = read_csv("doctors.csv")
        doctor_list = [
            f"{d['surname']} {d['name']} ({d['specialization']})" 
            for d in doctors
        ]
        self.doctor_combo['values'] = doctor_list
        if doctor_list:
            self.doctor_combo.current(0)

    def load_services(self):
        services = read_csv("services.csv")
        service_list = [f"{s['service_name']} ({s['price']} руб.)" for s in services]
        self.service_combo['values'] = service_list
        if service_list:
            self.service_combo.current(0)

    def submit(self):
        # Получение данных
        doctor_str = self.doctor_combo.get()
        service_str = self.service_combo.get()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        
        # Валидация
        if not all([doctor_str, service_str, date, time]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
            
        # Парсинг данных
        try:
            doctors = read_csv("doctors.csv")
            services = read_csv("services.csv")
            
            # Получаем ID врача
            doctor_name = doctor_str.split(' (')[0]
            doctor = next(
                d for d in doctors 
                if f"{d['surname']} {d['name']}" == doctor_name
            )
            
            # Получаем ID услуги
            service_name = service_str.split(' (')[0]
            service = next(s for s in services if s['service_name'] == service_name)
            
            # Проверка занятости врача
            appointments = read_csv("appointments.csv")
            for appt in appointments:
                if (
                    appt['doctor_id'] == doctor['doctor_id'] and
                    appt['date'] == date and
                    appt['time'] == time
                ):
                    messagebox.showerror("Ошибка", "У выбранного врача уже есть запись на это время.")
                    return
            
            # Создаем запись
            new_appointment = {
                "appointment_id": get_next_id("appointments.csv"),
                "patient_id": self.main_menu.app.current_user['patient_id'],
                "doctor_id": doctor['doctor_id'],
                "service_id": service['service_id'],
                "date": date,
                "time": time,
                "status": "Ожидается",
                "office": doctor['office']
            }
            
            # Сохранение в CSV
            appointments = read_csv("appointments.csv")
            appointments.append(new_appointment)
            write_csv("appointments.csv", appointments)
            
            messagebox.showinfo("Успех", "Запись успешно создана!")
            self.destroy()
            self.main_menu.load_patient_appointments()  # Обновляем через main_menu
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при записи: {str(e)}")
