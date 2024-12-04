import tkinter as tk
from tkinter import messagebox

from controller.user import UserController
from view.dashboard import Dashboard

class UserApp:
    def __init__(self):
        self.user_controller = UserController()
        self.root = tk.Tk()
        self.root.title("Login and Register")
        self.root.geometry("400x300+100+100")
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.login_form()
        self.root.mainloop()

    def login_form(self):
        self.register_frame.pack_forget()       
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Đăng nhập", font=('Arial', 14)).grid(row=0, column=1)

        tk.Label(self.login_frame, text="Username: ").grid(row=1, column=0, padx=5, pady=5)
        self.login_username = tk.Entry(self.login_frame, width = 30)
        self.login_username.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Password: ").grid(row=2, column=0, padx=5, pady=5)
        self.login_password = tk.Entry(self.login_frame, show='*', width = 30)
        self.login_password.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Đăng nhập", command=self.login).grid(row=3, column=0, pady=10)
        # Bắt sự kiện phím Enter
        self.root.bind('<Return>', lambda event: self.login())

        tk.Button(self.login_frame, text="Đăng ký", command=self.register_form).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if not username or not password:
            messagebox.showerror("Đăng nhập thất bại", "Nhập đầy đủ thông tin.")
            return
        
        user = self.user_controller.login(username, password)
        if user:
            messagebox.showinfo("Đăng nhập thành công", f"Xin chào {user['name']}!")
            self.root.destroy()
            dashboard = Dashboard()
        else:
            messagebox.showerror("Đăng nhập thất bại", "Sai Username hoặc Password")

    def register_form(self):
        self.login_frame.pack_forget()        
        self.register_frame.pack(pady=10)

        tk.Label(self.register_frame, text="Đăng ký", font=('Arial', 14)).grid(row=0, column=1)

        tk.Label(self.register_frame, text="Họ tên: ").grid(row=1, column=0, padx=5, pady=5)
        self.register_name = tk.Entry(self.register_frame, width = 30)
        self.register_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Username: ").grid(row=2, column=0, padx=5, pady=5)
        self.register_username = tk.Entry(self.register_frame, width = 30)
        self.register_username.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Password: ").grid(row=3, column=0, padx=5, pady=5)
        self.register_password = tk.Entry(self.register_frame, show='*', width = 30)
        self.register_password.grid(row=3, column=1, padx=5, pady=5)

        confirm_button = tk.Button(self.register_frame, text="Xác nhận", command=self.register).grid(row=4, column=0, pady=10)
        # Bắt sự kiện phím Enter
        self.root.bind('<Return>', lambda event: self.register())

        tk.Button(self.register_frame, text="Quay về đăng nhập", command=self.login_form).grid(row=4, column=1, pady=10)

    def register(self):
        name = self.register_name.get()
        username = self.register_username.get()
        password = self.register_password.get()
        if not name or not username or not password:
            messagebox.showerror("Đăng nhập thất bại", "Nhập đầy đủ thông tin.")
            return

        result = self.user_controller.register_user(name, username, password)
        if result:
            messagebox.showinfo("Register Success", "Đăng ký thành công")
            self.login_form()
        else:
            messagebox.showerror("Register Failed", "Username đã tồn tại")


