# app/main_menu.py
import tkinter as tk
import random
from tkinter import ttk, messagebox
from config import COLUMN_WIDTHS, FONT_SIZE
from app.database import read_csv, write_csv, get_next_id
from app.admin import AddDoctorWindow, ServicesWindow  # Теперь импорт будет работать
from app.doctor.end_appointment import EndAppointmentWindow
from app.patient.book_appointment import BookAppointmentWindow
from app.patient.payment import PaymentWindow, PaymentSelectionWindow
from app.patient.registry_appointment import RegistryAppointmentWindow


class MainMenu(tk.Toplevel):
    def __init__(self, app, user_role):
        super().__init__()
        self.app = app
        self.user_role = user_role
        self.title(f"Главное меню ({user_role})")
        self.geometry("1600x1000")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        if user_role == "Главный врач":
            self.show_admin_interface(main_frame)
        elif user_role == "Врач":
            self.show_doctor_interface(main_frame)
        elif user_role == "Пациент":
            self.show_patient_interface(main_frame)
        elif user_role == "Регистратура":
            self.show_registry_interface(main_frame)

    def logout(self):
        self.app.current_user = None
        self.app.user_role = None
        self.destroy()
        self.app.show_auth_window()

    # --- ИНТЕРФЕЙС АДМИНИСТРАТОРА ---
    def show_admin_interface(self, parent):
        # Поля поиска
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Фамилия:").pack(side=tk.LEFT, padx=5)
        self.last_name_search = ttk.Entry(search_frame, width=15)
        self.last_name_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Имя:").pack(side=tk.LEFT, padx=5)
        self.first_name_search = ttk.Entry(search_frame, width=15)
        self.first_name_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Телефон:").pack(side=tk.LEFT, padx=5)
        self.phone_search = ttk.Entry(search_frame, width=15)
        self.phone_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Специализация:").pack(side=tk.LEFT, padx=5)
        self.spec_search = ttk.Entry(search_frame, width=15)
        self.spec_search.pack(side=tk.LEFT, padx=5)
        
        # Привязка событий поиска
        for entry in [self.last_name_search, self.first_name_search, 
                    self.phone_search, self.spec_search]:
            entry.bind("<KeyRelease>", self.filter_admin_table)

        # Таблица врачей
        self.tree = ttk.Treeview(parent, columns=("№", "ФИО", "Специализация", "Квалификация", "Телефон"), show="headings")
        self.tree.column("№", width=COLUMN_WIDTHS['№'], anchor=tk.CENTER)
        self.tree.column("ФИО", width=COLUMN_WIDTHS['ФИО'])
        self.tree.column("Специализация", width=COLUMN_WIDTHS['Специализация'])
        self.tree.column("Квалификация", width=COLUMN_WIDTHS['Квалификация'])
        self.tree.column("Телефон", width=COLUMN_WIDTHS['Телефон'])
        
        # Заголовки
        for col in ("№", "ФИО", "Специализация", "Квалификация", "Телефон"):
            self.tree.heading(col, text=col)
        
        # Загрузите данные из CSV
        from app.database import read_csv
        doctors = read_csv("doctors.csv")
        
        # После добавления данных в таблицу
        for doc in doctors:
            self.tree.insert("", "end", values=(
                doc["doctor_id"],
                f"{doc['surname']} {doc['name']} {doc['patronymic']}",
                doc["specialization"],
                doc["qualification"],
                doc["phone"]
            ))
        
        # Добавьте эту строку
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Добавить врача", command=self.open_add_doctor, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Удалить врача", command=self.delete_doctor, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Посмотреть услуги", command=self.open_services_window, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Выход", command=self.logout, width=25).pack(side=tk.LEFT, padx=15)

    def delete_doctor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите врача для удаления")
            return

        # Получите ID выбранного врача
        item_values = self.tree.item(selected[0], 'values')
        doctor_id = item_values[0]

        # Загрузите данные из CSV
        from app.database import read_csv, write_csv
        doctors = read_csv("doctors.csv")

        # Удалите врача
        updated_doctors = [doc for doc in doctors if doc["doctor_id"] != doctor_id]

        # Сохраните изменения
        write_csv("doctors.csv", updated_doctors)

        # Обновите таблицу
        self.tree.delete(selected[0])
        messagebox.showinfo("Успех", "Врач успешно удалён")


    def filter_admin_table(self, event=None):
        from app.database import read_csv
        doctors = read_csv("doctors.csv")

        query_last = self.last_name_search.get().lower()
        query_first = self.first_name_search.get().lower()
        query_phone = self.phone_search.get().lower()
        query_spec = self.spec_search.get().lower()

        self.tree.delete(*self.tree.get_children())
        
        for doc in doctors:
            full_name = f"{doc['surname']} {doc['name']} {doc['patronymic']}".lower()
            last_name = doc["surname"].lower()
            first_name = doc["name"].lower()
            
            if (query_last in last_name and
                query_first in first_name and
                query_phone in doc["phone"].lower() and
                query_spec in doc["specialization"].lower()):
                
                self.tree.insert("", "end", values=(
                    doc["doctor_id"],
                    f"{doc['surname']} {doc['name']} {doc['patronymic']}",
                    doc["specialization"],
                    doc["qualification"],
                    doc["phone"]
                ))

    # --- ИНТЕРФЕЙС ВРАЧА ---
    def show_doctor_interface(self, parent):
        # Поля поиска
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Дата:").pack(side=tk.LEFT, padx=5)
        self.date_search = ttk.Entry(search_frame, width=12)
        self.date_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Время:").pack(side=tk.LEFT, padx=5)
        self.time_search = ttk.Entry(search_frame, width=8)
        self.time_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Диагноз:").pack(side=tk.LEFT, padx=5)
        self.diagnosis_search = ttk.Entry(search_frame, width=20)
        self.diagnosis_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Тип:").pack(side=tk.LEFT, padx=5)
        self.type_search = ttk.Combobox(search_frame, values=["Все", "Первичный", "Вторичный"])
        self.type_search.pack(side=tk.LEFT, padx=5)
        self.type_search.set("Все")
        
        # Привязка событий фильтрации
        for widget in [self.date_search, self.time_search, self.diagnosis_search, self.type_search]:
            widget.bind("<KeyRelease>", self.filter_doctor_appointments)
        self.type_search.bind("<<ComboboxSelected>>", self.filter_doctor_appointments)

        # Таблица
        self.tree = ttk.Treeview(parent, 
            columns=("№", "ID Приема", "Пациент", "Дата", "Время", "Услуга", "Диагноз"), 
            show="headings"
        )
        
        # Настройка колонок
        columns_config = {
            "№": 70,
            "ID Приема": 100,
            "Пациент": 200,
            "Дата": 100,
            "Время": 80,
            "Услуга": 200,
            "Диагноз": 300
        }
        
        for col, width in columns_config.items():
            self.tree.column(col, width=width, anchor=tk.CENTER)
            self.tree.heading(col, text=col)
        
        # Загрузка данных
        self.load_doctor_appointments()
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Привязка двойного клика
        self.tree.bind("<Double-1>", self.show_diagnosis_details)
        
        # Кнопки
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Завершить прием", 
                command=self.open_end_appointment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Выход", 
                command=self.logout, width=25).pack(side=tk.LEFT, padx=15)

    def filter_doctor_appointments(self, event=None):
        query_date = self.date_search.get()
        query_time = self.time_search.get()
        query_diagnosis = self.diagnosis_search.get().lower()
        query_type = self.type_search.get().lower()

        self.tree.delete(*self.tree.get_children())
        appointments = read_csv("appointments.csv")
        for app in appointments:
            if (query_date in app[2] and
                query_time in app[3] and
                query_diagnosis in app[5].lower() and
                query_type in app[4].lower()):
                self.tree.insert("", "end", values=app)
        
    def load_doctor_appointments(self):
        from app.database import read_csv
        
        appointments = read_csv("appointments.csv")
        services = read_csv("services.csv")
        patients = read_csv("patients.csv")
        diagnoses = read_csv("diagnoses.csv")
        
        doctor_id = self.app.current_user['doctor_id']
        
        self.tree.delete(*self.tree.get_children())
        for idx, appt in enumerate(appointments):
            if appt.get('doctor_id') != doctor_id:
                continue
                
            service = next(
                (s for s in services if s['service_id'] == appt['service_id']),
                {'service_name': 'Неизвестно'}
            )
            
            patient = next(
                (p for p in patients if p['patient_id'] == appt['patient_id']),
                {'surname': '', 'name': ''}
            )
            
            diagnosis = next(
                (d for d in diagnoses if d['appointment_id'] == appt['appointment_id']),
                {'diagnosis': 'Не завершен'}
            )
            
            self.tree.insert("", "end", values=(
                idx + 1,
                appt['appointment_id'],
                f"{patient['surname']} {patient['name']}".strip(),
                appt['date'],
                appt['time'],
                service['service_name'],
                diagnosis['diagnosis']
            ))

    def filter_doctor_appointments(self, event=None):
        query_date = self.date_search.get()
        query_time = self.time_search.get()
        query_diagnosis = self.diagnosis_search.get().lower()
        query_type = self.type_search.get()
        
        from app.database import read_csv
        appointments = read_csv("appointments.csv")
        services = read_csv("services.csv")
        patients = read_csv("patients.csv")
        diagnoses = read_csv("diagnoses.csv")
        
        doctor_id = self.app.current_user['doctor_id']
        
        self.tree.delete(*self.tree.get_children())
        for idx, appt in enumerate(appointments):
            if appt.get('doctor_id') != doctor_id:
                continue
                
            service = next(
                (s for s in services if s['service_id'] == appt['service_id']),
                {'service_name': ''}
            )
            
            patient = next(
                (p for p in patients if p['patient_id'] == appt['patient_id']),
                {'surname': '', 'name': ''}
            )
            
            diagnosis = next(
                (d for d in diagnoses if d['appointment_id'] == appt['appointment_id']),
                {'diagnosis': ''}
            )
            
            # Применение фильтров
            date_match = query_date in appt['date'] if query_date else True
            time_match = query_time in appt['time'] if query_time else True
            diagnosis_match = query_diagnosis in diagnosis['diagnosis'].lower()
            type_match = (query_type == "Все" or 
                        (query_type == "Первичный" and diagnosis['diagnosis'] == '') or
                        (query_type == "Вторичный" and diagnosis['diagnosis'] != ''))
            
            if date_match and time_match and diagnosis_match and type_match:
                self.tree.insert("", "end", values=(
                    idx + 1,
                    appt['appointment_id'],
                    f"{patient['surname']} {patient['name']}".strip(),
                    appt['date'],
                    appt['time'],
                    service['service_name'],
                    diagnosis['diagnosis'] or 'Не завершен'
                ))

    def show_diagnosis_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        appt_id = self.tree.item(selected[0], 'values')[1]
        from app.database import read_csv
        diagnoses = read_csv("diagnoses.csv")
        diagnosis = next((d for d in diagnoses if d['appointment_id'] == appt_id), None)
        
        if diagnosis:
            message = f"Диагноз: {diagnosis['diagnosis']}\n\nРекомендации:\n{diagnosis['recommendations']}"
            messagebox.showinfo("Детали приема", message)
        else:
            messagebox.showinfo("Информация", "Прием еще не завершен")


    # --- ИНТЕРФЕЙС ПАЦИЕНТА ---
    def show_patient_interface(self, parent):
        # Заголовок
        ttk.Label(parent, text="Мои записи на прием", font=('Arial', FONT_SIZE+2)).pack(pady=10)
        
        # Фрейм поиска
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        # Поля поиска
        ttk.Label(search_frame, text="Специализация:").pack(side=tk.LEFT, padx=5)
        self.spec_search = ttk.Entry(search_frame, width=20)
        self.spec_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Дата (ДД.ММ.ГГГГ):").pack(side=tk.LEFT, padx=5)
        self.date_search = ttk.Entry(search_frame, width=12)
        self.date_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Статус:").pack(side=tk.LEFT, padx=5)
        self.status_search = ttk.Combobox(search_frame, 
                                        values=["Все", "Ожидается", "Оплачено", "Завершен"],
                                        width=15)
        self.status_search.pack(side=tk.LEFT, padx=5)
        self.status_search.set("Все")
        
        # Привязка событий фильтрации
        for widget in [self.spec_search, self.date_search, self.status_search]:
            widget.bind("<KeyRelease>", self.filter_patient_appointments)
        self.status_search.bind("<<ComboboxSelected>>", self.filter_patient_appointments)
        
        # Таблица
        self.tree = ttk.Treeview(parent, 
                            columns=("№", "Специалист", "Дата", "Время", "Кабинет", "Статус", "Цена", "ID Приема"), 
                            show="headings")
        
        # Настройка колонок
        columns_config = {
            "№": 70,
            "Специалист": 150,
            "Дата": 100,
            "Время": 80,
            "Кабинет": 100,
            "Статус": 120,
            "Цена": 100,
            "ID Приема": 120
        }
        
        for col, width in columns_config.items():
            self.tree.column(col, width=width, anchor=tk.CENTER)
            self.tree.heading(col, text=col)
        
        # Загрузка данных
        self.load_patient_appointments()
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Привязка двойного клика
        self.tree.bind("<Double-1>", self.show_appointment_details)
        
        # Кнопки
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Запись на прием", 
                command=self.open_book_appointment, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отменить прием", 
                command=self.cancel_appointment, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Оплатить прием", 
                command=self.open_payment_selection, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Выход", 
                command=self.logout, width=20).pack(side=tk.LEFT, padx=10)

    def filter_patient_appointments(self, event=None):
        query_spec = self.spec_search.get().lower()
        query_date = self.date_search.get()
        status_filter = self.status_search.get()
        
        from app.database import read_csv
        appointments = read_csv("appointments.csv")
        services = read_csv("services.csv")
        doctors = read_csv("doctors.csv")
        
        patient_id = self.app.current_user['patient_id']
        
        self.tree.delete(*self.tree.get_children())
        for idx, appt in enumerate(appointments):
            if appt['patient_id'] != patient_id:
                continue
                
            service = next((s for s in services if s['service_id'] == appt['service_id']), {})
            doctor = next((d for d in doctors if d['doctor_id'] == appt['doctor_id']), {})
            
            # Применение фильтров
            spec_match = query_spec in doctor.get('specialization', '').lower()
            date_match = query_date in appt['date'] if query_date else True
            status_match = (status_filter == "Все") or (appt['status'] == status_filter)
            
            if spec_match and date_match and status_match:
                self.tree.insert("", "end", values=(
                    idx+1,
                    doctor.get('specialization', 'Неизвестно'),
                    appt['date'],
                    appt['time'],
                    appt['office'],
                    appt['status'],
                    f"{service.get('price', '0')} руб.",
                    appt['appointment_id']
                ))

    def load_patient_appointments(self):
        from app.database import read_csv
        appointments = read_csv("appointments.csv")
        services = read_csv("services.csv")
        doctors = read_csv("doctors.csv")
        
        patient_id = self.app.current_user['patient_id']
        
        self.tree.delete(*self.tree.get_children())
        for idx, appt in enumerate(appointments):
            if appt['patient_id'] != patient_id:
                continue
                
            service = next((s for s in services if s['service_id'] == appt['service_id']), {})
            doctor = next((d for d in doctors if d['doctor_id'] == appt['doctor_id']), {})
            
            self.tree.insert("", "end", values=(
                idx+1,
                doctor.get('specialization', 'Неизвестно'),
                appt['date'],
                appt['time'],
                appt['office'],
                appt['status'],
                f"{service.get('price', '0')} руб.",
                appt['appointment_id']
            ))

    def show_appointment_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        appt_id = self.tree.item(selected[0], 'values')[7]
        from app.database import read_csv
        diagnoses = read_csv("diagnoses.csv")
        diagnosis = next((d for d in diagnoses if d['appointment_id'] == appt_id), None)
        
        if diagnosis:
            message = f"Диагноз: {diagnosis['diagnosis']}\n\nРекомендации:\n{diagnosis['recommendations']}"
            messagebox.showinfo("Детали приема", message)
        else:
            messagebox.showinfo("Информация", "Прием еще не завершен врачом")

    def cancel_appointment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите запись для отмены")
            return
            
        appt_id = self.tree.item(selected[0], 'values')[7]
        
        try:
            from app.database import read_csv, write_csv
            appointments = read_csv("appointments.csv")
            
            # Поиск и проверка записи
            appointment = next((a for a in appointments if a['appointment_id'] == appt_id), None)
            if not appointment:
                messagebox.showerror("Ошибка", "Запись не найдена")
                return
                
            if appointment['status'] != 'Ожидается':
                messagebox.showwarning("Ошибка", "Можно отменять только записи со статусом 'Ожидается'")
                return
                
            # Удаление записи
            updated_appointments = [a for a in appointments if a['appointment_id'] != appt_id]
            write_csv("appointments.csv", updated_appointments)
            
            # Обновление таблицы
            self.load_patient_appointments()
            messagebox.showinfo("Успех", "Запись успешно отменена")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при отмене записи: {str(e)}")

    def open_payment_selection(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите запись для оплаты")
            return
            
        appt_id = self.tree.item(selected[0], 'values')[7]  # ID в последнем столбце
        from app.patient.payment import PaymentSelectionWindow
        PaymentSelectionWindow(self, appt_id, self.update_payment_status)

    def update_payment_status(self, appt_id):
        from app.database import read_csv, write_csv
        appointments = read_csv("appointments.csv")
        
        for appt in appointments:
            if appt['appointment_id'] == appt_id:
                appt['status'] = 'Оплачено'
                break
        
        write_csv("appointments.csv", appointments)
        self.load_patient_appointments()
        messagebox.showinfo("Обновлено", "Статус приема обновлен")


        # --- ИНТЕРФЕЙС Регистратуры ---
    
    def show_registry_interface(self, parent):
        # Фрейм поиска
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        # Поля поиска
        search_labels = ["ID приема:", "Специалист:", "Дата:", "Время:"]
        self.search_entries = {}
        
        for i, text in enumerate(search_labels):
            ttk.Label(search_frame, text=text).grid(row=0, column=i*2, padx=5)
            entry = ttk.Entry(search_frame, width=15)
            if "Специалист" in text:
                entry = ttk.Combobox(search_frame, width=15, values=["Терапевт", "Хирург", "Кардиолог"])
            elif "Время" in text:
                entry = ttk.Combobox(search_frame, width=15, values=["09:00", "10:00", "11:00", "14:00"])
            entry.grid(row=0, column=i*2+1, padx=5)
            self.search_entries[text] = entry

        # Таблица
        self.tree = ttk.Treeview(parent, columns=("ID приема", "Специалист", "Дата", "Время", "Кабинет", "Цена"), show="headings")
        self.tree.heading("ID приема", text="ID приема")
        self.tree.heading("Специалист", text="Специалист")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Время", text="Время")
        self.tree.heading("Кабинет", text="Кабинет")
        self.tree.heading("Цена", text="Цена")
        
        # Настройка ширины колонок
        for col in ("ID приема", "Специалист", "Дата", "Время", "Кабинет", "Цена"):
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

    # Заполнение таблицы тестовыми данными
        self.registry_data = [
            ("REG-1001", "Терапевт", "15.07.2023", "10:00", "101", "1500 руб"),
            ("REG-1002", "Хирург", "15.07.2023", "11:00", "205", "2500 руб"),
            ("REG-1003", "Кардиолог", "16.07.2023", "09:00", "312", "3000 руб"),
            ("REG-1004", "Терапевт", "16.07.2023", "14:00", "102", "1500 руб"),
            ("REG-1005", "Хирург", "17.07.2023", "10:30", "206", "2500 руб"),
            ("REG-1006", "Терапевт", "17.07.2023", "11:30", "103", "1500 руб"),
            ("REG-1007", "Кардиолог", "18.07.2023", "15:00", "313", "3000 руб"),
        ]

        for record in self.registry_data:
            self.tree.insert("", "end", values=record)

        # Добавляем фильтрацию
        for entry in self.search_entries.values():
            if isinstance(entry, (ttk.Entry, ttk.Combobox)):
                entry.bind("<KeyRelease>", self.filter_registry_table)

        # Кнопки
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Запись на прием", 
                command=self.open_registry_appointment).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Оплатить прием", 
                command=self.open_payment).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Выход", 
                command=self.logout).pack(side=tk.LEFT, padx=10)

    def filter_registry_table(self, event=None):
        search_params = {
            "ID приема:": self.search_entries["ID приема:"].get().lower(),
            "Специалист:": self.search_entries["Специалист:"].get().lower(),
            "Дата:": self.search_entries["Дата:"].get().lower(),
            "Время:": self.search_entries["Время:"].get().lower()
        }

        self.tree.delete(*self.tree.get_children())
        
        for record in self.registry_data:
            match = True
            # Проверяем соответствие каждому параметру поиска
            if search_params["ID приема:"] and search_params["ID приема:"] not in record[0].lower():
                match = False
            if search_params["Специалист:"] and search_params["Специалист:"] not in record[1].lower():
                match = False
            if search_params["Дата:"] and search_params["Дата:"] not in record[2].lower():
                match = False
            if search_params["Время:"] and search_params["Время:"] not in record[3].lower():
                match = False
            
            if match:
                self.tree.insert("", "end", values=record)

    def update_payment_status_registry(self, appointment_id):
        # Обновление статуса оплаты в таблице регистратуры
        for child in self.tree.get_children():
            if self.tree.item(child, 'values')[0] == appointment_id:
                values = list(self.tree.item(child, 'values'))
                # Пример: обновление статуса (если есть соответствующий столбец)
                # values[5] = "Оплачено"
                self.tree.item(child, values=values)

    # --- ОБРАБОТЧИКИ КНОПОК ---
    def open_add_doctor(self):
        AddDoctorWindow(self.app)

    def open_services_window(self):
        ServicesWindow(self.app)

    def open_end_appointment(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        appt_id = self.tree.item(selected[0], 'values')[1]
        EndAppointmentWindow(self, appt_id)  # Передаем self (MainMenu), а не self.app
    
    # В классе MainMenu
    def open_book_appointment(self):
        from app.patient.book_appointment import BookAppointmentWindow
        BookAppointmentWindow(self)  # Передаем сам MainMenu вместо app

    def open_registry_appointment(self):
        RegistryAppointmentWindow(self.app)

    def open_payment(self):
        PaymentWindow(self.app, self.update_payment_status_registry)

