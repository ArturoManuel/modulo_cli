import json
import networkx as nx
import matplotlib.pyplot as plt


def dibujar_topologia(json_data):
    vms = json_data['vms']
    topologia_tipo = json_data.get('topologia', 'desconocida')
    output_filename = f'topologia_{topologia_tipo}.png'  # Generar el nombre basado en la topología

    G = nx.Graph()  # Crear un grafo vacío

    # Añadir nodos (VMs) al grafo
    for vm in vms:
        G.add_node(vm['name'], label=vm['name'])

    # Crear un diccionario para mapear VLANs a VMs conectadas a esas VLANs
    vlan_to_vm = {}

    # Recorremos cada VM y sus interfaces para mapear las VLANs
    for vm in vms:
        for interface in vm['interfaces']:
            vlan = interface['vlan']
            if vlan not in vlan_to_vm:
                vlan_to_vm[vlan] = []
            vlan_to_vm[vlan].append(vm['name'])

    # Añadir aristas al grafo basadas en las VMs que comparten la misma VLAN
    for vlan, vm_list in vlan_to_vm.items():
        # Crear aristas entre todas las VMs conectadas a la misma VLAN
        for i in range(len(vm_list)):
            for j in range(i + 1, len(vm_list)):
                G.add_edge(vm_list[i], vm_list[j], label=f"VLAN {vlan}")

    # Dibujar el grafo con los nodos y las aristas
    pos = nx.spring_layout(G)  # Usa un layout flexible que ajusta automáticamente las conexiones
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    
    # Dibujar los nodos
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
    nx.draw_networkx_labels(G, pos, labels, font_size=12)
    
    # Dibujar las aristas con etiquetas de VLAN
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Guardar la gráfica como archivo
    plt.title(f"Topología: {json_data['topologia']} - {len(vms)} nodos")
    plt.savefig(output_filename)
    plt.close()

    # Imprimir el nombre del archivo en la línea de comandos
    print(f"Gráfica guardada como: {output_filename}")

# Función para leer el archivo .json y graficar la topología
def generar_grafica_desde_archivo(archivo_json):
    try:
        # Abrir y leer el archivo .json
        with open(archivo_json, 'r') as file:
            data = json.load(file)  # Cargar el JSON desde el archivo
            # Dibujar la topología
            dibujar_topologia(data)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_json} no se encontró.")
    except json.JSONDecodeError as e:
        print(f"Error en el formato del JSON: {e}")