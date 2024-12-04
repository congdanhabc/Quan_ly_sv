from controller.student import StudentController
from controller.student_class import Student_ClassController
from controller.schedule import ScheduleController

import tkinter as tk      
from tkinter import ttk 
from tkcalendar import  DateEntry
from datetime import datetime

class ProfilePage:
    def __init__(self, content_frame, ma_sinh_vien):
        self.content_frame = content_frame
        self.ma_sinh_vien = ma_sinh_vien

        self.student_controller = StudentController()
        self.student_class_controller = Student_ClassController()

        # Hủy bỏ frame hiện tại
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.profile_frame = tk.Frame(self.content_frame, bg="#1c1c1c")
        self.profile_frame.pack(fill="both", expand=True, padx=10, pady=10, anchor="center", side="top")
        self.view_profile()
        self.class_view()
        self.schedule_view()
        self.show_class_view()

    def view_profile(self):
        self.profile = self.student_controller.get_student_profile(self.ma_sinh_vien)

        # Tạo khung top bar trong khung nội dung
        top_bar = tk.Frame(self.profile_frame, bg="#2c2c2c", height=50)
        top_bar.pack(side="top", fill="x")

        # Thêm tiêu đề vào top bar
        tk.Label(top_bar, text="Chi tiết thông tin sinh viên", bg="#2c2c2c", fg="white", font=("Arial", 14)).pack(side="left", padx=10)

        # Thêm tiêu đề cho khung thông tin sinh viên
        tk.Label(self.profile_frame, text="Thông tin sinh viên", bg="#1c1c1c", fg="white", font=("Arial", 16)).pack(pady=10)

        # Hiển thị thông tin chi tiết của sinh viên dưới dạng các mục nhập chỉ đọc
        self.infor_frame = tk.Frame(self.profile_frame, bg="#1c1c1c")
        self.infor_frame.pack(fill="both")
        self.infor_view()

        # Thêm nút
        self.infor_bt_frame = tk.Frame(self.profile_frame, bg="#1c1c1c")
        self.infor_bt_frame.pack(side="top", pady=20)

        self.edit_button = tk.Button(self.infor_bt_frame, text="Chỉnh sửa", command=lambda: self.enable_edit_all(), bg="#2c2c2c", fg="white", font=("Arial", 12), width=15)
        self.edit_button.pack(side="left", padx=5)
        self.confirm_button = tk.Button(self.infor_bt_frame, text="Xác nhận", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, command=lambda: self.confirm_edit())
        self.cancel_button = tk.Button(self.infor_bt_frame, text="Hủy", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, command=lambda: self.cancel_edit())

        self.class_bt_frame = tk.Frame(self.profile_frame, bg="#1c1c1c")
        self.class_bt_frame.pack(side="top", pady=10)
        self.class_button = tk.Button(self.class_bt_frame, text="Lớp học phần", command=lambda: self.show_class_view())
        self.class_button.pack(side="left", padx=5)
        self.schedule_button = tk.Button(self.class_bt_frame, text="Chuyên cần", command=lambda: self.show_schedule_view())
        self.schedule_button.pack(side="left", padx=5)

    def infor_view(self):
        for widget in self.infor_frame.winfo_children():
            widget.destroy()
        self.details = [
            ("Mã sinh viên", self.profile.get('MaSinhVien')),
            ("Họ tên", self.profile.get('HoTen')),
            ("Giới tính", self.profile.get('GioiTinh')),
            ("Ngày sinh", self.profile.get('NgaySinh')),
            ("Email sinh viên", self.profile.get("EmailSinhVien")),
            ("Email phụ huynh", self.profile.get("EmailPhuHuynh")),
            ("Email GVCN", self.profile.get("EmailGVCN")) 
        ]
        
        self.entries = []
        for label_text, value in self.details:  
            row_frame = tk.Frame(self.infor_frame, bg="#1c1c1c")
            row_frame.pack(fill="x", padx=20, pady=5)                  
            tk.Label(row_frame, text=label_text, bg="#1c1c1c", fg="white", font=("Arial", 12), width=15, anchor="w").pack(side="left")
            if label_text == "Ngày sinh":
                self.birthDay_entry = DateEntry(row_frame, font=("Arial", 12), width=50, fg="black", date_pattern="dd/MM/yyyy", state="readonly")
                self.birthDay_entry.set_date(value)
                self.birthDay_entry.pack(side="left")
                self.birthDay_entry.bind("<FocusOut>", lambda e: self.validate_date(value))
                self.entries.append((None, value, label_text))
            else:
                if label_text == "Giới tính": 
                    self.gender_var = tk.StringVar(value=value) 
                    options = ["Nam", "Nữ"] 
                    entry = tk.OptionMenu(row_frame, self.gender_var, *options)
                    entry.config(font=("Arial", 12), fg="black", bd=0)
                else:
                    entry = tk.Entry(row_frame, font=("Arial", 12), width=50, fg="black")
                    entry.insert(0, value)
                
                entry.pack(side="left")
                entry.bind("<Button-1>", lambda e: "break")
            if label_text != "Mã sinh viên":
                self.entries.append((entry, value, label_text))
            else:
                self.studen_id = value

    def validate_date(self, default):
        try:
            datetime.strptime(self.birthDay_entry.get(), "%d/%m/%Y")
            return True
        except ValueError:
            self.birthDay_entry.set_date(default)

    def enable_edit_all(self):
        for entry, default, entry_type in self.entries:
            if entry_type != "Ngày sinh":
                entry.unbind("<Button-1>")
            else:
                self.birthDay_entry.set_date(default)
        self.birthDay_entry.config(state="normal")
           
        self.edit_button.pack_forget()
        self.confirm_button.pack(side="left", padx = 5)
        self.cancel_button.pack(side="left", padx = 5)
       
    def cancel_edit(self):
        for entry, default, entry_type in self.entries:
            if entry_type != "Ngày sinh":
                entry.bind("<Button-1>", lambda e: "break")
            else:
                self.birthDay_entry.config(state="readonly")
                self.birthDay_entry.set_date(default)
        self.cancel_button.pack_forget()
        self.confirm_button.pack_forget()
        self.edit_button.pack(side="left", padx=5)
        
    def confirm_edit(self):
        # Lấy giá trị từ các ô Entry
        ma_sinh_vien = self.studen_id
        ho_ten = self.entries[0][0].get()
        gioi_tinh = self.gender_var.get()
        ngay_sinh = self.birthDay_entry.get_date().strftime("%d/%m/%Y")
        EmailSinhVien = self.entries[4][0].get()
        EmailPhuHuynh = self.entries[5][0].get()
        EmailGVCN = self.entries[6][0].get()

        #Gọi hàm update_student với các giá trị đã lấy
        try: 
            self.student_controller.update_student(ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh, EmailSinhVien, EmailPhuHuynh, EmailGVCN)
            tk.messagebox.showinfo("Thành công", "Sửa sinh viên thành công")
        except Exception as ex:
            print(ex)
            tk.messagebox.showwarning("Cảnh báo", "Sửa sinh viên không thành công")
        self.cancel_edit()
                


    def class_view(self):
        self.class_student = self.student_class_controller.search_class_by_student_id(self.ma_sinh_vien)

        self.class_frame = tk.Frame(self.profile_frame, bg="#1c1c1c")
        # Tạo Treeview để hiển thị kết quả
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("STT", "MaLopHocPhan", "TenMonHoc", "CoSo", "Phong",  "HocKy")
        self.class_tree = ttk.Treeview(self.class_frame, columns=columns, show="headings", style="Treeview")

        self.class_tree.heading("STT", text="STT")
        self.class_tree.heading("MaLopHocPhan", text="Mã lớp học phần")
        self.class_tree.heading("TenMonHoc", text="Tên môn học")
        self.class_tree.heading("HocKy", text="Học kỳ")
        self.class_tree.heading("CoSo", text="Cơ sở")
        self.class_tree.heading("Phong", text="Phòng")  

        # Đặt chiều rộng cột và tô màu nền khác nhau
        self.class_tree.column("STT", width=70, anchor="center")
        self.class_tree.column("MaLopHocPhan", width=150, anchor="center")
        self.class_tree.column("TenMonHoc", width=150, anchor="center")
        self.class_tree.column("HocKy", width=100, anchor="center")
        self.class_tree.column("CoSo", width=70, anchor="center")
        self.class_tree.column("Phong", width=100, anchor="center")  

        self.class_tree.tag_configure('evenrow', background='white')
        self.class_tree.tag_configure('oddrow', background='#e6e6e6')

        self.class_tree.pack(fill="both", expand=True, padx=10, pady=10)

        for index, result in enumerate(self.class_student):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            values = (index+1, result["MaLopHocPhan"], result["TenMonHoc"], result["CoSo"], result["Phong"], result["HocKy"])
            self.class_tree.insert("", "end", values=values, tags=tag)

    def schedule_view(self):
        self.schedule_frame = tk.Frame(self.profile_frame, bg="#1c1c1c")
        # Tạo Treeview để hiển thị kết quả
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("NgayHoc", "TinhTrang")
        self.schedule_tree = ttk.Treeview(self.schedule_frame, columns=columns, show="headings", style="Treeview")

        self.schedule_tree.heading("NgayHoc", text="Ngày Học")      
        self.schedule_tree.heading("TinhTrang", text="Tình trạng")

        # Đặt chiều rộng cột và tô màu nền khác nhau
        self.schedule_tree.column("NgayHoc", width=100, anchor="center")      
        self.schedule_tree.column("TinhTrang", width=70, anchor="center")

        self.schedule_tree.tag_configure('evenrow', background='white')
        self.schedule_tree.tag_configure('oddrow', background='#e6e6e6')

        self.schedule_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def show_class_view(self):
        self.schedule_frame.pack_forget()
        self.class_button.config(state="disabled", bg="#1c1c1c", fg="white", font=("Arial", 12, "underline", "bold"), borderwidth=0, disabledforeground="white")
        self.schedule_button.config(state="normal", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, borderwidth=2)
        self.class_frame.pack(fill="both", expand=True)


    
    def show_schedule_view(self):
        selected_item = self.class_tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lớp học phần!")
            return
        
        self.class_frame.pack_forget()
        self.schedule_button.config(state="disabled", bg="#1c1c1c", fg="white", font=("Arial", 12, "underline", "bold"), borderwidth=0, disabledforeground="white")
        self.class_button.config(state="normal", bg="#2c2c2c", fg="white", font=("Arial", 12), width=15, borderwidth=2)
        self.schedule_frame.pack(fill="both", expand=True)  

        item = self.class_tree.item(selected_item)
        values = item["values"]
        MaLopHocPhan = "0" + str(values[1])
        schedule_controller = ScheduleController()
        schedule_list = schedule_controller.search_schedule_list(self.ma_sinh_vien, MaLopHocPhan)
        for index, result in enumerate(schedule_list):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            values = (result["NgayHoc"], result["TrangThai"])
            self.schedule_tree.insert("", "end", values=values, tags=tag)
        

    