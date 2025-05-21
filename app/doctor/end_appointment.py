# app/doctor/end_appointment.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.database import read_csv, write_csv, get_next_id
from config import COLUMN_WIDTHS, FONT_SIZE

class EndAppointmentWindow(tk.Toplevel):
    def __init__(self, main_menu, appointment_id):  # Правильные параметры
        super().__init__()
        self.main_menu = main_menu  # Сохраняем ссылку на MainMenu
        self.appointment_id = appointment_id
        self.title("Завершение приема")
        self.geometry("600x400")
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Диагноз
        ttk.Label(main_frame, text="Диагноз:").grid(row=0, column=0, sticky='w', pady=5)
        self.diagnosis_entry = ttk.Entry(main_frame, width=40)
        self.diagnosis_entry.grid(row=0, column=1, sticky='ew', pady=5)
        
        # Рекомендации
        ttk.Label(main_frame, text="Рекомендации:").grid(row=1, column=0, sticky='nw', pady=5)
        self.recommendations_entry = tk.Text(main_frame, width=40, height=10)
        self.recommendations_entry.grid(row=1, column=1, sticky='ew', pady=5)
        
        # Фрейм для кнопок
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=self.submit).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Назад", command=self.destroy).pack(side=tk.LEFT, padx=10)  # Новая кнопка


    def submit(self):
        diagnosis = self.diagnosis_entry.get().strip()
        recommendations = self.recommendations_entry.get("1.0", tk.END).strip()
        
        if not diagnosis:
            messagebox.showerror("Ошибка", "Введите диагноз")
            return
        if not recommendations:
            messagebox.showerror("Ошибка", "Введите описание (рекомендации)")
            return
        
         # Проверка: если диагноз уже есть для этого приема — редактирование запрещено
        diagnoses = read_csv("diagnoses.csv")
        if any(d['appointment_id'] == self.appointment_id for d in diagnoses):
            messagebox.showerror("Ошибка", "Диагноз для этого приема уже существует и не может быть изменен.")
            self.destroy()
            return

        try:
            # Создаем новую запись диагноза
            new_diagnosis = {
                "diagnosis_id": get_next_id("diagnoses.csv"),
                "appointment_id": self.appointment_id,
                "diagnosis": diagnosis,
                "recommendations": recommendations
            }
            
            # Добавляем в CSV
            diagnoses.append(new_diagnosis)
            write_csv("diagnoses.csv", diagnoses)
            
            messagebox.showinfo("Успех", "Прием успешно завершен")
            self.destroy()
            self.main_menu.load_doctor_appointments()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")
