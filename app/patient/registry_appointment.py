# app/patient/registry_appointment.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import FONT_SIZE

class RegistryAppointmentWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Запись на прием")
        self.geometry("1200x800")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)
        
        # Поля ввода
        fields = [
            ("Дата:", "entry_date"),
            ("Время:", "combo_time"),
            ("Скидка (%):", "combo_discount"),
            ("Специалист:", "combo_specialist")
        ]
        
        self.entries = {}
        for i, (label, name) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if "combo" in name:
                entry = ttk.Combobox(main_frame)
                if "specialist" in name:
                    entry['values'] = ["Терапевт", "Хирург", "Кардиолог"]
                elif "time" in name:
                    entry['values'] = ["09:00", "10:00", "11:00", "14:00"]
                elif "discount" in name:
                    entry['values'] = ["0", "5", "10", "15"]
            else:
                entry = ttk.Entry(main_frame)
            
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            self.entries[name] = entry

        # Блок с выбором аккаунта
        ttk.Label(main_frame, text="У пациента есть аккаунт?").grid(row=4, column=0, columnspan=2, pady=10)
        
        self.account_var = tk.StringVar()
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Radiobutton(btn_frame, text="Да", variable=self.account_var, 
                       value="yes", command=self.toggle_phone_input).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(btn_frame, text="Нет", variable=self.account_var, 
                       value="no", command=self.toggle_phone_input).pack(side=tk.LEFT, padx=10)
        
        # Поле для телефона
        self.phone_frame = ttk.Frame(main_frame)
        ttk.Label(self.phone_frame, text="Телефон:").pack(side=tk.LEFT, padx=5)
        self.phone_entry = ttk.Entry(self.phone_frame)
        self.phone_entry.pack(side=tk.LEFT, expand=True)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Выход", 
                  command=self.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Запись", 
                  command=self.create_record).pack(side=tk.LEFT, padx=10)

    def toggle_phone_input(self):
        if self.account_var.get() == "yes":
            self.phone_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        else:
            self.phone_frame.grid_forget()

    def create_record(self):
        # Проверка заполнения обязательных полей
        required_fields = [
            self.entries['entry_date'].get(),
            self.entries['combo_time'].get(),
            self.entries['combo_specialist'].get()
        ]
        
        if not all(required_fields):
            messagebox.showerror("Ошибка", "Заполните все обязательные поля!")
            return
            
        # Логика сохранения данных
        messagebox.showinfo("Успех", "Запись успешно создана!")
        self.destroy()
