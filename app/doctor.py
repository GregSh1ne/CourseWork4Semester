import tkinter as tk
from tkinter import ttk, messagebox
from config import COLUMN_WIDTHS, FONT_SIZE


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
