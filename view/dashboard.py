from view.home_page import HomePage
from view.manager_page import ManagerPage

import tkinter as tk

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản lý sinh viên")
        self.root.geometry("1200x760+150+20")
        self.root.configure(bg="#1c1c1c")

        # Tạo khung sidebar
        self.create_sidebar()

        # Tạo khung nội dung chính
        self.content_frame = tk.Frame(self.root, bg="#2c2c2c")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.home_page()
        self.root.mainloop()

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#2c2c2c", width=200)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Quản lý sinh viên", bg="#2c2c2c", fg="white", font=("Arial", 16)).pack(pady=20)

        nav_items = {"Trang chủ": self.home_page, "Quản lý học vụ": self.manager_page}
        for item, command in nav_items.items():
            tk.Button(sidebar, text=item, bg="#2c2c2c", fg="white", font=("Arial", 12), width=30, height=2, command=command).pack(fill="x", pady=5)

    def home_page(self):
        HomePage(self.content_frame)

    def manager_page(self):
        ManagerPage(self.content_frame)