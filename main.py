
from modules.authetication.auth import authenticate_user
from modules.menus.menus import execute_menu
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Bienvenido al sistema de gestión de VMs y slices")

    while True:
        # Autenticación y obtención de token
        email = input("Ingrese su correo: ")
        print(f"Correo ingresado: {email}")
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
    main()


