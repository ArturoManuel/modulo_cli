from config_backend import deployment_vm as BASE_URL
import requests

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