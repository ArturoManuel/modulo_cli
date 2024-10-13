from modules.menus.users.topology import show_deployment_menu
from modules.deployment_vm.utils import select_topology, delete_topology, monitor_resources , monitorear_vm
import os
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def deployment_menu(user_id):
    while True:
        clear_console()
        option = show_deployment_menu()
        if option == '1':
            select_topology(user_id)
        elif option == '2':
            delete_topology(user_id)
        elif option == '3':
            monitor_resources()
        elif option == '4':
            monitorear_vm()  # Llamada corregida a la función monitorear_vm
        elif option == '5':
            print("Regresando al menú principal...")
            break  # Salir del menú de despliegue
        else:
            print("Opción no válida. Intente de nuevo.")
            input("Presione Enter para continuar...")