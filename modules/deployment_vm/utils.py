from modules.slice_manager.routes import list_slices
from modules.deployment_vm.routes import deploy_topology,delete_topology_funtion

def select_topology(user_id):
    slices = list_slices(user_id)  # Suponiendo que esta función ya está implementada y retorna una lista de nombres de archivo
    if not slices:
        print("No se encontraron topologías para este usuario.")
    else:
        print("\n--- Topologías disponibles ---")
        for i, slice_file in enumerate(slices, 1):
            print(f"{i}. {slice_file}")
        selected_index = input("Seleccione el número de la topología para desplegar o 'r' para regresar: ")
        if selected_index.lower() == 'r':
            print("Operación cancelada.")
            return
        try:
            selected_index = int(selected_index) - 1
            if 0 <= selected_index < len(slices):
                selected_name = slices[selected_index]
                deploy_topology(user_id, selected_name)  # Función para desplegar la topología
            else:
                print("Número de selección no válido.")
        except ValueError:
            print("Entrada no válida, por favor introduzca un número.")
    input("Presione Enter para continuar...")


def delete_topology(user_id):
    slices = list_slices(user_id)  # Suponiendo que esta función ya está implementada y retorna una lista de nombres de archivo
    if not slices:
        print("No se encontraron topologías para este usuario.")
    else:
        print("\n--- Topologías disponibles para eliminación ---")
        for i, slice_file in enumerate(slices, 1):
            print(f"{i}. {slice_file}")
        selected_index = input("Seleccione el número de la topología para eliminar o 'r' para regresar: ")
        if selected_index.lower() == 'r':
            print("Operación cancelada.")
            return
        try:
            selected_index = int(selected_index) - 1
            if 0 <= selected_index < len(slices):
                selected_name = slices[selected_index]
                delete_topology_funtion(user_id, selected_name)  # Función para confirmar y luego eliminar la topología
            else:
                print("Número de selección no válido.")
        except ValueError:
            print("Entrada no válida, por favor introduzca un número.")
    input("Presione Enter para continuar...")


def monitor_resources():
    print("Función para monitorear recursos de una topología seleccionada.")
    # Aquí va la lógica para monitorear recursos como CPU, memoria, etc.
    input("Presione Enter para continuar...")
