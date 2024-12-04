from model.student_class import Student_ClassModel
from controller.class_study import ClassController

class Student_ClassController:
    def __init__(self):
        self.class_list = None

    def search_class_by_student_id(self, id):
        student_class_model = Student_ClassModel()
        class_id_list = student_class_model.search_student_class(id)
        class_controller = ClassController()
        self.class_list = class_controller.search_class_by_student_id(class_id_list)
        return self.class_list
    
    def search_student_class_id(self, ma_sinh_vien, ma_hoc_phan):
        student_class_model = Student_ClassModel()
        student_class_id = student_class_model.search_student_class_id(ma_sinh_vien, ma_hoc_phan)
        return student_class_id

    def fill_absent_list(self, absent_list):
        student_class_model = Student_ClassModel()
        student_class_model.fill_absent_list(absent_list)