from config_backend import deployment_vm as BASE_URL
import requests
import pandas as pd
import json

def deploy_topology(user_id, filename):
    endpoint_url = f"{BASE_URL}/deploy/{user_id}/{filename}"
    try:
        response = requests.post(endpoint_url)
        if response.status_code == 200:
            # Obteniendo la respuesta JSON del servidor
            response_data = response.json()
            print("Respuesta del servidor:")
            # Imprimir de forma bonita la respuesta
            print(json.dumps(response_data, indent=4))
        else:
            print(f"Error al desplegar la topología: {response.status_code}")
    except Exception as e:
        print(f"Se produjo un error al conectar con el servidor: {str(e)}")



def delete_topology_funtion(user_id, filename):
    url = f"{BASE_URL}/eliminar/{user_id}/{filename}"  # Cambia la URL según tu configuración
    try:
        response = requests.post(url)
        if response.status_code == 200:
             # Obteniendo la respuesta JSON del servidor
            response_data = response.json()
            print("Respuesta del servidor:")
            # Imprimir de forma bonita la respuesta
            print(json.dumps(response_data, indent=4))
        else:
            print("Error al eliminar:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error al conectar con la API:", e)
