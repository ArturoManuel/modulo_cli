import requests
from config_backend import slice_manager as BASE_URL
import os
from modules.menus.users.topology import admin_topology_menu
from modules.slice_manager.routes import list_slices ,view_slice_details,delete_slice
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def admin_topology(user_id):
    while True:
        option = admin_topology_menu()
        if option == '1':
            slices = list_slices(user_id)  # Llamada a la función que obtiene los slices
            if slices:
                print("\n--- Slices encontrados ---")
                for i, slice_file in enumerate(slices, 1):
                    print(f"{i}. {slice_file}")
                
                # Menú para ver detalles o regresar
                while True:
                    print("\nOpciones:")
                    print("1. Ver detalles de una topología")
                    print("2. Regresar al menú anterior")
                    user_option = input("Seleccione una opción: ")
                    
                    if user_option == '1':
                        selected_name = input("Ingrese el nombre de la topología que desea ver (por ejemplo: '1_prueba.json'): ")
                        
                        if selected_name in slices:
                            view_slice_details(user_id, selected_name)  # Llamada para ver detalles
                            input("\nPresione Enter para regresar a la lista de slices...")
                            clear_console()  # Limpiar consola después de ver los detalles
                            break  # Regresar al menú anterior de listar topologías
                        else:
                            print(f"El nombre '{selected_name}' no está en la lista. Intente de nuevo.")
                    
                    elif user_option == '2':
                        clear_console()
                        break  # Regresar al menú anterior
                    else:
                        print("Opción no válida. Intente de nuevo.")
                        input("Presione Enter para continuar...")

            else:
                print("No se encontraron slices para este usuario.")
                input("Presione Enter para continuar...")
                clear_console()

        elif option == '2':
            print(f"Unir topologías para el usuario con ID: {user_id}...")
            # Aquí puedes agregar la lógica para unir topologías
            input("Presione Enter para continuar...")
        
        elif option == '3':

            slices = list_slices(user_id)

            if slices:
                print("\n--- Slices encontrados ---")
                for i, slice_file in enumerate(slices, 1):
                    print(f"{i}. {slice_file}")
                while True:
                    print("\nOpciones:")
                    print("1. Borrar un archivo de topología")
                    print("2. Regresar al menú anterior")
                    user_option = input("Seleccione una opción: ")

                    if user_option == '1':
                        selected_name = input("Ingrese el nombre del archivo de topología que desea borrar (por ejemplo: '1_prueba.json'): ")
                        
                        if selected_name in slices:
                            # Llamada al endpoint para borrar el archivo
                            delete_response = delete_slice(selected_name)
                            print(f"\n{delete_response['message']}")
                            input("\nPresione Enter para regresar al menú anterior...")
                            clear_console()
                            break  # Regresar al menú anterior después de borrar
                        else:
                            print(f"El nombre '{selected_name}' no está en la lista. Intente de nuevo.")

                    elif user_option == '2':
                        clear_console()
                        break  # Regresar al menú anterior
                    else:
                        print("Opción no válida. Intente de nuevo.")
                        input("Presione Enter para continuar...")
            else:
                print("No se encontraron slices para este usuario.")
                input("Presione Enter para continuar...")
                clear_console()


            
        
        elif option == '4':
            print("Regresando al menú anterior...")
            return None  # Regresar al menú anterior

        else:
            print("Opción no válida. Intente de nuevo.")
            input("Presione Enter para continuar...")

