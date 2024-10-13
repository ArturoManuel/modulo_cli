import json
import networkx as nx
import matplotlib.pyplot as plt

# Función para dibujar la topología de VMs basada en las VLANs y las conexiones
def dibujar_topologia(json_data):
    vms = json_data['vms']
    topologia_tipo = json_data.get('topologia', 'desconocida')
    output_filename = f'topologia_{topologia_tipo}.png'  # Generar el nombre basado en la topología

    G = nx.Graph()  # Crear un grafo vacío

    # Añadir nodos (VMs) al grafo y marcar las que tienen VLAN 100
    vm_colores = {}  # Diccionario para definir colores de los nodos
    tiene_salida_internet = False  # Verificar si alguna VM tiene VLAN 100

    for vm in vms:
        salida_internet = any(interface['vlan'] == '100' for interface in vm['interfaces'])
        color = 'lightgreen' if salida_internet else 'skyblue'
        G.add_node(vm['name'], label=vm['name'])
        vm_colores[vm['name']] = color

        if salida_internet:
            tiene_salida_internet = True

    # Crear un diccionario para mapear VLANs a VMs conectadas a esas VLANs
    vlan_to_vm = {}
    for vm in vms:
        for interface in vm['interfaces']:
            vlan = interface['vlan']
            if vlan not in vlan_to_vm:
                vlan_to_vm[vlan] = []
            vlan_to_vm[vlan].append(vm['name'])

    # Añadir aristas al grafo basadas en las VMs que comparten la misma VLAN
    for vlan, vm_list in vlan_to_vm.items():
        if vlan == '100':
            continue  # Ignorar conexiones en VLAN 100
        for i in range(len(vm_list)):
            for j in range(i + 1, len(vm_list)):
                G.add_edge(vm_list[i], vm_list[j], label=f"VLAN {vlan}")

    # Dibujar el grafo con los nodos y las aristas
    pos = nx.spring_layout(G)  # Layout automático
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    # Dibujar los nodos con colores personalizados
    nx.draw(G, pos, with_labels=True, node_size=2000,
            node_color=[vm_colores[n] for n in G.nodes()],
            font_size=10, font_weight='bold')
    nx.draw_networkx_labels(G, pos, labels, font_size=12)

    # Dibujar las aristas con etiquetas de VLAN
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Crear la leyenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='VM (sin salida a Internet)',
                   markerfacecolor='skyblue', markersize=15),
        plt.Line2D([0], [0], marker='o', color='w', label='VM con salida a Internet (VLAN 100)',
                   markerfacecolor='lightgreen', markersize=15)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    # Guardar la gráfica como archivo
    plt.title(f"Topología: {json_data['topologia']} - {len(vms)} nodos")
    plt.savefig(output_filename)
    plt.close()

    # Imprimir el nombre del archivo en la línea de comandos
    print(f"Grafica guardada como: {output_filename}")

# Función para leer el archivo .json y graficar la topología
def generar_grafica_desde_archivo(archivo_json):
    try:
        with open(archivo_json, 'r') as file:
            data = json.load(file)  # Cargar el JSON desde el archivo
            dibujar_topologia(data)  # Dibujar la topología
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_json} no se encontró.")
    except json.JSONDecodeError as e:
        print(f"Error en el formato del JSON: {e}")