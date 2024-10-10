def show_topology():
    print("\n--- Selecciona una Topología ---")
    print("1. Anillo")
    print("2. Lineal")
    print("3. Regresar")
    return input("Seleccione una opción: ")

def admin_topology_menu():
    print("\n--- Selecciona una option---")
    print("1. Listar Topología")
    print("2. Unir topologías")
    print("3. Borrar Topología")
    print("4. Regresar")
    return input("Seleccione una opción:")



def show_user_menu():
    print("\n--- Menú Usuario Corriente ---")
    print("1. Implementar topología predefinida")
    print("2. Administrar Topología")
    print("3. Desplegar Topologias")
    print("4. Salir")
    return input("Seleccione una opción: ")

def show_flavors():
    print("\n--- Seleccione un Flavor para la VM ---")
    print("1. Flavor 1 (small): 1 CPU, 1 GB de RAM")
    print("2. Flavor 2 (medium): 2 CPUs, 2 GB de RAM")
    print("3. Flavor 3 (large): 4 CPUs, 4 GB de RAM")
    print("4. Flavor 4 (extra large): 8 CPUs, 8 GB de RAM")
    return input("Seleccione una opción: ")

def select_flavor(flavor_option):
    if flavor_option == '1':
        return 1, '1G'
    elif flavor_option == '2':
        return 2, '2G'
    elif flavor_option == '3':
        return 4, '4G'
    elif flavor_option == '4':
        return 8, '8G'
    else:
        print("Opción no válida. Seleccionando Flavor 1 por defecto.")
        return 1, '1G'