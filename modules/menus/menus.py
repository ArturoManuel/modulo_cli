import os
import json
from modules.menus.users.topology import show_topology,show_user_menu,show_flavors , show_user_menu_by_drivers
from modules.slice_manager.routes import  implement_topology
from modules.slice_manager.utils import  admin_topology
from modules.authetication.user_roles import session_data
from modules.deployment_vm.menu import deployment_menu
from modules.import_vm.utils import upload_selected_image
from modules.import_plantillas.utils import parse_arguments,import_and_deploy

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
                show_user_menu_by_drivers()  
                deployment_menu(session_data.get("id"))
            elif option == '4':
                upload_selected_image()
            elif option == '5':
                # import_json_template()
                args = parse_arguments()
                import_and_deploy(args)

            elif option == '6':
                print("Saliendo del sistema...")
                break
            elif option == '7':
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida. Intente de nuevo.")
                input("Presione Enter para continuar...")
        elif role == 'admin':
            print("Opciones de Admin aún no implementadas")
            break
