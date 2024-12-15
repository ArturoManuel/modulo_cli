
from modules.authetication.auth import authenticate_user
from modules.menus.menus import execute_menu
from modules.token.utils import load_token,save_token,delete_token,load2_token
from modules.token.route import get_token
import os
import signal
import sys
from pyfiglet import Figlet
import getpass
import msvcrt


def signal_handler(sig, frame):
    print('Se ha detectado Control+C! Terminando la aplicación...')
    sys.exit(0)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

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


def main():
    
    f = Figlet(font='slant')
    print (f.renderText('Cloud Resources'))



    if load_token() and load2_token():
        token_data = load_token()
        session_data =load2_token()
        user_id = token_data.get("user_id")
        token = token_data.get("token")
        print(f"Token encontrado para el usuario {user_id}. Verificando validez...")
        print(session_data)
        role ='user'
        # Obtener el token activo desde la API
        response = get_token(user_id)
        if response:
            if response["status"] and response["expires_at"] > response["created_at"]:
                print("Token válido encontrado. Accediendo directamente...")
                
                execute_menu(role)
                print(f"Token: {response['token']}")
                sys.exit(0)
            else:
                print("El token ha expirado o es inválido. Necesitas iniciar sesión nuevamente.")
                delete_token()
        else:
            print("No se pudo verificar el token. Intenta iniciar sesión nuevamente.")


    while True:        
        email = masked_input("Ingrese su correo: ")
        role, is_authenticated = authenticate_user(email)

        if is_authenticated:
            print("Acceso concedido.")
            # Ejecutar el menú adecuado según el rol
            execute_menu(role)
            break  # Salir del bucle una vez autenticado correctamente
        else:
            print("Acceso denegado. Verifique su correo o token.")
            input("Presione Enter para intentarlo de nuevo...")
            clear_terminal()  # Limpiar la terminal después de cada intento fallido


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()


