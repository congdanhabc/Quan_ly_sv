from model.user import UserModel

class UserController:
    def __init__(self):
        self.user_model = UserModel()
        self.user = None

    def login(self, username, password):
        self.user = self.user_model.check_login(username, password)
        return self.user

    def register_user(self, name, username, password):
        return self.user_model.register_user(name, username, password)
    
    

        