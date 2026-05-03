from Ui.colors import Colors
from typing import Callable
from time import sleep
import getpass
import shutil
class Interface:
    def __init__(self, Sistema):
        self.system = Sistema
    def new_user(self) -> tuple[str, str, str]:
        name = str(input("Insert your name username: "))
        gmail = str(input("Insert your gmail: "))
        password = str(input("Insert your password user: "))
        return name.strip(), gmail, password
    def login(self) -> tuple[str, str]:
            gmail = str(input("Enter your gmail for login: "))
            password = str(input("Enter your password for login: "))
            return gmail, password
    def edit_profile(self) -> tuple[str, str]:
        options_for_edit = str(input("|1| name" \
            "\n|2| gmail" \
            "\n|3| password"
            "\nWhat field do you want for edit? "))
        if options_for_edit == '1':
            name = str(input("Enter your new name: "))
            return('name', name)
        if options_for_edit == '2':
            gmail = str(input("Enter your new gmail: "))
            return ('gmail', gmail)
        if options_for_edit == '3':
            password = getpass.getpass("Enter your new password: ")
            return ('password', password)

    def create_tasks(self) -> tuple[str, str]:
            task_name = str(input("Enter name for your task: "))
            description = str(input("Enter a description for your task(Optional): "))
            return task_name, description

    def edit_task(self, tasks: Callable[[int], tuple[str, str, str, str] | bool]) -> tuple[str, str, int] | None:
        self.show_tasks(tasks)
        try:
            id_task = int(input("What task you do you want edit: "))
            task_selected = str(input("|1| Name" \
            "\n|2| Description" \
            "\n|3| Status" \
            "\nWhat field do you want for edit: "))
            if task_selected == '1':
                name = str(input("Enter a new name for your task: "))
                return ('name', name, id_task)
            if task_selected == '2':
                description = str(input("Enter a new description: "))
                return ('description', description, id_task)
            if task_selected == '3':
                    status = int(input("|1| Outstanding" \
                    "\n|2| Finished"
                    "\nWhat do you want to do ?"))
                    if status == 1:
                        status = 'Outstanding'
                    if status == 2:
                        status = 'Finished'
                    else:
                        return None
                    return ('status', status, id_task)
        except ValueError:
            return None
        return None
        
    def show_tasks(self, tasks: dict | bool) -> True | False:
        if tasks:
            for task in tasks:
                print(f"ID = {task['id']} | Name = {task['name']} | Description = {task['description']} | status = {task['status']}")
            return True
        return False
    def del_task(self, tasks: Callable[[int], tuple[str, str, str, str] | bool]) -> bool:
        if tasks:
            try:
                self.show_tasks(tasks)
                task_selected = int(input('Select your ID task for delete: '))
                return task_selected
            except ValueError:
                return False
        return None
    def print_header(self) -> None:
        columns = shutil.get_terminal_size().columns
        lines = [
                "",
            "████████╗ █████╗ ███████╗██╗  ██╗███████╗██╗      ██████╗ ██╗    ██╗",
            "╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝██║     ██╔═══██╗██║    ██║",
            "   ██║   ███████║███████╗█████╔╝ █████╗  ██║     ██║   ██║██║ █╗ ██║",
            "   ██║   ██╔══██║╚════██║██╔═██╗ ██╔══╝  ██║     ██║   ██║██║███╗██║",
            "   ██║   ██║  ██║███████║██║  ██╗██║     ███████╗╚██████╔╝╚███╔███╔╝",
            "   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ ",
            ""
        ]
        for line in lines:
            print(f"{Colors.BOLD}{Colors.BLUE}{line.center(columns)}{Colors.RESET}")

    def handle(self, func: Callable[[], tuple[bool, str]]) -> None:
        booll, mensage = func()
        if booll:
            print('\n')
            print(f"{Colors.BOLD}{mensage}{Colors.GREEN}")
            sleep(2)
            return
        print(f"{Colors.BOLD}{mensage}{Colors.RED}")
        sleep(2)
    