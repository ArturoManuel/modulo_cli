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

def process_vm_data():
    url = f'{BASE_URL}/info/'  # Reemplaza con tu URL real
    try:
        # Realizar la solicitud POST (puedes cambiar a GET si es necesario)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()  # Obtener el JSON de la respuesta
            
            # Extraer los datos relevantes en listas
            names = [vm['name'] for vm in data['data']]
            process_ids = [vm['processId'] for vm in data['data']]
            workers = [vm['worker'] for vm in data['data']]
            worker_ips = [vm['worker_ip'] for vm in data['data']]

            # Crear un DataFrame con pandas
            df = pd.DataFrame({
                "NombreVM": names,
                "ProcessID": process_ids,
                "Worker": workers,
                "IP Worker": worker_ips
            })

            # Mostrar la tabla
            print("\nLista Monitoreo de Recursos VM:\n")
            print(df.to_string(index=False))  # Mostrar el DataFrame sin los índices
        else:
            print(f"Error al obtener datos: {response.status_code} - {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")


def clean_process_json():
    # URL para limpiar el archivo process.json
    clear_url = f'{BASE_URL}/clear-process/'
    
    try:
        # Realizar el POST para limpiar el archivo
        clear_response = requests.post(clear_url)
        
        if clear_response.status_code == 200:
            print("\nArchivo process.json limpiado con éxito.")
        else:
            print(f"\nError al limpiar el archivo: {clear_response.status_code} - {clear_response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud para limpiar el archivo: {e}")
