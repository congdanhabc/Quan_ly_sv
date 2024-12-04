from model.student import StudentModel

class StudentController:
    def __init__(self):
        self.student_list = None

    def search_student_by_name(self, name):
        self.student_model = StudentModel()
        self.student_list = self.student_model.search_student(name)
        return self.student_list
    
    def get_student_profile(self, ma_sinh_vien):
        self.student_model = StudentModel()
        return self.student_model.get_student(ma_sinh_vien)
    
    def update_student(self, ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh, EmailSinhVien, EmailPhuHuynh, EmailGVCN):
        self.student_model = StudentModel()
        return self.student_model.update_student(ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh, EmailSinhVien, EmailPhuHuynh, EmailGVCN)

    def delete_student(self, ma_sinh_vien):
        self.student_model = StudentModel()
        return self.student_model.delete_student(ma_sinh_vien)
    
    def add_student(self, ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh):
        self.student_model = StudentModel()
        return self.student_model.add_student(ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh)
    
    def fill_absent_list(self, absent_list):
        student_model = StudentModel()
        student_model.fill_absent_list(absent_list)