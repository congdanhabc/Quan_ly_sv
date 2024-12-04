from controller.schedule import ScheduleController
from controller.send_mail import send_absent_warning, send_excel_report

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class ManagerPage:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.schedule_controller = ScheduleController()
        self.absent_list = self.schedule_controller.get_absent_list()

        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.home_frame = tk.Frame(self.content_frame, bg="#1c1c1c")
        self.home_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.show_manager_page()

    def show_manager_page(self):
        # Tạo khung top bar trong khung nội dung
        top_bar = tk.Frame(self.home_frame, bg="#2c2c2c", height=50)
        top_bar.pack(side="top", fill="x")

        # Thêm tiêu đề vào top bar
        tk.Label(top_bar, text="Quản lý học vụ", bg="#2c2c2c", fg="white", font=("Arial", 14)).pack(side="left", padx=10)

        # Tạo khung cho các chức năng
        self.function_frame = tk.Frame(self.home_frame, bg="#1c1c1c")
        self.function_frame.pack(pady=20)

        # Thêm các nút gửi mail       
        tk.Button(self.function_frame, text="Gửi mail cảnh báo", bg="#2c2c2c", fg="white", font=("Arial", 12), width=20, command=lambda: self.send_absent_warning()).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.function_frame, text="Gửi excel tổng hợp", bg="#2c2c2c", fg="white", font=("Arial", 12), width=20, command=lambda: self.send_excel()).grid(row=1, column=2, padx=10, pady=5)

        # Khu vực hiển thị kết quả với Treeview
        result_frame = tk.Frame(self.home_frame, bg="#1c1c1c")
        result_frame.pack(fill="both", expand=True)

        # Tạo Treeview để hiển thị kết quả
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("MaSinhVien", "TenSinhVien", "TenMonHoc", "SoBuoi", "ThoiLuong")
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", style="Treeview")

        self.result_tree.heading("MaSinhVien", text="Mã sinh viên")
        self.result_tree.heading("TenSinhVien", text="Tên sinh viên")
        self.result_tree.heading("TenMonHoc", text="Tên môn học")
        self.result_tree.heading("SoBuoi", text="Số buổi vắng")
        self.result_tree.heading("ThoiLuong", text="Thời lượng vắng")

        # Đặt chiều rộng cột và tô màu nền khác nhau
        self.result_tree.column("MaSinhVien", width=100, anchor="center")
        self.result_tree.column("TenSinhVien", width=150, anchor="center")
        self.result_tree.column("TenMonHoc", width=150, anchor="center")
        self.result_tree.column("SoBuoi", width=60, anchor="center")
        self.result_tree.column("ThoiLuong", width=70, anchor="center")

        self.result_tree.tag_configure('evenrow', background='white')
        self.result_tree.tag_configure('oddrow', background='#e6e6e6')

        self.result_tree.pack(fill="both", expand=True, padx=10, pady=10) 

        for index, absent in enumerate(self.absent_list):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            values = (absent["MaSinhVien"], absent["TenSinhVien"], absent["TenMonHoc"], absent["SoBuoi"], absent["ThoiLuong"])
            self.result_tree.insert("", "end", values=values, tags=tag)       
        
    def send_absent_warning(self):
        try:
            students_missing_email = send_absent_warning(self.absent_list)
            if students_missing_email: 
                dialog = tk.Toplevel(self.content_frame) 
                dialog.title("Danh sách sinh viên thiếu email") 
                dialog.geometry("300x200") 
                tk.Label(dialog, text="Danh sách sinh viên thiếu email:").pack(padx=10, pady=10) 
                listbox = tk.Listbox(dialog) 
                listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5) 
                for student in students_missing_email: 
                    listbox.insert(tk.END, student) 
                tk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=10)
            tk.messagebox.showinfo("Thành công", "Gửi Email cảnh báo thành công")
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi gửi Email:\n{e}")

    def send_excel(self):
        try:
            send_excel_report(self.absent_list)
            tk.messagebox.showinfo("Thành công", "Gửi file Excel thành công")
        except Exception as e:
            print(e)
            tk.messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi gửi file Excel:\n{e}")

