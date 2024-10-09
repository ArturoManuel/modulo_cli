import requests
from config_backend import autentication
from urllib.parse import quote

# Función para validar el correo
def validate_email(email: str):
    url = f"{autentication}/users/validate-email/"
    
    # No necesitas codificar el email manualmente
    params = {"email": email}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Procesar la respuesta JSON del servidor
            data = response.json()
            if data.get("exists"):
                username = data.get("username")
                print(f"Correo registrado. Username: {username}")
                return True, username  # Devolver True y el username
        elif response.status_code == 404:
            print("Correo no registrado")
            return False, None  # El correo no está registrado, sin username
        else:
            print(f"Error del servidor: {response.status_code}")
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"Error conectando al backend: {e}")
        return False, None

        
# Función para obtener el rol del usuario

session_data={}
def get_user_role(username, password):
    url = f"{autentication}/users/login/"
    payload = {"username": username, "password": password}

    try:
        response = requests.post(url, json=payload)  # Realiza la solicitud POST al backend
        if response.status_code == 200:
            data = response.json()  # Decodifica la respuesta
            
            session_data['id'] = data['user']['id']
            session_data['username'] = data['user']['username']
            session_data['rol'] = data['user']['rol']

            print("Sesión iniciada con éxito.")
            return data['user']['rol']  # Retorna el rol del usuario
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error conectando al backend: {e}")
        return None