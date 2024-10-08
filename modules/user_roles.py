# Lista de correos válidos y sus roles
USERS = {
    'jesus.idrogo@pucp.edu.pe':'user',
    'noriegaarturonoriega@gmail.com': 'user',
    'a20190411@pucp.edu.pe': 'admin'  
}

import requests
from config_backend import API_URL
from urllib.parse import quote

# Función para validar el correo
def validate_email(email: str):
    print(email)
    url = f"{API_URL}/users/validate-email/"
    
    # No necesitas codificar el email manualmente
    params = {"email": email}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return True  # El correo está registrado
        elif response.status_code == 404:
            print("Correo no registrado")
            return False  # El correo no está registrado
        else:
            print(f"Error del servidor: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error conectando al backend: {e}")
        return False
        
# Función para obtener el rol del usuario
def get_user_role(username, password):
    url = f"{API_URL}/users/login/"
    payload = {"username": username, "password": password}

    try:
        response = requests.post(url, json=payload)  # Realiza la solicitud POST al backend
        if response.status_code == 200:
            data = response.json()  # Decodifica la respuesta
            return data["user"]["rol"]  # Retorna el rol del usuario
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error conectando al backend: {e}")
        return None
