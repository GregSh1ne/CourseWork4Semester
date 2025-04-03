import tkinter as tk
from tkinter import ttk, messagebox
from config import COLUMN_WIDTHS, FONT_SIZE

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
