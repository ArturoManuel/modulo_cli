
import json
import os
import sys
from typing import Optional

TOKEN_FILE = 'C:/Users/Arturon/VisualStudioCode/modulo_cli_2/modulo_cli/session_data/session_token.json'
SESSION_FILE ='C:/Users/Arturon/VisualStudioCode/modulo_cli_2/modulo_cli/session_data/session_token2.json'



def save2_token(data: dict):
    """
    Guarda el token en un archivo local.

    Args:
        data (dict): Datos del token a guardar.
    """
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def save_token(data: dict):
    """
    Guarda el token en un archivo local.

    Args:
        data (dict): Datos del token a guardar.
    """
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def load_token() -> Optional[dict]:
    """
    Carga el token desde el archivo local.

    Returns:
        Optional[dict]: Datos del token o None si no existe.
    """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

def load2_token() -> Optional[dict]:
    """
    Carga el token desde el archivo local.

    Returns:
        Optional[dict]: Datos del token o None si no existe.
    """
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def delete_token():
    """
    Elimina el archivo del token local.
    """
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)