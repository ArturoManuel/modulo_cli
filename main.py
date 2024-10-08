
# import random
# import smtplib
# from email.mime.text import MIMEText

# # Lista de correos válidos (hardcodeada por el momento)
# VALID_EMAILS = ['noriegaarturonoriega@gmail.com']

# # Función para generar el token
# def generate_token():
#     return str(random.randint(100000, 999999))

# # Función para enviar el token por correo
# def send_token(email, token):
#     sender = "noriegaarturonoriega2@gmail.com"  # Correo desde el que se envía el token (deberías cambiarlo)
#     msg = MIMEText(f"Tu token de acceso es: {token}")
#     msg['Subject'] = "Token de acceso"
#     msg['From'] = sender
#     msg['To'] = email

#     try:
#         # Configurar el servidor SMTP (aquí se está usando un servidor ficticio, reemplaza con tu configuración)
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()
#             server.login(sender, "edks wbje agoo svwx")  # Reemplaza con la contraseña del remitente
#             server.sendmail(sender, email, msg.as_string())
#         print(f"Token enviado a {email}")
#     except Exception as e:
#         print(f"Error al enviar el correo: {e}")

# # Función para validar el correo
# def validate_email(email):
#     return email in VALID_EMAILS

# # Función para mostrar el menú principal
# def show_menu():
#     print("\n--- Menú de Opciones ---")
#     print("1. Crear nueva VM")
#     print("2. Ver slices activos")
#     print("3. Monitorear recursos del sistema")
#     print("4. Eliminar slice")
#     print("5. Implementar topología predefinida")
#     print("6. Salir")
    
#     option = input("Seleccione una opción: ")
#     return option

# # Función principal
# def main():
#     print("Bienvenido al sistema de gestión de VMs y slices")
    
#     # Solicitar correo
#     email = input("Ingrese su correo: ")
    
#     if not validate_email(email):
#         print("Correo no válido. El acceso está restringido.")
#         return

#     # Generar y enviar token
#     token = generate_token()
#     send_token(email, token)

#     # Solicitar el token ingresado por el usuario
#     user_token = input("Ingrese el token que recibió en su correo: ")
    
#     if user_token == token:
#         print("Token válido. Acceso concedido.")
        
#         # Mostrar menú
#         while True:
#             option = show_menu()
#             if option == '1':
#                 print("Función de creación de nueva VM...")
#             elif option == '2':
#                 print("Mostrando slices activos...")
#             elif option == '3':
#                 print("Monitoreo de recursos del sistema...")
#             elif option == '4':
#                 print("Eliminando slice...")
#             elif option == '5':
#                 print("Implementando topología predefinida...")
#             elif option == '6':
#                 print("Saliendo del sistema...")
#                 break
#             else:
#                 print("Opción no válida. Intente de nuevo.")
#     else:
#         print("Token incorrecto. Acceso denegado.")

# if __name__ == "__main__":
#     main()




from modules.auth import authenticate_user
from modules.menus import execute_menu
from modules.user_roles import get_user_role
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


