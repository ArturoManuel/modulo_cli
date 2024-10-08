import random
from modules.email_service import send_token
from modules.user_roles import validate_email ,get_user_role



# Función para generar el token
def generate_token():
    return str(random.randint(100000, 999999))

# Función de autenticación del usuario
def authenticate_user(email):
    if not validate_email(email):
        # Si el correo no es válido, no proceder
        print("Correo no válido o no registrado. El acceso está restringido.")
        return None, False

    # Generar y enviar token
    token = generate_token()
    send_token(email, token)

    # Solicitar el token ingresado por el usuario
    user_token = input("Ingrese el token que recibió en su correo: ")

    if user_token == token:
        # Solicitar nombre de usuario y contraseña
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")

        # Obtener el rol del usuario desde el backend
        role = get_user_role(username, password)

        if role:
            return role, True  # Retorna el rol y True si la autenticación fue exitosa
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            return None, False
    else:
        print("Token incorrecto.")
        return None, False

