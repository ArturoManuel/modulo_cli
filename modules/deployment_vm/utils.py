from tabulate import tabulate
from modules.slice_manager.routes import list_slices
from modules.deployment_vm.routes import deploy_topology,delete_topology_funtion
from modules.monitoreo_recursos.routes import get_vm_stats
import pandas as pd

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
    # Lista de VMs en la topología
    vms = {
        "worker1": "10.0.0.30",
        "worker2": "10.0.0.40",
        "worker3": "10.0.0.50"
    }

    print("Función para monitorear recursos de una topología seleccionada.\n")
    
    # Crear un DataFrame con las VMs
    df = pd.DataFrame(list(vms.items()), columns=["Servidor", "IP"])
    df['Opción'] = df.index + 1  # Añadir columna 'Opción' para facilitar la selección del usuario

    # Mostrar la tabla ordenando las columnas para que 'Opción' aparezca primero
    df = df[['Opción', 'Servidor', 'IP']]  # Reordenar las columnas

    # Usar pandas para imprimir el DataFrame formateado
    print(df.to_string(index=False))

    # Permitir al usuario elegir una VM para monitorear por número de opción
    try:
        choice = int(input("\nIngrese el número de la opción del servidor que desea monitorear: "))
        if 1 <= choice <= len(df):
            selected_row = df[df['Opción'] == choice]
            vm_name = selected_row['Servidor'].values[0]
            ip = selected_row['IP'].values[0]
            get_vm_stats(ip)
        else:
            print("Opción no válida. Asegúrese de ingresar un número de opción correcto.")
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número válido.")

    



