# Función para mostrar el menú de usuario corriente
def show_user_menu():
    print("\n--- Menú Usuario Corriente ---")
    print("1. Implementar topología predefinida")
    print("2. Monitorear recursos del sistema")
    print("3. Listar VMs")
    print("4. Salir")
    return input("Seleccione una opción: ")

# Función para mostrar el menú de admin
def show_admin_menu():
    print("\n--- Menú Admin ---")
    print("1. Crear nueva VM")
    print("2. Ver slices activos")
    print("3. Monitorear recursos del sistema")
    print("4. Eliminar slice")
    print("5. Ver usuarios")
    print("6. Salir")
    return input("Seleccione una opción: ")

# Función principal para la ejecución del menú en función del rol
def execute_menu(role):
    while True:
        if role == 'user':
            option = show_user_menu()
            if option == '1':
                print("Implementando topología predefinida...")
            elif option == '2':
                print("Monitoreo de recursos del sistema...")
            elif option == '3':
                print("Listando VMs...")
            elif option == '4':
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
        elif role == 'admin':
            option = show_admin_menu()
            if option == '1':
                print("Creación de nueva VM...")
            elif option == '2':
                print("Mostrando slices activos...")
            elif option == '3':
                print("Monitoreo de recursos del sistema...")
            elif option == '4':
                print("Eliminando slice...")
            elif option == '5':
                print("Mostrando usuarios...")
            elif option == '6':
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
