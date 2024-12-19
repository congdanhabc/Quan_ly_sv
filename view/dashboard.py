from view.home_page import HomePage
from view.manager_page import ManagerPage
from PIL import Image, ImageTk
import tkinter as tk

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản lý sinh viên")
        self.root.geometry("1200x760+150+20")
        # Khởi tạo theme
        self.is_dark_theme = True
        self.theme_colors = {
            "dark": {
                "bg": "#1c1c1c",
                "fg": "white",
                "button_bg": "#2c2c2c",
                "top_bar_bg": "#2c2c2c",
                "sidebar_bg": "#2c2c2c"
            },
            "light": {
                "bg": "white",
                "fg": "black", 
                "button_bg": "#e0e0e0",
                "top_bar_bg": "#f0f0f0",
                "sidebar_bg": "#f0f0f0"
            }
        }
        
        # Áp dụng theme ban đầu
        self.apply_theme()

        # Tạo khung sidebar
        self.create_sidebar()

        # Tạo khung nội dung chính
        self.content_frame = tk.Frame(self.root, bg=self.get_current_theme()["bg"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Tạo settings frame
        self.create_settings()

        self.home_page()
        self.root.mainloop()

    def create_sidebar(self):
        colors = self.get_current_theme()
        self.sidebar = tk.Frame(self.root, bg=colors["sidebar_bg"], width=200)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar, 
            text="Quản lý sinh viên", 
            bg=colors["sidebar_bg"], 
            fg=colors["fg"], 
            font=("Arial", 16)
        ).pack(pady=20)

        nav_items = {"Trang chủ": self.home_page, "Quản lý học vụ": self.manager_page}
        for item, command in nav_items.items():
            tk.Button(
                self.sidebar, 
                text=item, 
                bg=colors["button_bg"], 
                fg=colors["fg"], 
                font=("Arial", 12), 
                width=30, 
                height=2, 
                command=command
            ).pack(fill="x", pady=5)


    def create_settings(self):
        colors = self.get_current_theme()
        settings_frame = tk.Frame(self.sidebar, bg=colors["sidebar_bg"])
        settings_frame.pack(side="bottom", pady=20)

        # Tải và chuẩn bị icon settings
        settings_icon = Image.open("assets/settings.png")
        settings_icon = settings_icon.resize((30, 30), Image.LANCZOS)
        self.settings_icon = ImageTk.PhotoImage(settings_icon)

        self.settings_button = tk.Button(
            settings_frame,
            image=self.settings_icon,
            bg=colors["sidebar_bg"],
            bd=0,
            command=self.show_settings_menu
        )
        self.settings_button.pack(side="left", padx=10)

        # Tải và chuẩn bị icon micro
        micro_icon = Image.open("assets/mic.png")
        micro_icon = micro_icon.resize((30, 30), Image.LANCZOS)
        self.micro_icon = ImageTk.PhotoImage(micro_icon)

        self.micro_button = tk.Button(
            settings_frame,
            image=self.micro_icon,
            bg=colors["sidebar_bg"],
            bd=0,
            command=self.open_chatbot
        )
        self.micro_button.pack(side="left", padx=10)

    def show_settings_menu(self):
        settings_menu = tk.Menu(self.root, tearoff=0)
        current_theme = "Sáng" if self.is_dark_theme else "Tối"
        settings_menu.add_command(
            label=f"Đổi sang theme {current_theme}",
            command=self.toggle_theme
        )
        
        # Hiển thị menu tại vị trí chuột
        settings_menu.post(
            self.settings_button.winfo_rootx(),
            self.settings_button.winfo_rooty()
        )

    def get_current_theme(self):
        return self.theme_colors["dark" if self.is_dark_theme else "light"]

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        # Cập nhật lại giao diện
        self.refresh_interface()

    def apply_theme(self):
        colors = self.get_current_theme()
        self.root.configure(bg=colors["bg"])

    def refresh_interface(self):
        # Xóa và tạo lại toàn bộ giao diện
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tạo lại sidebar và nội dung chính
        self.create_sidebar()
        self.content_frame = tk.Frame(self.root, bg=self.get_current_theme()["bg"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Tạo lại settings
        self.create_settings()

        # Hiển thị lại trang chính hoặc giao diện hiện tại
        self.home_page()

    def open_chatbot(self):
        # Tạo cửa sổ mới cho chatbot
        chatbot_window = tk.Toplevel(self.root)
        chatbot_window.title("Chatbot")
        chatbot_window.geometry("400x200+500+300")
        chatbot_window.configure(bg=self.get_current_theme()["bg"])

        tk.Label(
            chatbot_window,
            text="Xin chào, tôi là Chatbot, bạn cần tôi giúp gì?",
            bg=self.get_current_theme()["bg"],
            fg=self.get_current_theme()["fg"],
            font=("Arial", 14),
            wraplength=380
        ).pack(expand=True, padx=20, pady=20)

        tk.Button(
            chatbot_window,
            text="Đóng",
            bg=self.get_current_theme()["button_bg"],
            fg=self.get_current_theme()["fg"],
            command=chatbot_window.destroy
        ).pack(pady=10)

    def home_page(self):
        HomePage(self.content_frame, self.theme_colors, self.is_dark_theme)

    def manager_page(self):
        ManagerPage(self.content_frame)