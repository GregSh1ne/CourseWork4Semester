import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Конфигурация стилей
FONT_SIZE = 14
TABLE_ROW_HEIGHT = 45
COLUMN_WIDTHS = {
    'ID': 120,
    'ФИО': 350,
    'Дата рождения': 200,
    'Последний визит': 200,
    'Дата': 180,
    'Врач': 300,
    'Услуга': 300,
    'Статус': 150,
    'Кабинет': 150,
    'Специализация': 250
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
        self.geometry("1280x720")
        
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
            if phone == "admin" and password == "12345":
                self.app.show_main_menu("Главный врач")
            elif phone == "doctor" and password == "12345":
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
        self.geometry("1000x800")
        
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
        self.geometry("1200x900")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Добро пожаловать, {user_role}!",
                 font=('Arial', FONT_SIZE+2)).pack(pady=20)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        if user_role == "Главный врач":
            ttk.Button(btn_frame, text="Добавить врача", command=self.open_add_doctor, width=25).pack(pady=15)
            ttk.Button(btn_frame, text="Добавить услугу", command=self.open_add_service, width=25).pack(pady=15)
        elif user_role == "Врач":
            ttk.Button(btn_frame, text="Список пациентов", command=self.open_patient_list, width=25).pack(pady=15)
            ttk.Button(btn_frame, text="Завершить прием", command=self.open_end_appointment, width=25).pack(pady=15)
        elif user_role == "Пациент":
            ttk.Button(btn_frame, text="История приемов", command=self.open_appointment_history, width=25).pack(pady=15)
            ttk.Button(btn_frame, text="Записаться на прием", command=self.open_book_appointment, width=25).pack(pady=15)
            ttk.Button(btn_frame, text="Оплатить услуги", command=self.open_payment, width=25).pack(pady=15)
        
        ttk.Button(btn_frame, text="Выход", command=self.logout, width=25).pack(pady=30)
    
    def logout(self):
        self.app.current_user = None
        self.app.user_role = None
        self.destroy()
        self.app.show_auth_window()
    
    def open_add_doctor(self):
        AddDoctorWindow(self.app)
    
    def open_add_service(self):
        AddServiceWindow(self.app)
    
    def open_patient_list(self):
        PatientListWindow(self.app)
    
    def open_end_appointment(self):
        EndAppointmentWindow(self.app)
    
    def open_appointment_history(self):
        AppointmentHistoryWindow(self.app)
    
    def open_book_appointment(self):
        BookAppointmentWindow(self.app)
    
    def open_payment(self):
        PaymentWindow(self.app)

class AddDoctorWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Добавление врача")
        self.geometry("1000x800")
        
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

class PatientListWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Список пациентов")
        self.geometry("1600x1000")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(main_frame, columns=("ID", "ФИО", "Дата рождения", "Последний визит"), show="headings")
        
        # Настройка столбцов
        self.tree.column("ID", width=COLUMN_WIDTHS['ID'], anchor=tk.CENTER)
        self.tree.column("ФИО", width=COLUMN_WIDTHS['ФИО'])
        self.tree.column("Дата рождения", width=COLUMN_WIDTHS['Дата рождения'])
        self.tree.column("Последний визит", width=COLUMN_WIDTHS['Последний визит'])
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Дата рождения", text="Дата рождения")
        self.tree.heading("Последний визит", text="Последний визит")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Заполнение данными
        for i in range(1, 31):
            self.tree.insert("", "end", values=(
                i,
                f"Иванова Мария Петровна {i}",
                f"{i%28+1:02d}.{i%12+1:02d}.{1980+i%20}",
                f"{i%28+1:02d}.06.2023"
            ))
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Завершить прием", command=self.open_end_appointment, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)
    
    def open_end_appointment(self):
        if self.tree.selection():
            EndAppointmentWindow(self.app)
        else:
            messagebox.showwarning("Внимание", "Выберите пациента")

class EndAppointmentWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Завершение приема")
        self.geometry("1200x900")
        
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

if __name__ == "__main__":
    app = MainApplication()
    tk.mainloop()