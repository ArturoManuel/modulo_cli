import os
import json
from modules.menus.users.topology import show_topology,show_user_menu,show_flavors
from modules.slice_manager.routes import  implement_topology
from modules.slice_manager.utils import  admin_topology
from modules.authetication.user_roles import session_data
from modules.deployment_vm.menu import deployment_menu

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def execute_menu(role):
    while True:
        clear_console()
        if role == 'user':
            option = show_user_menu()
            if option == '1':
                clear_console()
                implement_topology(session_data.get("id"))
            elif option == '2':
                clear_console()
                admin_topology(session_data.get("id"))
            elif option == '3':
                clear_console()
                deployment_menu(session_data.get("id"))
            elif option == '4':
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida. Intente de nuevo.")
                input("Presione Enter para continuar...")
        elif role == 'admin':
            print("Opciones de Admin aún no implementadas")
            break
