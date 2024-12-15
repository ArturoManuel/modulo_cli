import random
import msvcrt
import sys
from modules.authetication.email_service import send_token
from modules.authetication.user_roles import validate_email ,get_user_role






# Función para generar el token
def generate_token():
    return str(random.randint(100000, 999999))

def masked_input(prompt=""):
    print(prompt, end="", flush=True)
    input_data = []
    while True:
        char = msvcrt.getch()  # Captura una tecla

        if char in {b'\r', b'\n'}:  # Si presiona Enter, termina la entrada
            print()  # Salta a la siguiente línea
            break
        elif char == b'\x08':  # Si presiona Backspace
            if input_data:  # Elimina el último carácter si existe
                input_data.pop()
                sys.stdout.write('\b \b')  # Borra el último asterisco en la terminal
                sys.stdout.flush()
        else:
            input_data.append(char.decode('utf-8'))  # Agrega el carácter a la lista
            sys.stdout.write('*')  # Muestra un asterisco
            sys.stdout.flush()

    return ''.join(input_data) 




# Función de autenticación del usuario
def authenticate_user(email):
    # Validar el correo y obtener el username
    is_registered, username = validate_email(email)
    
    if not is_registered:
        # Si el correo no es válido o no registrado, no proceder
        print("Correo no válido o no registrado. El acceso está restringido.")
        return None, False

    # Generar y enviar token, ahora con el username
    token = generate_token()
    send_token(email, token, username)  # Pasar también el username a send_token

    # Solicitar el token ingresado por el usuario
    user_token = input("Ingrese el token que recibió en su correo: ")

    if user_token == token:
        # Solicitar nombre de usuario y contraseña
        input_username = input("Ingrese su nombre de usuario: ")
        password = masked_input("Ingrese su contraseña: ")

        # Obtener el rol del usuario desde el backend
        role = get_user_role(input_username, password)

        if role:
            return role, True   # Retorna el rol y True si la autenticación fue exitosa
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            return None, False 
    else:
        print("Token incorrecto.")
        return None, False


