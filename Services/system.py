from Ui.interface import Interface
from Logs.savelogs import SaveLog
from DataBase import UserRepository
from  pymysql.err import IntegrityError
from sys import exit
from time import sleep
import bcrypt
import re
_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
class System:
    def __init__(self):
        self.user_logged = None
        self.ui = Interface(self)
        self.logs = SaveLog()
        self.data_base = UserRepository()
    def check_gmail(self, gmail) -> bool | str:
        if _EMAIL_REGEX.fullmatch(gmail):
            return gmail
        return False
    
    def register_user(self) -> tuple[bool, str]:
        name, gmail, password = self.ui.new_user()
        if not name:
            return False, "The name field cannot be empty"
        if len(password) < 6:
            return False, 'Your password is too short!'
        try:
            if self.check_gmail(gmail):
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
                self.data_base.insert(name, gmail, password_hash)
                self.logs.success(f"Register completed: {gmail}")
                return True, 'User registration successfull'
            return False, 'The email address you entered is incorrect'
        except IntegrityError:
            return False, 'Gmail already exists'
        
    def login(self) -> tuple[bool, str]:
        gmail, password = self.ui.login()
        user = self.data_base.login(gmail)
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            self.user_logged = user
            self.logs.success(f"Success to login: {gmail}")
            return True, 'Success to carry out login'
        self.logs.error(f"Access deined: {gmail}")
        return False, 'Error to carry out login, check your credentials and try again!\n'
    
    def edit_profile(self) -> tuple[bool, str]:
        if self.user_logged:
            result = self.ui.edit_profile()
            if result is None:
                return False, 'Invalid option'
            colum, data = result
            if data is None:
                return False, 'Field cannot be empty' 
            if colum == 'password':
                if len(data) < 6:
                    return False, 'Your passsword is too short'
                data = bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode('utf-8')
            if colum == 'gmail':
                data = self.check_gmail(data)
                if not data:
                    return False, 'The email address you entered is incorrect'
            try:
                self.data_base.update_user(colum, data, self.user_logged['id'])
                self.user_logged[colum] = data
                return True, 'Success when updating the information'
            except ValueError:
                return False, f'Column {colum} dont exist'
            except IntegrityError:
                return False, 'Gmail already exists'
        return False, 'Carry out login for update your informations!'
    def view_own_info(self) -> tuple[bool, str]:
        if self.user_logged:
            return True, f'ID = {self.user_logged['id']} | Name = {self.user_logged['name']} | Email = {self.user_logged['gmail']}'
        return False, 'Carry out login to check your informations!'

    def edit_tasks(self) -> tuple[bool, str]:
        if self.user_logged:
            result = self.ui.edit_task(self.data_base.show_tasks(self.user_logged['id']))
            if result is None:
                return False, 'Error editing task'
            colum, new_data, id_task = result
            if colum is None or new_data is None or id_task is None:
                return False, 'Field cannot be empty'
            try:
                self.data_base.update_task(colum, new_data, self.user_logged['id'], id_task)
                return True, 'Task updated successfully!'
            except ValueError:
                return False, f'Column {colum} dont exist'
        return False, 'Carry out login for update tasks'
    def del_task(self) -> tuple[bool, str]:
        if self.user_logged:
            task_selected = self.ui.del_task(self.data_base.show_tasks(self.user_logged['id']))
            if task_selected is None:
                return False, 'You dont have task for delete'
            if self.data_base.del_task(self.user_logged['id'], task_selected) and task_selected:
                return True, 'Your task was successfully deleted'
            return False, 'An error occurred while deleting your task; please check that the information was entered correctly.'
        return False, 'Carry out login for delete tasks'
    def create_tasks(self) -> tuple[bool, str]:
       if self.user_logged:
           name, description = self.ui.create_tasks()
           if name is None:
               return False, 'The name task cannot be empyt'
           self.data_base.insert_task(name, description, self.user_logged['id'])
           return True, 'Task created successfully'
       return False, 'Carry out login to use this function!'
    
    def show_tasks(self) -> tuple[bool, str]:
        if self.user_logged:
            if self.ui.show_tasks(self.data_base.show_tasks(self.user_logged['id'])):
                return True, ""
            return False, 'You dont have tasks for show'
        return False, 'Log in to view tasks.'
    def exiting(self) -> None:
        print("Exiting...")
        sleep(2)
        exit()