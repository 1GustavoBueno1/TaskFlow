from Ui.interface import Interface
from Logs.savelogs import SaveLog
from DataBase import UserRepository
import bcrypt
from sys import exit
from time import sleep

class System:
    def __init__(self):
        self.user_logged = None
        self.ui = Interface(self)
        self.logs = SaveLog()
        self.data_base = UserRepository()
    def check_gmail(self, gmail):
        if '@gmail.com' not in gmail or len(gmail) < 10:
            return False
        return True
    
    def register_user(self) -> tuple[bool, str]:
        name, gmail, password = self.ui.new_user()
        if self.check_gmail(gmail):
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.data_base.insert(name, gmail, password_hash)
            self.logs.success(f"Register completed: {gmail}")
            return (True, 'User registration successfull')
        return (False, 'Error registering the user, check your credentials and try again!')
    
    def login(self) -> tuple[bool, str]:
        gmail, senha = self.ui.login()
        user = self.data_base.login(gmail)
        if user and bcrypt.checkpw(senha.encode(), user[3].encode()):
            self.user_logged = user
            self.logs.success(f"Success to login: {gmail}")
            return (True, 'Success to carry out login')
        self.logs.error(f"Access deined: {gmail}")
        return (False, 'Error to carry out login, check your credentials and try again!\n')
    
    def edit_profile(self) -> tuple[bool, str]:
        if self.user_logged:
            colum, data = self.ui.edit_profile()
            if colum == 'name':
                self.data_base.update_user(colum, data, self.user_logged[0])
                self.user_logged[1] = data
            if colum == 'gmail':
                self.data_base.update_user(colum, data, self.user_logged[0])
                self.user_logged[2] = data
            if colum == 'password':
                data_hash = bcrypt.hashpw(data.encode(), bcrypt.gensalt())
                self.data_base.update_user(colum, data_hash, self.user_logged[0])
                self.user_logged[3] = data_hash
            return True, 'Success when updating the information'
        return False, 'Carry out login for update your informations!'
    
    def view_own_info(self) -> tuple[bool, str]:
        if self.user_logged:
            return True, f'ID = {self.user_logged[0]} | Name = {self.user_logged[1]} | Email = {self.user_logged[2]}'
        return False, 'Carry out login to check your informations!'

    def edit_tasks(self) -> tuple[bool, str]:
        if self.user_logged:
            self.ui.show_tasks(self.data_base.show_tasks(self.user_logged[0]))
            colum, new_data, id_task = self.ui.edit_task()
            if colum == 'name':
                self.data_base.update_task(colum, new_data, self.user_logged[0], id_task)
                return True, 'Task name updated successfully'
            if colum == 'description':
                self.data_base.update_task(colum, new_data, self.user_logged[0], id_task)
                return True, 'Task description updated successfully'
            if colum == 'status':
                self.data_base.update_task(colum, new_data, self.user_logged[0], id_task)
                return True, 'Task status updated successfully!'
        return False, 'Carry out login for update tasks'

    def create_tasks(self) -> tuple[bool, str]:
       if self.user_logged:
           values = self.ui.create_tasks()
           self.data_base.insert_task(values[0], values[1], self.user_logged[0])
           return True, 'Task created successfully'
       return False, 'Carry out login to use this function!'
         
    def show_tasks(self) -> tuple[bool, str]:
        if self.user_logged:
            self.ui.show_tasks(self.data_base.show_tasks(self.user_logged[0]))
            return True, ''
        return False, 'Carry out login to'
    def exiting(self) -> None:
        print("Exiting...")
        sleep(2)
        exit()