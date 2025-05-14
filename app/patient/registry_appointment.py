# app/patient/registry_appointment.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_SIZE
from app.database import read_csv, write_csv, get_next_id
import random

class RegistryAppointmentWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Запись на прием")
        self.geometry("1200x800")
        
        # Загрузка данных
        self.doctors = read_csv("doctors.csv")
        self.services = read_csv("services.csv")
        
        # Добавляем ссылку на main_frame
        self.main_frame = ttk.Frame(self)  # <-- Исправлено
        self.main_frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)
        
        # Поля ввода
        fields = [
            ("Дата (ДД.ММ.ГГГГ):", "entry_date"),
            ("Время:", "combo_time"),
            ("Скидка (%):", "combo_discount"),
            ("Специалист:", "combo_specialist"),
            ("Услуга:", "combo_service")
        ]
        
        self.entries = {}
        for i, (label, name) in enumerate(fields):
            ttk.Label(self.main_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if "combo" in name:
                entry = ttk.Combobox(self.main_frame)
                if "specialist" in name:
                    specializations = list(set(d['specialization'] for d in self.doctors))
                    entry['values'] = specializations
                    entry.bind("<<ComboboxSelected>>", self.update_doctors)
                elif "service" in name:
                    services = [f"{s['service_name']} ({s['price']} руб.)" for s in self.services]
                    entry['values'] = services
                elif "time" in name:
                    entry['values'] = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
                elif "discount" in name:
                    entry['values'] = ["0", "5", "10", "15"]
            else:
                entry = ttk.Entry(self.main_frame)
            
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.entries[name] = entry

        # Блок с выбором аккаунта
        ttk.Label(self.main_frame, text="У пациента есть аккаунт?").grid(row=5, column=0, columnspan=2, pady=10)
        
        self.account_var = tk.StringVar(value="no")
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=5)
        
        ttk.Radiobutton(btn_frame, text="Да", variable=self.account_var, 
                       value="yes", command=self.toggle_phone_input).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(btn_frame, text="Нет", variable=self.account_var, 
                       value="no", command=self.toggle_phone_input).pack(side=tk.LEFT, padx=10)
        
        # Поле для телефона
        self.phone_frame = ttk.Frame(self.main_frame)
        ttk.Label(self.phone_frame, text="Телефон:").pack(side=tk.LEFT, padx=5)
        self.phone_entry = ttk.Entry(self.phone_frame)
        self.phone_entry.pack(side=tk.LEFT, expand=True)
        
        # Кнопки
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Выход", 
                  command=self.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Запись", 
                  command=self.create_record).pack(side=tk.LEFT, padx=10)

    def update_doctors(self, event):
        specialization = self.entries['combo_specialist'].get()
        doctors = [d for d in self.doctors if d['specialization'] == specialization]
        
        # Если комбобокс врачей еще не создан
        if 'combo_doctor' not in self.entries:
            ttk.Label(self.main_frame, text="Врач:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
            self.entries['combo_doctor'] = ttk.Combobox(self.main_frame)
            self.entries['combo_doctor'].grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        
        # Обновляем значения
        self.entries['combo_doctor']['values'] = [
            f"{d['surname']} {d['name']} (каб. {d['office']})" 
            for d in doctors
        ]

    def toggle_phone_input(self):
        if self.account_var.get() == "yes":
            self.phone_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        else:
            self.phone_frame.grid_forget()

    def create_record(self):
        try:
            # Валидация выбора врача
            if 'combo_doctor' in self.entries and not self.entries['combo_doctor'].get():
                raise ValueError("Выберите врача из списка")
            
            # Сбор данных
            data = {
                'date': self.entries['entry_date'].get(),
                'time': self.entries['combo_time'].get(),
                'discount': self.entries['combo_discount'].get() or '0',
                'specialization': self.entries['combo_specialist'].get(),
                'service': self.entries['combo_service'].get().split(' (')[0],
                'phone': self.phone_entry.get() if self.account_var.get() == "yes" else None
            }

            # Валидация
            if not all([data['date'], data['time'], data['specialization'], data['service']]):
                raise ValueError("Заполните все обязательные поля")

            # Поиск пациента
            patient_id = None
            if data['phone']:
                patients = read_csv("patients.csv")
                patient = next((p for p in patients if p['phone'] == data['phone']), None)
                if not patient:
                    raise ValueError("Пациент с таким телефоном не найден")
                patient_id = patient['patient_id']

            # Поиск услуги
            service = next((s for s in self.services if s['service_name'] == data['service']), None)
            if not service:
                raise ValueError("Услуга не найдена")

            # Поиск врача
            doctors = [d for d in self.doctors if d['specialization'] == data['specialization']]
            if not doctors:
                raise ValueError("Нет доступных врачей этой специализации")
            doctor = random.choice(doctors)

            # Получаем выбранного врача
            doctor_str = self.entries['combo_doctor'].get()
            doctor_id = next(
                d['doctor_id'] for d in self.doctors 
                if f"{d['surname']} {d['name']} (каб. {d['office']})" == doctor_str
            )
            
            # Формируем запись
            new_appointment = {
                "appointment_id": get_next_id("appointments.csv"),
                "patient_id": patient_id or '',
                "doctor_id": doctor_id,
                "service_id": service['service_id'],
                "date": data['date'],
                "time": data['time'],
                "status": "Ожидается оплаты" if int(data['discount']) > 0 else "Ожидается",
                "office": doctor['office'],
                "discount": data['discount']
            }

            # Сохранение
            appointments = read_csv("appointments.csv")
            appointments.append(new_appointment)
            write_csv("appointments.csv", appointments)

            # Создание талона
            ticket = f"""
            Талон на прием
            {'='*30}
            Пациент: {patient['surname']} {patient['name']} ({data['phone']}) 
                """ if patient_id else f"""
            Талон на прием
            {'='*30}
            Пациент: Гость
            """
            
            ticket += f"""
            Дата: {data['date']}
            Время: {data['time']}
            Кабинет: {doctor['office']}
            Врач: {doctor['surname']} {doctor['name']}
            Услуга: {service['service_name']}
            Стоимость: {float(service['price'])*(100 - int(data['discount']))/100:.2f} руб.
            """
            
            messagebox.showinfo("Талон", ticket)
            self.destroy()
            self.app.load_registry_appointments()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
