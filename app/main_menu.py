# app/main_menu.py
import tkinter as tk
import random
from tkinter import ttk, messagebox
from config import COLUMN_WIDTHS, FONT_SIZE
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
        
        # Тестовые данные
        self.admin_data = []
        for i in range(1, 11):
            self.admin_data.append((
                i,
                f"Иванов Иван Иванович {i}",
                ["Терапевт", "Хирург", "Офтальмолог"][i%3],
                f"Высшая категория {i}",
                f"+7 (999) 123-45-{i:02d}"
            ))
        
        # Добавление данных в таблицу
        for doctor in self.admin_data:
            self.tree.insert("", "end", values=doctor)
        
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
        
        item_values = self.tree.item(selected[0], 'values')
        
        doctor_id = item_values[0]
        self.admin_data = [doc for doc in self.admin_data if doc[0] != doctor_id]
        
        self.tree.delete(selected[0])
        
        self.filter_admin_table()
        
        messagebox.showinfo("Успех", "Врач успешно удалён")


    def filter_admin_table(self, event=None):
        query_last = self.last_name_search.get().lower()
        query_first = self.first_name_search.get().lower()
        query_phone = self.phone_search.get().lower()
        query_spec = self.spec_search.get().lower()

        self.tree.delete(*self.tree.get_children())
        for doctor in self.admin_data:
            parts = doctor[1].split()
            last_name = parts[0].lower() if len(parts) > 0 else ""
            first_name = parts[1].lower() if len(parts) > 1 else ""
            
            if (query_last in last_name and
                query_first in first_name and
                query_phone in str(doctor[3]).lower() and
                query_spec in doctor[2].lower()):
                self.tree.insert("", "end", values=doctor)

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
        self.type_search = ttk.Combobox(search_frame, values=["Первичный", "Вторичный"])
        self.type_search.pack(side=tk.LEFT, padx=5)
        
        # Привязка событий
        for widget in [self.date_search, self.time_search, self.diagnosis_search, self.type_search]:
            widget.bind("<KeyRelease>", self.filter_doctor_appointments)

        # Таблица
        self.tree = ttk.Treeview(parent, columns=("№", "ID Приема", "Дата", "Время", "Тип приема", "Диагноз"), show="headings")
        self.tree.column("№", width=COLUMN_WIDTHS['№'], anchor=tk.CENTER)
        self.tree.column("ID Приема", width=COLUMN_WIDTHS['ID Приема'])
        self.tree.column("Дата", width=COLUMN_WIDTHS['Дата'])
        self.tree.column("Время", width=COLUMN_WIDTHS['Последний визит'])
        self.tree.column("Тип приема", width=COLUMN_WIDTHS['Тип приема'])
        self.tree.column("Диагноз", width=COLUMN_WIDTHS['Диагноз'])
        
        # Заголовки
        for col in ("№", "ID Приема", "Дата", "Время", "Тип приема", "Диагноз"):
            self.tree.heading(col, text=col)
        
        # Тестовые данные
        self.doctor_data = []
        for i in range(1, 6):
            self.doctor_data.append((
                i,
                f"{i + random.randint(1,100)}",
                f"{i%28+1:02d}.07.2023",
                f"10:{i%60:02d}",
                ["Первичный", "Вторичный"][i%2],
                f"ОРВИ {i}"
            ))
        
        # Добавление данных в таблицу
        for app in self.doctor_data:
            self.tree.insert("", "end", values=app)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Завершить прием", command=self.open_end_appointment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Выход", command=self.logout, width=25).pack(side=tk.LEFT, padx=15)

    def filter_doctor_appointments(self, event=None):
        query_date = self.date_search.get()
        query_time = self.time_search.get()
        query_diagnosis = self.diagnosis_search.get().lower()
        query_type = self.type_search.get().lower()

        self.tree.delete(*self.tree.get_children())
        for app in self.doctor_data:
            if (query_date in app[2] and
                query_time in app[3] and
                query_diagnosis in app[5].lower() and
                query_type in app[4].lower()):
                self.tree.insert("", "end", values=app)


    # --- ИНТЕРФЕЙС ПАЦИЕНТА ---
    def show_patient_interface(self, parent):
        # Поля поиска
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Специализация:").pack(side=tk.LEFT, padx=5)
        self.spec_search = ttk.Entry(search_frame, width=15)
        self.spec_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Дата (ДД.ММ.ГГГГ):").pack(side=tk.LEFT, padx=5)
        self.date_search = ttk.Entry(search_frame, width=12)
        self.date_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Статус:").pack(side=tk.LEFT, padx=5)
        self.status_search = ttk.Combobox(search_frame, values=["Ожидает оплаты", "Оплачено", "Ожидается прием"])
        self.status_search.pack(side=tk.LEFT, padx=5)
        
        # Привязка событий
        for widget in [self.spec_search, self.date_search, self.status_search]:
            widget.bind("<KeyRelease>", self.filter_patient_appointments)

        # Таблица
        self.tree = ttk.Treeview(parent, columns=("№", "Специалист", "Дата", "Время", "Кабинет", "Статус", "Цена", "ID Приема"), 
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

        # Тестовые данные
        self.appointments_data = []
        for i in range(1, 11):
            self.appointments_data.append((
                i,
                "Терапевт",
                f"{i+10}.07.2023",
                f"10:{i%60:02d}",
                f"101",
                ["Ожидается прием", "Оплачено", "Ожидает оплаты"][i%3],
                "1500 руб.",
                f"APT-{i}"
            ))

        # Добавление данных в таблицу
        for app in self.appointments_data:
            self.tree.insert("", "end", values=app)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
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
        query_status = self.status_search.get().lower()

        self.tree.delete(*self.tree.get_children())
        for app in self.appointments_data:
            if (query_spec in app[1].lower() and
                (query_date == "" or query_date in app[2]) and
                (query_status == "" or query_status in app[5].lower())):
                self.tree.insert("", "end", values=app)

    def show_appointment_details(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            self.description_text.config(state='normal')
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, item[8])  # 8 индекс - описание
            self.description_text.config(state='disabled')

    def cancel_appointment(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0], 'values')
        if item[5] != "Ожидается прием":
            messagebox.showerror("Ошибка", "Можно отменять только приемы со статусом 'Ожидается прием'")
            return
        
        self.tree.delete(selected[0])

    def open_payment_selection(self):
        selected = self.tree.selection()
        if selected:
            PaymentSelectionWindow(self.app, self.update_payment_status)

    def update_payment_status(self, appointment_id):
        for child in self.tree.get_children():
            if self.tree.item(child, 'values')[7] == appointment_id:
                values = list(self.tree.item(child, 'values'))
                values[5] = "Оплачено"
                self.tree.item(child, values=values)

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
        EndAppointmentWindow(self.app)

    def open_book_appointment(self):
        BookAppointmentWindow(self.app)

    def open_registry_appointment(self):
        RegistryAppointmentWindow(self.app)

    def open_payment(self):
        PaymentWindow(self.app, self.update_payment_status_registry)

    