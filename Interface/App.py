import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import simpledialog

# Конфигурация стилей
FONT_SIZE = 14
TABLE_ROW_HEIGHT = 45
COLUMN_WIDTHS = {
    'ID': 120,
    'ФИО': 400,
    'Специализация': 300,
    'Кабинет': 150,
    'Дата рождения': 200,
    'Последний визит': 200,
    'Название': 400,
    'Цена': 200,
    'Дата': 200,
    'Врач': 300,
    'Услуга': 300,
    'Статус': 150
}

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.current_user = None
        self.user_role = None
        
        # Инициализация стилей
        self.style = ttk.Style()
        self.style.configure('.', font=('Arial', FONT_SIZE))
        self.style.configure('Treeview', rowheight=TABLE_ROW_HEIGHT)
        self.style.configure('TButton', padding=10)
        self.style.map('TButton', 
            foreground=[('active', 'black'), ('!disabled', 'black')],
            background=[('active', '#e1e1e1'), ('!disabled', '#f0f0f0')]
        )
        
        self.show_auth_window()

    def show_auth_window(self):
        AuthWindow(self)

    def show_main_menu(self, user_role):
        self.user_role = user_role
        MainMenu(self, user_role)

class AuthWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Авторизация")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=80, padx=80, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Система управления поликлиникой", 
                 font=('Arial', FONT_SIZE+4)).pack(pady=30)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=30)
        
        ttk.Label(form_frame, text="Номер телефона:").grid(row=0, column=0, padx=15, pady=15, sticky='e')
        self.phone_entry = ttk.Entry(form_frame, width=25)
        self.phone_entry.grid(row=0, column=1, padx=15, pady=15)
        
        ttk.Label(form_frame, text="Пароль:").grid(row=1, column=0, padx=15, pady=15, sticky='e')
        self.password_entry = ttk.Entry(form_frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, padx=15, pady=15)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Войти", command=self.login, width=15).pack(side=tk.LEFT, padx=25)
        ttk.Button(btn_frame, text="Регистрация", command=self.open_registration, width=15).pack(side=tk.LEFT, padx=25)
    
    def login(self):
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        
        if phone and password:
            self.app.current_user = phone
            if phone == "admin" and password == "1234":
                self.app.show_main_menu("Главный врач")
            elif phone == "doctor" and password == "1234":
                self.app.show_main_menu("Врач")
            else:
                self.app.show_main_menu("Пациент")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")
    
    def open_registration(self):
        RegistrationWindow(self.app)

class RegistrationWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Регистрация пациента")
        self.geometry("900x1800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Регистрация нового пациента", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        fields = [
            ("Фамилия", 0),
            ("Имя", 1),
            ("Отчество", 2),
            ("Номер телефона", 3),
            ("Пароль", 4),
            ("Дата рождения", 5),
            ("Адрес", 6)
        ]
        
        self.entries = {}
        for text, row in fields:
            ttk.Label(form_frame, text=text+":").grid(row=row, column=0, padx=15, pady=10, sticky='e')
            entry = ttk.Entry(form_frame, width=35)
            entry.grid(row=row, column=1, padx=15, pady=10)
            self.entries[text] = entry
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Зарегистрироваться", command=self.submit, width=20).pack(side=tk.LEFT, padx=20)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=20).pack(side=tk.LEFT, padx=20)
    
    def submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        if all(data.values()):
            messagebox.showinfo("Успех", "Регистрация завершена!")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")

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

class AddDoctorWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Добавление врача")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Добавление нового врача", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        fields = [
            ("Фамилия", 0),
            ("Имя", 1),
            ("Отчество", 2),
            ("Номер телефона", 3),
            ("Пароль", 4),
            ("Кабинет", 5),
            ("Специализация", 6),
            ("Квалификация", 7)
        ]
        
        self.entries = {}
        for text, row in fields:
            ttk.Label(form_frame, text=text+":").grid(row=row, column=0, padx=15, pady=10, sticky='e')
            entry = ttk.Entry(form_frame, width=35)
            entry.grid(row=row, column=1, padx=15, pady=10)
            self.entries[text] = entry
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.submit, width=20).pack(side=tk.LEFT, padx=20)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=20).pack(side=tk.LEFT, padx=20)
    
    def submit(self):
        data = {field: entry.get() for field, entry in self.entries.items()}
        if all(data.values()):
            messagebox.showinfo("Успех", "Врач успешно добавлен!")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")

class ServicesWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Управление услугами")
        self.geometry("1400x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Список услуг
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Название", "Цена", "Кабинет"), show="headings")
        
        self.tree.column("ID", width=COLUMN_WIDTHS['ID'], anchor=tk.CENTER)
        self.tree.column("Название", width=COLUMN_WIDTHS['Название'])
        self.tree.column("Цена", width=COLUMN_WIDTHS['Цена'], anchor=tk.CENTER)
        self.tree.column("Кабинет", width=COLUMN_WIDTHS['Кабинет'], anchor=tk.CENTER)
        
        for col in ("ID", "Название", "Цена", "Кабинет"):
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Тестовые данные
        for i in range(1, 16):
            self.tree.insert("", "end", values=(
                i,
                f"Медицинская услуга {i}",
                f"{1500 + i*100}",
                f"{200 + i}"
            ))
        
        # Кнопки управления
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Добавить услугу", command=self.open_add_service, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)

    def open_add_service(self):
        AddServiceWindow(self.app)

class AddServiceWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Добавление услуги")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Добавление новой услуги", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        fields = [
            ("Название услуги", 0),
            ("Цена (руб)", 1),
            ("Кабинет", 2),
            ("Описание", 3)
        ]
        
        self.entries = {}
        for text, row in fields[:3]:
            ttk.Label(form_frame, text=text+":").grid(row=row, column=0, padx=15, pady=10, sticky='e')
            entry = ttk.Entry(form_frame, width=35)
            entry.grid(row=row, column=1, padx=15, pady=10)
            self.entries[text] = entry
        
        # Текстовое поле для описания
        ttk.Label(form_frame, text="Описание:").grid(row=3, column=0, padx=15, pady=10, sticky='ne')
        self.description_entry = tk.Text(form_frame, height=8, width=50, font=('Arial', FONT_SIZE))
        self.description_entry.grid(row=3, column=1, padx=15, pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.submit, width=20).pack(side=tk.LEFT, padx=20)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=20).pack(side=tk.LEFT, padx=20)
    
    def submit(self):
        data = {
            'Название услуги': self.entries['Название услуги'].get(),
            'Цена (руб)': self.entries['Цена (руб)'].get(),
            'Кабинет': self.entries['Кабинет'].get(),
            'Описание': self.description_entry.get("1.0", tk.END).strip()
        }
        
        if all(data.values()):
            try:
                float(data['Цена (руб)'])
                messagebox.showinfo("Успех", "Услуга успешно добавлена!")
                self.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат цены")
        else:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")

class EndAppointmentWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Завершение приема")
        self.geometry("1200x1000")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=40, padx=40, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Завершение приема", 
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        ttk.Label(main_frame, text="Диагноз:").pack(pady=10, anchor='w')
        self.diagnosis_entry = tk.Text(main_frame, height=6, width=80, font=('Arial', FONT_SIZE))
        self.diagnosis_entry.pack(pady=10)
        
        ttk.Label(main_frame, text="Рекомендации:").pack(pady=10, anchor='w')
        self.recommendations_entry = tk.Text(main_frame, height=10, width=80, font=('Arial', FONT_SIZE))
        self.recommendations_entry.pack(pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.submit, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)
    
    def submit(self):
        diagnosis = self.diagnosis_entry.get("1.0", tk.END).strip()
        recommendations = self.recommendations_entry.get("1.0", tk.END).strip()
        
        if diagnosis and recommendations:
            messagebox.showinfo("Успех", "Прием успешно завершен!")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

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

if __name__ == "__main__":
    app = MainApplication()
    tk.mainloop()