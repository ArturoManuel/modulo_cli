
import requests
from typing import Optional, Dict, Any
from config_backend import autentication

def create_token(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Crea un token para el usuario especificado.

    Args:
        user_id (int): ID del usuario.

    Returns:
        Optional[Dict[str, Any]]: Respuesta de la API con detalles del token o None en caso de error.
    """
    url = f"{autentication}/token/create-token"
    payload = {"user_id": user_id}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred al crear el token: {http_err} - {response.text}")
    except Exception as err:
        print(f"Otro error ocurrió al crear el token: {err}")
    return None

def get_token(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene el token activo para el usuario especificado.

    Args:
        user_id (int): ID del usuario.

    Returns:
        Optional[Dict[str, Any]]: Respuesta de la API con detalles del token o None en caso de error.
    """
    url = f"{autentication}/token/get-token/{user_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred al obtener el token: {http_err} - {response.text}")
    except Exception as err:
        print(f"Otro error ocurrió al obtener el token: {err}")
    return None