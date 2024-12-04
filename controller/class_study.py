from model.class_study import ClassModel

class ClassController:
    def __init__(self):
        self.class_list = []

    def search_class_by_student_id(self, class_id_list):
        self.class_model = ClassModel()
        for class_id in class_id_list:
            self.class_list.append(self.class_model.get_class(class_id))
        return self.class_list
    
    def fill_absent_list(self, absent_list):
        class_model = ClassModel()
        class_model.fill_absent_list(absent_list)