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


def show_deployment_menu():
    print("\n--- Menú de Despliegue de Topología ---")
    print("1. Seleccionar una topología")
    print("2. Eliminar una topología")
    print("3. Monitorear recursos")
    print("4. Monitorear procesos")
    print("5. Regresar al menú anterior")
    return input("Seleccione una opción: ")



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

def show_vm():
    print("\n--- Seleccione la imagen para la VM ---")
    print("1. cirros-0.6.2-x86_64-disk.img")
    print("2. focal-server-cloudimg-amd64.img")
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
    
def select_vm(image_vm):
    if image_vm == '1':
        return "cirros-0.6.2-x86_64-disk.img"
    elif image_vm == '2':
        return "focal-server-cloudimg-amd64.img"