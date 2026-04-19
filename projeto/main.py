from Services.system import System
from Ui.interface import Interface
from DataBase import UserRepository
import os
import shutil

data_base = UserRepository()
data_base.create_table_users()
data_base.create_table_tasks()

columns = shutil.get_terminal_size().columns
system = System()
ui = Interface(system)
def execute_action(choice) -> None:
    options_for_user = {'0': system.exiting,
                        '1': lambda: ui.handle(system.register_user),
                        '2': lambda: ui.handle(system.login),
                        '3': lambda: ui.handle(system.edit_profile),
                        '4': lambda: ui.handle(system.view_own_info),
                        '5': lambda: ui.handle(system.create_tasks),
                        '6': lambda: ui.handle(system.show_tasks),
                        '7': lambda: ui.handle(system.edit_tasks)
                        }
    action = options_for_user.get(choice)
    if action:
        action()
    else:
        print("That comand dont exist!")
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    ui.print_header()
    print('\n')
    menu = ["|1| Register a new user",
    "|2| Sing-in",
    "|3| Edit your information",
    "|4| Check my information",
    "|5| Creat a new task",
    "|6| Check my tasks",
    "|7| Update tasks", 
    "|0| Exit"]
    for option in menu:
        print(f'\n{option.center(columns)}')
    choice = str(input("\nwhat you want to do? "))
    execute_action(choice)