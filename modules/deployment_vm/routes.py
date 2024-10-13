from config_backend import deployment_vm as BASE_URL
import requests
import pandas as pd

def deploy_topology(user_id, filename):
    endpoint_url = f"{BASE_URL}/deploy/{user_id}/{filename}"
    try:
        response = requests.post(endpoint_url)
        if response.status_code == 200:
            print(f"Respuesta del servidor: {response.json()['message']}")
        else:
            print(f"Error al desplegar la topología: {response.status_code}")
    except Exception as e:
        print(f"Se produjo un error al conectar con el servidor: {str(e)}")


def delete_topology_funtion(user_id, filename):
    url = f"{BASE_URL}/eliminar/{user_id}/{filename}"  # Cambia la URL según tu configuración
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("Eliminación completada con éxito:", response.json())
        else:
            print("Error al eliminar:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error al conectar con la API:", e)

def get_vm_stats(ip):
    url = f"{BASE_URL}/system-stats"
    headers = {'Content-Type': 'application/json'}
    data = {"ip": ip}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print("Estadísticas recibidas:")
        
        # Crear un DataFrame para organizar y mostrar las estadísticas
        data = {
            "Recurso": ["CPU Uso", "Memoria Total", "Memoria Usada", "Memoria Disponible", "Memoria % Usada", "Disco Usado", "Disco Libre", "Disco % Usado"],
            "Valor": [
                stats['uso_cpu'],
                stats['memoria']['total'],
                stats['memoria']['usada'],
                stats['memoria']['disponible'],
                stats['memoria']['porcentaje_usada'],
                stats['disco']['usado'],
                stats['disco']['libre'],
                stats['disco']['porcentaje_usado']
            ]
        }
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
    else:
        print(f"Error al obtener estadísticas: {response.status_code} - {response.text}")

    input("Presione Enter para continuar...")