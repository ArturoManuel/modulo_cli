
import requests
from config_backend import slice_manager as BASE_URL
from modules.menus.users.topology import show_topology,show_flavors,select_flavor

def implement_topology(user_id):
    topology = {}

    # Selección de la topología
    topology_option = show_topology()
    if topology_option == '1':
        topology['topologia'] = "anillo"
    elif topology_option == '2':
        topology['topologia'] = "lineal"
    elif topology_option == '3':
        return None  # Regresar al menú anterior

    # Ingreso de la cantidad de nodos (VMs)
    topology['nodos'] = int(input("Ingrese la cantidad de nodos (VMs): "))

    # Solicitar el nombre del OVS (solo una vez)
    ovs_name = input("Ingrese el nombre del OVS: ")

    # Solicitar las VLANs de acuerdo a la cantidad de nodos
    vlans = []
    for i in range(1, topology['nodos'] + 1):
        vlan = input(f"Ingrese el nombre de la VLAN {i}: ")
        vlans.append(vlan)

    # Crear todas las VMs primero
    vms_creadas = []
    for i in range(topology['nodos']):
        print(f"Creando VM {i + 1} de {topology['nodos']}")
        vm = create_vm(user_id, i + 1, ovs_name, vlans, topology['nodos'])
        vms_creadas.append(vm)

    # Solo si todas las VMs fueron creadas con éxito, proceder con la creación de la topología
    if len(vms_creadas) == topology['nodos']:
        # Solicitar el nombre del archivo de topología
        topology['file_name'] = input("Ingrese el nombre del archivo de topología: ")

        # Realizar la solicitud POST para crear la topología
        url = f"{BASE_URL}/create_topology/{user_id}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=topology, headers=headers)

        if response.status_code == 201:
            print(f"Topología {topology['topologia']} creada exitosamente.")
        else:
            print(f"Error creando la topología: {response.status_code}, {response.text}")
    else:
        print("Error: no se pudieron crear todas las VMs.")


def create_vm(user_id, vm_number, ovs_name, vlans, num_vms):
    vm = {}
    vm['name'] = input(f"Ingrese el nombre de la VM{vm_number}: ")
    vm['ovs_name'] = ovs_name

    # Selección del flavor para esta VM
    flavor_option = show_flavors()
    flavor_cpu, flavor_ram = select_flavor(flavor_option)
    vm['cpu'] = flavor_cpu
    vm['ram'] = flavor_ram
    vm['imagen'] = input(f"Ingrese el nombre de la imagen para VM{vm_number} (ejemplo: cirros-0.5.1-x86_64-disk.img): ")

    # Interfaces: cada VM tendrá 2 interfaces conectadas a VLANs
    vm['interfaces'] = []
    
    # Asignar VLANs de acuerdo al orden de las VMs y el ovs_name
    if vm_number == 1:
        # Para la primera VM, se conecta la primera VLAN y la última para cerrar el ciclo
        vlan1, vlan2 = vlans[0], vlans[-1]
    else:
        # Para las otras VMs, se asignan VLANs consecutivas
        vlan1, vlan2 = vlans[vm_number - 2], vlans[vm_number - 1]

    # Definir los taps con los nombres y VLANs
    vm['interfaces'].append({
        "tap_name": f"tap-{ovs_name}-{vm['name']}-{vlan1}",
        "vlan": vlan1
    })
    
    vm['interfaces'].append({
        "tap_name": f"tap-{ovs_name}-{vm['name']}-{vlan2}",
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