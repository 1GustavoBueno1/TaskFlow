from flask.blueprints import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix = '/task')

class Tasks():
    def list_tasks(self) -> tuple[bool, str]:
        if self.user_logged:
            if self.ui.show_tasks(self.data_base.show_tasks(self.user_logged['id'])):
                return True, ""
            return False, 'You dont have tasks for show'
        return False, 'Log in to view tasks.'
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