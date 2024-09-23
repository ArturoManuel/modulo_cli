# Lista de correos válidos y sus roles
USERS = {
    'noriegaarturonoriega@gmail.com': 'user',
    'a20190411@pucp.edu.pe': 'admin'  # Supuesto correo del admin
}

# Función para validar el correo
def validate_email(email):
    return email in USERS

# Función para obtener el rol del usuario
def get_user_role(email):
    return USERS.get(email)
