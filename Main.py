import tkinter as tk
from app.auth import AuthWindow
from app.main_menu import MainMenu
from config import FONT_SIZE, COLUMN_WIDTHS, TABLE_ROW_HEIGHT

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.current_user = None
        self.user_role = None
        
        # Инициализация стилей
        self.style = tk.ttk.Style()
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

if __name__ == "__main__":
    app = MainApplication()
    tk.mainloop()  # Запуск основного цикла обработки событий