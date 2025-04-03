import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .admin import AddDoctorWindow, ServicesWindow
from .doctor import EndAppointmentWindow
from .patient import BookAppointmentWindow, PaymentWindow
from config import COLUMN_WIDTHS

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
    
    def logout(self):
        self.app.current_user = None
        self.app.user_role = None
        self.destroy()
        self.app.show_auth_window()  # Показываем окно авторизации
    
    def show_admin_interface(self, parent):
        # Добавляем поле поиска
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_admin_table)

        # Список врачей
        self.tree = ttk.Treeview(parent, columns=("ID", "ФИО", "Специализация", "Кабинет"), show="headings")
        
        self.tree.column("ID", width=COLUMN_WIDTHS['ID'], anchor=tk.CENTER)
        self.tree.column("ФИО", width=COLUMN_WIDTHS['ФИО'])
        self.tree.column("Специализация", width=COLUMN_WIDTHS['Специализация'])
        self.tree.column("Кабинет", width=COLUMN_WIDTHS['Кабинет'], anchor=tk.CENTER)
        
        for col in ("ID", "ФИО", "Специализация", "Кабинет"):
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Сохраняем исходные данные
        self.admin_data = []
        for i in range(1, 11):
            self.admin_data.append((
                i,
                f"Иванов Иван Иванович {i}",
                ["Терапевт", "Хирург", "Офтальмолог"][i%3],
                f"{100 + i}"
            ))
        
        # Кнопки управления
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Добавить врача", command=self.open_add_doctor, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Посмотреть услуги", command=self.open_services_window, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Выход", command=self.logout, width=25).pack(side=tk.LEFT, padx=15)
    
    def filter_admin_table(self, event):
        query = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())
        for item in self.admin_data:
            if any(query in str(field).lower() for field in item):
                self.tree.insert("", "end", values=item)

    def show_doctor_interface(self, parent):
        # Поиск
        search_frame = ttk.Frame(parent)
        search_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_doctor_table)
        
        # Список пациентов
        self.tree = ttk.Treeview(parent, columns=("ID", "ФИО", "Дата рождения", "Последний визит"), show="headings")
        
        self.tree.column("ID", width=COLUMN_WIDTHS['ID'], anchor=tk.CENTER)
        self.tree.column("ФИО", width=COLUMN_WIDTHS['ФИО'])
        self.tree.column("Дата рождения", width=COLUMN_WIDTHS['Дата рождения'])
        self.tree.column("Последний визит", width=COLUMN_WIDTHS['Последний визит'])
        
        for col in ("ID", "ФИО", "Дата рождения", "Последний визит"):
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Тестовые данные
        for i in range(1, 16):
            self.tree.insert("", "end", values=(
                i,
                f"Петрова Мария Ивановна {i}",
                f"{i%28+1:02d}.{i%12+1:02d}.{1985+i%20}",
                f"{i%28+1:02d}.07.2023"
            ))
        
        # Кнопки управления
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Завершить прием", command=self.open_end_appointment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Выход", command=self.logout, width=25).pack(side=tk.LEFT, padx=15)
    
    def show_patient_interface(self, parent):
        # Список приемов пациента
        self.tree = ttk.Treeview(parent, columns=("ID", "Дата", "Врач", "Услуга", "Статус"), show="headings")
        
        self.tree.column("ID", width=COLUMN_WIDTHS['ID'], anchor=tk.CENTER)
        self.tree.column("Дата", width=COLUMN_WIDTHS['Дата'])
        self.tree.column("Врач", width=COLUMN_WIDTHS['Врач'])
        self.tree.column("Услуга", width=COLUMN_WIDTHS['Услуга'])
        self.tree.column("Статус", width=COLUMN_WIDTHS['Статус'])
        
        for col in ("ID", "Дата", "Врач", "Услуга", "Статус"):
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Тестовые данные
        statuses = ["Ожидает оплаты", "Оплачено", "Завершен"]
        for i in range(1, 11):
            self.tree.insert("", "end", values=(
                i,
                f"{i%28+1:02d}.07.2023 10:{i%60:02d}",
                f"Сидоров П.П. ({['Терапевт', 'Хирург'][i%2]})",
                f"Консультация {i}",
                statuses[i%3]
            ))
        
        # Кнопки управления
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Записаться на прием", command=self.open_book_appointment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Оплатить", command=self.open_payment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Выход", command=self.logout, width=25).pack(side=tk.LEFT, padx=15)
    
    def open_add_doctor(self):
        AddDoctorWindow(self.app)
    
    def open_services_window(self):
        ServicesWindow(self.app)
    
    def open_end_appointment(self):
        EndAppointmentWindow(self.app)
    
    def open_book_appointment(self):
        BookAppointmentWindow(self.app)
    
    def open_payment(self):
        PaymentWindow(self.app)
