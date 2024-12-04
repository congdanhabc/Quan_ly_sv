from model.schedule import ScheduleModel
from controller.student_class import Student_ClassController
from controller.student import StudentController
from controller.class_study import ClassController

class ScheduleController:
    def __init__(self):
        self.schedule_list = None

    def search_schedule_list(self, ma_sinh_vien, ma_hoc_phan):
        student_class_cotroller = Student_ClassController()
        schedule_id = student_class_cotroller.search_student_class_id(ma_sinh_vien, ma_hoc_phan)
        schedule_model = ScheduleModel()
        self.schedule_list = schedule_model.search_schedule(schedule_id)
        return self.schedule_list
    
    def get_absent_list(self):
        schedule_model = ScheduleModel()
        absent_list = schedule_model.get_absent_list()
        student_class_cotroller = Student_ClassController()
        student_class_cotroller.fill_absent_list(absent_list)
        student_controller = StudentController()
        student_controller.fill_absent_list(absent_list)
        class_controller = ClassController()
        class_controller.fill_absent_list(absent_list)
        return absent_list

