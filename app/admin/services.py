# app/admin/services.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import COLUMN_WIDTHS, FONT_SIZE
from .add_doctor import AddDoctorWindow  # если требуется


class ServicesWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Управление услугами")
        self.geometry("1400x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Список услуг
        self.tree = ttk.Treeview(
            main_frame, 
            columns=("ID", "Название", "Цена", "Кабинет"), 
            show="headings"
        )
        
        # Настройка столбцов
        self.tree.column("ID", width=COLUMN_WIDTHS['ID'], anchor=tk.CENTER)
        self.tree.column("Название", width=COLUMN_WIDTHS['Название'])
        self.tree.column("Цена", width=COLUMN_WIDTHS['Цена'], anchor=tk.CENTER)
        self.tree.column("Кабинет", width=COLUMN_WIDTHS['Кабинет'], anchor=tk.CENTER)
        
        # Заголовки
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Цена", text="Цена (руб)")
        self.tree.heading("Кабинет", text="Кабинет")
        
        # Тестовые данные
        for i in range(1, 16):
            self.tree.insert(
                "", 
                "end", 
                values=(
                    i,
                    f"Медицинская услуга {i}",
                    f"{1500 + i*100}",
                    f"{200 + i}"
                )
            )
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Поля поиска
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(search_frame, text="Название:").pack(side=tk.LEFT, padx=5)
        self.name_search = ttk.Entry(search_frame, width=20)
        self.name_search.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Мин. цена:").pack(side=tk.LEFT, padx=5)
        self.min_price = ttk.Entry(search_frame, width=10)
        self.min_price.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Макс. цена:").pack(side=tk.LEFT, padx=5)
        self.max_price = ttk.Entry(search_frame, width=10)
        self.max_price.pack(side=tk.LEFT, padx=5)
        
        # Привязка событий
        for entry in [self.name_search, self.min_price, self.max_price]:
            entry.bind("<KeyRelease>", self.filter_services)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Добавить услугу", command=self.open_add_service, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Удалить услугу", command=self.delete_service, width=25).pack(side=tk.LEFT, padx=15)
        ttk.Button(btn_frame, text="Назад", command=self.destroy, width=25).pack(side=tk.LEFT, padx=15)

    def delete_service(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        # Удаление из данных
        item_id = self.tree.item(selected[0], 'values')[0]
        for child in self.tree.get_children():
            if self.tree.item(child, 'values')[0] == item_id:
                self.tree.delete(child)
                break

    def filter_services(self, event=None):
        query_name = self.name_search.get().lower()
        min_p = self.min_price.get()
        max_p = self.max_price.get()

        self.tree.delete(*self.tree.get_children())
        for i in range(1, 16):
            price = 1500 + i * 100
            if (query_name in f"Медицинская услуга {i}".lower() and
                (min_p == "" or price >= float(min_p or 0)) and
                (max_p == "" or price <= float(max_p or float('inf')))):
                self.tree.insert("", "end", values=(
                    i,
                    f"Медицинская услуга {i}",
                    f"{price}",
                    f"{200 + i}"
                ))

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
