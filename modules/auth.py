import random
from modules.email_service import send_token
from modules.user_roles import validate_email ,get_user_role

# Función para generar el token
def generate_token():
    return str(random.randint(100000, 999999))

# Función de autenticación del usuario
def authenticate_user(email):
    if not validate_email(email):
        print("Correo no válido. El acceso está restringido.")
        return None, False

    # Generar y enviar token
    token = generate_token()
    send_token(email, token)

    # Solicitar el token ingresado por el usuario
    user_token = input("Ingrese el token que recibió en su correo: ")
    
    if user_token == token:
        return get_user_role(email), True
    else:
        print("Token incorrecto.")
        return None, False
