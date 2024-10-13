from config_backend import monitoreo_recuros as BASE_URL
import requests
import pandas as pd
import json
from modules.authetication.user_roles import session_data

def get_vm_stats(ip):
    url = f"{BASE_URL}/system-stats"
    
    # Obtener el token de monitoreo de recursos desde session_data
    token = session_data.get('access_token_monitoreo')

    # Si el token no está disponible, lanza un error
    if not token:
        print("Error: No se encontró el token de monitoreo en session_data.")
        return

    # Agregar el token al encabezado de autorización
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    data = {"ip": ip}

    try:
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
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión: {e}")

    input("Presione Enter para continuar...")