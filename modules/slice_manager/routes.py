
import requests
from config_backend import slice_manager as BASE_URL
from modules.menus.users.topology import show_topology,show_flavors,select_flavor,show_vm ,select_vm
from modules.slice_manager.grafic_topology import dibujar_topologia
import json
import os
import platform
import time



def clear_console():
    """Limpia la consola dependiendo del sistema operativo."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def validate_input(prompt, validation_fn, error_message):
    """
    Solicita un input al usuario y lo valida utilizando una función.
    Permite regresar al input anterior usando la tecla 'r'.
    
    :param prompt: Mensaje que se mostrará al usuario.
    :param validation_fn: Función que evalúa si la entrada es válida.
    :param error_message: Mensaje que se muestra si la validación falla.
    :return: Entrada válida o 'retry' si el usuario ingresa 'r'.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'r':
            print("Regresando al paso anterior...")
            return 'retry'
        if validation_fn(user_input):
            return user_input
        print(error_message)
        time.sleep(3)
        clear_console()



def implement_topology(user_id):
    while True:  # Bucle principal
        topology = {}
        while True:
            clear_console()
            topology_option = validate_input(
                "Seleccione la topología (1: Anillo, 2: Lineal, 3: Regresar al menú anterior): ",
                lambda x: x in {'1', '2', '3'},
                "Opción no válida. Ingrese 1, 2 o 3."
            )
            if topology_option == 'retry':
                continue
            elif topology_option == '3':
                return None  # Regresar al menú principal
            topology['topologia'] = "anillo" if topology_option == '1' else "lineal"
            break

        # Ingreso de la cantidad de nodos (VMs)
        while True:
        
            nodos = validate_input(
                "Ingrese la cantidad de nodos (VMs): ",
                lambda x: x.isdigit() and int(x) > 0,
                "Entrada no válida. Ingrese un número entero mayor que 0."
            )
            if nodos == 'retry':
                continue
            topology['nodos'] = int(nodos)
            if topology['topologia'] == "anillo" and topology['nodos'] < 3:
                print("Error: La topología 'anillo' requiere al menos 3 nodos.")
                continue
            elif topology['topologia'] == "lineal" and topology['nodos'] < 2:
                print("Error: La topología 'lineal' requiere al menos 2 nodos.")
                continue
            break

        # Solicitar las VLANs
        vlans = []
        vlan_count = topology['nodos'] if topology['topologia'] == "anillo" else topology['nodos'] - 1
        vlan_index = 0

        while vlan_index < vlan_count:
            vlan = validate_input(
                f"Ingrese el nombre de la VLAN {vlan_index + 1}: ",
                lambda x: len(x) > 0,  # Validar que no sea vacío
                "Entrada no válida. Ingrese un nombre de VLAN no vacío."
            )
            if vlan == 'retry':
                # Regresar al paso anterior (nodos)
                print("Regresando al paso de cantidad de nodos...")
                break  # Salir del bucle de VLANs y volver al bucle de nodos

            vlans.append(vlan)
            vlan_index += 1

        if len(vlans) < vlan_count:
            continue  # Volver a pedir nodos y luego VLANs

        topology['vlans'] = vlans

        # Crear VMs
        vms_creadas = []
        for i in range(topology['nodos']):
            print(f"Creando VM {i + 1} de {topology['nodos']}...")
            if topology['topologia'] == "anillo":
                vm = create_vm_anillo(user_id, i + 1, topology['vlans'], topology['nodos'])
            elif topology['topologia'] == "lineal":
                vm = create_vm_lineal(user_id, i + 1, topology['vlans'], topology['nodos'])
            if vm:
                vms_creadas.append(vm)
            else:
                print(f"Error en la creación de la VM {i + 1}. Abortando operación.")
                return None

        # Crear topología si todas las VMs fueron creadas
        if len(vms_creadas) == topology['nodos']:
            while True:
                file_name = validate_input(
                    "Ingrese el nombre del archivo de topología: ",
                    lambda x: len(x) > 0,
                    "Entrada no válida. Ingrese un nombre de archivo no vacío."
                )
                if file_name == 'retry':
                    continue
                topology['file_name'] = file_name
                break
            
            response = requests.post(f"{BASE_URL}/create_topology/{user_id}", json=topology)
            if response.status_code == 201:
                print(f"Topología '{topology['topologia']}' creada exitosamente.")
            else:
                print(f"Error creando la topología: {response.status_code}, {response.text}")
        else:
            print("Error: no se pudieron crear todas las VMs.")
        break






def create_vm_anillo(user_id, vm_number, vlans, num_vms):
    vm = {}
    vm['name'] = input(f"Ingrese el nombre de la VM{vm_number}: ")

    # Selección del flavor para esta VM
    flavor_option = show_flavors()
    flavor_cpu, flavor_ram = select_flavor(flavor_option)
    vm['cpu'] = flavor_cpu
    vm['ram'] = flavor_ram
    vm_option = show_vm()
    vm['imagen'] = select_vm(vm_option)
    
    # Interfaces: cada VM tendrá 2 interfaces conectadas a VLANs
    vm['interfaces'] = []

    # Preguntar si la VM necesita acceso a Internet
    internet_option = input(f"¿La VM{vm_number} necesita acceso a Internet? (s/n): ").lower()

    if internet_option == 's':
        # Si la VM necesita acceso a Internet, la primera interfaz será para la VLAN 100
        vm['interfaces'].append({
            "tap_name": f"tap-{vm['name']}-100",
            "vlan": "100"
        })

    # Asignar VLANs de acuerdo al orden de las VMs y el ovs_name
    if vm_number == 1:
        # Para la primera VM, se conecta la primera VLAN y la última para cerrar el ciclo
        vlan1, vlan2 = vlans[0], vlans[-1]
    else:
        # Para las otras VMs, se asignan VLANs consecutivas
        vlan1, vlan2 = vlans[vm_number - 2], vlans[vm_number - 1]

    # Definir las interfaces para las VLANs seleccionadas, manteniendo las anteriores
    vm['interfaces'].append({
        "tap_name": f"tap-{vm['name']}-{vlan1}",
        "vlan": vlan1
    })
    
    vm['interfaces'].append({
        "tap_name": f"tap-{vm['name']}-{vlan2}",
        "vlan": vlan2
    })

    # Realizar la solicitud POST para agregar la VM
    url = f"{BASE_URL}/add_vm/{user_id}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=vm, headers=headers)

    if response.status_code == 200:
        print(f"VM {vm['name']} creada exitosamente.")
    else:
        print(f"Error creando la VM: {response.status_code}, {response.text}")
    
    return vm



def create_vm_lineal(user_id, vm_number, vlans, num_vms):
    vm = {}
    vm['name'] = input(f"Ingrese el nombre de la VM{vm_number}: ")

    # Selección del flavor para esta VM
    flavor_option = show_flavors()
    flavor_cpu, flavor_ram = select_flavor(flavor_option)
    vm['cpu'] = flavor_cpu
    vm['ram'] = flavor_ram
    vm_option = show_vm()
    vm['imagen'] = select_vm(vm_option)

    # Interfaces
    vm['interfaces'] = []

    # Preguntar si la VM necesita acceso a Internet
    internet_option = input(f"¿La VM{vm_number} necesita acceso a Internet? (s/n): ").lower()

    if internet_option == 's':
        # Si la VM necesita acceso a Internet, la primera interfaz se asigna a la VLAN 100
        vm['interfaces'].append({
            "tap_name": f"tap-{vm['name']}-100",
            "vlan": "100"
        })

    # Asignar las VLANs de acuerdo al número de la VM
    if vm_number == 1:
        # La primera VM se conecta a la primera VLAN
        vlan = vlans[0]
        vm['interfaces'].append({
            "tap_name": f"tap-{vm['name']}-{vlan}",
            "vlan": vlan
        })
    elif vm_number == num_vms:
        # La última VM se conecta a la última VLAN
        vlan = vlans[-1]
        vm['interfaces'].append({
            "tap_name": f"tap-{vm['name']}-{vlan}",
            "vlan": vlan
        })
    else:
        # VMs intermedias se conectan a dos VLANs consecutivas
        vlan_prev = vlans[vm_number - 2]  # VLAN anterior
        vlan_curr = vlans[vm_number - 1]  # VLAN actual
        vm['interfaces'].append({
            "tap_name": f"tap-{vm['name']}-{vlan_prev}",
            "vlan": vlan_prev
        })
        vm['interfaces'].append({
            "tap_name": f"tap-{vm['name']}-{vlan_curr}",
            "vlan": vlan_curr
        })

    # Realizar la solicitud POST para agregar la VM
    url = f"{BASE_URL}/add_vm/{user_id}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=vm, headers=headers)

    if response.status_code == 200:
        print(f"VM {vm['name']} creada exitosamente.")
    else:
        print(f"Error creando la VM: {response.status_code}, {response.text}")
    
    return vm



def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def unir_topologias_cli(slices):
    while True:
        print("\nOpciones:")
        print("1. Unir topologías")
        print("2. Regresar al menú anterior")
        user_option = input("Seleccione una opción: ")
        
        if user_option == '1':
            # Solicitar topología 1
            topo1 = input("Ingrese el nombre de la topología 1 que desea unir (sin '.json'): ")
            if f"6_{topo1}.json" not in slices:
                print(f"El nombre '{topo1}' no está en la lista. Intente de nuevo.")
                continue
            
            # Solicitar topología 2
            topo2 = input("Ingrese el nombre de la topología 2 que desea unir (sin '.json'): ")
            if f"6_{topo2}.json" not in slices:
                print(f"El nombre '{topo2}' no está en la lista. Intente de nuevo.")
                continue
            
            # Solicitar la VM de topología 1
            vm1 = input(f"Ingrese el nombre de la VM de la topología '{topo1}': ")

            # Solicitar la VM de topología 2
            vm2 = input(f"Ingrese el nombre de la VM de la topología '{topo2}': ")
            
            # Solicitar el valor de la VLAN
            vlan_value = input("Ingrese el valor de la VLAN para unir las VMs: ")

            # Solicitar el nombre del archivo de salida
            output_file_name = input("Ingrese el nombre del archivo para guardar la nueva topología: ")

            # Datos para enviar al servidor
            payload = {
                "user_id": 6,  # El ID del usuario es 6
                "topo1_name": topo1,
                "topo2_name": topo2,
                "vm1_name": vm1,
                "vm2_name": vm2,
                "vlan_union": vlan_value,
                "output_file_name": output_file_name
            }

            # Hacer la solicitud POST al endpoint de FastAPI
            try:
                response = requests.post(f"{BASE_URL}/unir_topologias/", json=payload)
                if response.status_code == 201:
                    data = response.json()
                    print(f"Topologías unidas exitosamente. Archivo creado: {data['file']}")
                else:
                    print(f"Error al unir las topologías: {response.json()['detail']}")
            except Exception as e:
                print(f"Error al conectar con el servidor: {e}")
            
            input("\nPresione Enter para regresar al menú anterior...")
            break  # Regresar al menú anterior después de unir topologías

        elif user_option == '2':
            clear_console()
            break  # Regresar al menú anterior

        else:
            print("Opción no válida. Intente de nuevo.")
            input("Presione Enter para continuar...")









def list_slices(user_id: int):
    url = f"{BASE_URL}/list_slices/{user_id}"  # URL del endpoint
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            slices = data.get("files", [])
            return slices  # Devolver la lista de slices (archivos)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error conectando al backend: {e}")
        return []



# Ver slices :

def view_slice_details(user_id, file_name):
    url = f"{BASE_URL}/get_slice/"
    payload = {"file_name": file_name}
    
    try:
        # Haciendo la solicitud POST al endpoint
        response = requests.post(url, json=payload)

        # Verificar si la respuesta fue exitosa (código 200)
        if response.status_code == 200:
            data = response.json()  # Parsear el JSON de la respuesta
            topology_data = data.get("topology_data", {})

            # Imprimir los detalles de la topología en formato JSON
            print(f"\n--- Detalles de la topología '{file_name}' ---")
            print(json.dumps(topology_data, indent=4))

            # Llamar a la función para graficar la topología
            dibujar_topologia(topology_data)

        else:
            # Manejo de errores en caso de respuesta con código diferente de 200
            print(f"Error al obtener la topología: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # Manejo de errores de conexión o solicitud
        print(f"Error conectando al backend: {e}")












def delete_slice(file_name: str):
    url = f"{BASE_URL}/delete_slice/"
    payload = {"file_name": file_name}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  # Devuelve la respuesta del servidor con el mensaje
        else:
            return {"error": f"Error al eliminar el archivo: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error conectando al backend: {e}"}

def create_topology(user_id, topology_data):
    """
    Envía una solicitud POST para crear una topología para un usuario específico.

    Args:
    user_id (int): ID del usuario para el cual crear la topología.
    topology_data (dict): Diccionario que contiene los datos de la topología como topologia, nodos, file_name.

    Returns:
    dict or str: Respuesta del servidor.
    """
    url = f"{BASE_URL}/create_topology/{user_id}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=topology_data, headers=headers)
    
    if response.status_code == 201:
        return response.json()  # Retorna la respuesta del servidor en formato JSON
    elif response.status_code == 422:
        return response.json()  # Retorna los detalles del error de validación
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def get_vm_count(user_id):
    """
    Envía una solicitud GET para obtener el conteo de VMs de un usuario específico.

    Args:
    user_id (int): ID del usuario cuyo conteo de VMs se quiere obtener.

    Returns:
    dict or str: Respuesta del servidor.
    """
    url = f"{BASE_URL}/vm_count/{user_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Retorna el conteo de VMs en formato JSON
    elif response.status_code == 422:
        return response.json()  # Retorna los detalles del error de validación
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def clear_vms(user_id):
    """
    Envía una solicitud DELETE para eliminar todas las VMs de un usuario específico.

    Args:
    user_id (int): ID del usuario cuyas VMs se quieren eliminar.

    Returns:
    dict or str: Respuesta del servidor.
    """
    url = f"{BASE_URL}/clear_vms/{user_id}"
    response = requests.delete(url)
    
    if response.status_code == 200:
        return response.json()  # Retorna la respuesta del servidor en formato JSON
    elif response.status_code == 422:
        return response.json()  # Retorna los detalles del error de validación
    else:
        return f"Error: {response.status_code} - {response.text}"