# import requests
# from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
# from tqdm import tqdm
# import sys
# from pathlib import Path
# import json
import time

# def list_json_files(directory: str):
#     """
#     Lista todos los archivos .json en el directorio especificado.

#     Args:
#         directory (str): Ruta al directorio que contiene archivos .json.

#     Returns:
#         List[Path]: Lista de rutas a archivos .json.
#     """
#     dir_path = Path(directory)
#     if not dir_path.is_dir():
#         print(f"El directorio especificado no existe: {dir_path}")
#         sys.exit(1)
    
#     json_files = list(dir_path.glob("*.json"))
#     if not json_files:
#         print("No se encontraron archivos .json en el directorio especificado.")
#         sys.exit(1)
    
#     return json_files

# def select_file(files):
#     """
#     Muestra una lista numerada de archivos y permite al usuario seleccionar uno.

#     Args:
#         files (List[Path]): Lista de rutas a archivos.

#     Returns:
#         Path: Ruta al archivo seleccionado.
#     """
#     print("\nArchivos disponibles para importar:")
#     for idx, file in enumerate(files, start=1):
#         print(f"{idx}. {file.name}")
    
#     while True:
#         try:
#             selection = int(input(f"\nIngresa el número del archivo que deseas importar (1-{len(files)}): "))
#             if 1 <= selection <= len(files):
#                 selected_file = files[selection - 1]
#                 print(f"\nSeleccionaste: {selected_file.name}")
#                 return selected_file
#             else:
#                 print(f"Por favor, ingresa un número entre 1 y {len(files)}.")
#         except ValueError:
#             print("Entrada inválida. Por favor, ingresa un número.")

# def load_session(session_file: str):
#     """
#     Carga la información de sesión desde un archivo JSON.

#     Args:
#         session_file (str): Ruta al archivo de sesión JSON.

#     Returns:
#         dict: Datos de sesión.
#     """
#     session_path = Path(session_file)
#     if not session_path.is_file():
#         print(f"El archivo de sesión no existe: {session_path}")
#         sys.exit(1)
    
#     try:
#         with session_path.open('r', encoding='utf-8') as f:
#             session_data = json.load(f)
#         return session_data
#     except json.JSONDecodeError as e:
#         print(f"Error al leer el archivo de sesión JSON: {e}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error al abrir el archivo de sesión: {e}")
#         sys.exit(1)

# def upload_json(file_path: Path, upload_url: str, headers: dict = None):
#     """
#     Sube el archivo JSON especificado al endpoint proporcionado.

#     Args:
#         file_path (Path): Ruta al archivo .json a subir.
#         upload_url (str): URL del endpoint al que se subirá el archivo.
#         headers (dict, optional): Headers adicionales para la solicitud.
#     """
#     # Leer el contenido del archivo JSON
#     try:
#         with file_path.open('r', encoding='utf-8') as f:
#             data = json.load(f)
#     except json.JSONDecodeError as e:
#         print(f"Error al leer el archivo JSON: {e}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Error al abrir el archivo: {e}")
#         sys.exit(1)
    
#     # Enviar la solicitud POST al endpoint
#     try:
#         response = requests.post(upload_url, json=data, headers=headers, timeout=60)
#         response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        
#         # Asumiendo que la respuesta es JSON
#         try:
#             response_data = response.json()
#         except json.JSONDecodeError:
#             response_data = response.text
        
#         print(f"\nPlantilla importada exitosamente. Respuesta del servidor:")
#         print(f"Código de Estado: {response.status_code}")
#         print(f"Contenido: {response_data}")
#         return response_data
#     except requests.exceptions.HTTPError as e:
#         print(f"\nError HTTP al importar la plantilla: {e} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"\nError al realizar la solicitud: {e}")
    
#     return None

# def assign_plantilla_to_user(id_user: int, id_plantillas: str, assign_url: str, headers: dict = None):
#     """
#     Asigna una plantilla a un usuario específico.

#     Args:
#         id_user (int): ID del usuario.
#         id_plantillas (str): ID de la plantilla.
#         assign_url (str): URL del endpoint para asignar la plantilla.
#         headers (dict, optional): Headers adicionales para la solicitud.
#     """
#     payload = {
#         "id_user": id_user,
#         "id_plantillas": id_plantillas
#     }
    
#     try:
#         response = requests.post(assign_url, json=payload, headers=headers, timeout=60)
#         response.raise_for_status()
        
#         # Asumiendo que la respuesta es JSON
#         try:
#             response_data = response.json()
#         except json.JSONDecodeError:
#             response_data = response.text
        
#         print(f"\nPlantilla asignada exitosamente. Respuesta del servidor:")
#         print(f"Código de Estado: {response.status_code}")
#         print(f"Contenido: {response_data}")
#     except requests.exceptions.HTTPError as e:
#         print(f"\nError HTTP al asignar la plantilla: {e} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"\nError al realizar la solicitud: {e}")

# def import_json_template():
#     """
#     Función principal que lista archivos .json, permite al usuario seleccionar uno,
#     lo importa al endpoint y asigna la plantilla al usuario basado en la sesión.
#     """
#     DIRECTORY = r"C:\Users\Arturon\VisualStudioCode\modulo_cli_2\modulo_cli\plantillas"
#     PLANTILLA_UPLOAD_URL = "http://gateway:8001/plantilla"
#     ASSIGN_PLANTILLA_URL = "http://gateway:8001/user_plantillas"
#     SESSION_FILE = r"C:\Users\Arturon\VisualStudioCode\modulo_cli_2\modulo_cli\session_data\session_token2.json"

#     print("=== Importador y Asignador de Plantillas JSON ===")
    
#     # Listar archivos .json
#     json_files = list_json_files(DIRECTORY)
    
#     # Seleccionar archivo
#     selected_file = select_file(json_files)
    
#     # Cargar información de sesión
#     session_data = load_session(SESSION_FILE)
#     id_user = session_data.get("id")
#     if not id_user:
#         print("El archivo de sesión no contiene 'id' del usuario.")
#         sys.exit(1)
    
#     # Preparar headers con tokens si es necesario
#     # Supongamos que necesitas usar 'access_token_deployment' para autenticar
#     access_token = session_data.get("access_token_deployment")
#     headers = {}
#     if access_token:
#         headers["Authorization"] = f"Bearer {access_token}"
    
#     # Confirmar antes de importar
#     confirm = input(f"\n¿Deseas importar la plantilla '{selected_file.name}'? (s/n): ").strip().lower()
#     if confirm != 's':
#         print("Importación cancelada por el usuario.")
#         sys.exit(0)
    
#     # Importar plantilla
#     response_data = upload_json(selected_file, PLANTILLA_UPLOAD_URL, headers=headers)
#     if not response_data:
#         print("No se pudo importar la plantilla.")
#         sys.exit(1)
    
#     plantilla_id = response_data.get("id")
#     if not plantilla_id:
#         print("La respuesta del servidor no contiene el 'id' de la plantilla.")
#         sys.exit(1)
    
#     # Asignar plantilla al usuario
#     print(f"\nAsignando la plantilla ID {plantilla_id} al usuario ID {id_user}...")
#     assign_plantilla_to_user(id_user, plantilla_id, ASSIGN_PLANTILLA_URL, headers=headers)

#     print("\nSubida completada. La pantalla se limpiará en 5 segundos.")
#     time.sleep(5)



import requests
from tqdm import tqdm
import sys
from pathlib import Path
import json
import argparse

def list_json_files(directory: str):
    """
    Lista todos los archivos .json en el directorio especificado.

    Args:
        directory (str): Ruta al directorio que contiene archivos .json.

    Returns:
        List[Path]: Lista de rutas a archivos .json.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"El directorio especificado no existe: {dir_path}")
        sys.exit(1)
    
    json_files = list(dir_path.glob("*.json"))
    if not json_files:
        print("No se encontraron archivos .json en el directorio especificado.")
        sys.exit(1)
    
    return json_files

def select_file(files):
    """
    Muestra una lista numerada de archivos y permite al usuario seleccionar uno.

    Args:
        files (List[Path]): Lista de rutas a archivos.

    Returns:
        Path: Ruta al archivo seleccionado.
    """
    print("\nArchivos disponibles para importar:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file.name}")
    
    while True:
        try:
            selection = int(input(f"\nIngresa el número del archivo que deseas importar (1-{len(files)}): "))
            if 1 <= selection <= len(files):
                selected_file = files[selection - 1]
                print(f"\nSeleccionaste: {selected_file.name}")
                return selected_file
            else:
                print(f"Por favor, ingresa un número entre 1 y {len(files)}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def load_session(session_file: str):
    """
    Carga la información de sesión desde un archivo JSON.

    Args:
        session_file (str): Ruta al archivo de sesión JSON.

    Returns:
        dict: Datos de sesión.
    """
    session_path = Path(session_file)
    if not session_path.is_file():
        print(f"El archivo de sesión no existe: {session_path}")
        sys.exit(1)
    
    try:
        with session_path.open('r', encoding='utf-8') as f:
            session_data = json.load(f)
        return session_data
    except json.JSONDecodeError as e:
        print(f"Error al leer el archivo de sesión JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al abrir el archivo de sesión: {e}")
        sys.exit(1)

def upload_json(file_path: Path, upload_url: str, headers: dict = None):
    """
    Sube el archivo JSON especificado al endpoint proporcionado.

    Args:
        file_path (Path): Ruta al archivo .json a subir.
        upload_url (str): URL del endpoint al que se subirá el archivo.
        headers (dict, optional): Headers adicionales para la solicitud.

    Returns:
        dict or None: Datos de la respuesta JSON si la solicitud es exitosa, de lo contrario None.
    """
    # Leer el contenido del archivo JSON
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error al leer el archivo JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        sys.exit(1)
    
    # Enviar la solicitud POST al endpoint
    try:
        response = requests.post(upload_url, json=data, headers=headers, timeout=60)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        
        # Asumiendo que la respuesta es JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = response.text
        
        print(f"\nPlantilla importada exitosamente. Respuesta del servidor:")
        print(f"Código de Estado: {response.status_code}")
        print(f"Contenido: {response_data}")
        return response_data
    except requests.exceptions.HTTPError as e:
        print(f"\nError HTTP al importar la plantilla: {e} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nError al realizar la solicitud: {e}")
    
    return None

def assign_plantilla_to_user(id_user: int, id_plantillas: str, assign_url: str, headers: dict = None):
    """
    Asigna una plantilla a un usuario específico.

    Args:
        id_user (int): ID del usuario.
        id_plantillas (str): ID de la plantilla.
        assign_url (str): URL del endpoint para asignar la plantilla.
        headers (dict, optional): Headers adicionales para la solicitud.
    """
    payload = {
        "id_user": id_user,
        "id_plantillas": id_plantillas
    }
    
    try:
        response = requests.post(assign_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        # Asumiendo que la respuesta es JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = response.text
        
        print(f"\nPlantilla asignada exitosamente. Respuesta del servidor:")
        print(f"Código de Estado: {response.status_code}")
        print(f"Contenido: {response_data}")
    except requests.exceptions.HTTPError as e:
        print(f"\nError HTTP al asignar la plantilla: {e} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nError al realizar la solicitud: {e}")

def deploy_topology(json_data: dict, deploy_linux_url: str, deploy_openstack_url: str, headers: dict = None):
    """
    Despliega la topología utilizando el endpoint correspondiente basado en el servicio.

    Args:
        json_data (dict): JSON importado que describe la topología.
        deploy_linux_url (str): URL del endpoint para desplegar en Linux.
        deploy_openstack_url (str): URL del endpoint para desplegar en OpenStack.
        headers (dict, optional): Headers adicionales para la solicitud.
    """
    servicio = json_data.get("servicio", "").lower()
    if servicio == "linux":
        deploy_url = deploy_linux_url
        servicio_desc = "Linux"
    elif servicio == "openstack":
        deploy_url = deploy_openstack_url
        servicio_desc = "OpenStack"
    else:
        print(f"Servicio '{servicio}' no reconocido. No se puede desplegar.")
        return
    
    print(f"\nDesplegando topología para el servicio: {servicio_desc}...")
    
    try:
        response = requests.post(deploy_url, json=json_data, headers=headers, timeout=120)
        response.raise_for_status()
        
        # Asumiendo que la respuesta es JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = response.text
        
        print(f"\nDespliegue completado exitosamente. Respuesta del servidor:")
        print(f"Código de Estado: {response.status_code}")
        print(f"Contenido: {response_data}")
    except requests.exceptions.HTTPError as e:
        print(f"\nError HTTP al desplegar la topología: {e} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nError al realizar la solicitud: {e}")

def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.

    Returns:
        Namespace: Objeto con los argumentos.
    """
    parser = argparse.ArgumentParser(description="Importa, asigna y despliega plantillas JSON.")
    parser.add_argument("--directory", type=str, default=r"C:\Users\Arturon\VisualStudioCode\modulo_cli_2\modulo_cli\plantillas",
                        help="Ruta al directorio que contiene plantillas JSON.")
    parser.add_argument("--session_file", type=str, default=r"C:\Users\Arturon\VisualStudioCode\modulo_cli_2\modulo_cli\session_data\session_token2.json",
                        help="Ruta al archivo de sesión JSON.")
    parser.add_argument("--plantilla_url", type=str, default="http://gateway:8001/plantilla",
                        help="URL del endpoint para subir plantillas.")
    parser.add_argument("--assign_url", type=str, default="http://gateway:8001/user_plantillas",
                        help="URL del endpoint para asignar plantillas a usuarios.")
    parser.add_argument("--deploy_linux_url", type=str, default="http://gateway:8002/deploy_linux",
                        help="URL del endpoint para desplegar en Linux.")
    parser.add_argument("--deploy_openstack_url", type=str, default="http://gateway:8002/deploy_openstack",
                        help="URL del endpoint para desplegar en OpenStack.")
    return parser.parse_args()

def import_and_deploy(args):
    """
    Función principal que importa plantillas, asigna al usuario y opcionalmente despliega la topología.

    Args:
        args (Namespace): Argumentos de línea de comandos.
    """
    print("=== Importador, Asignador y Despliegue de Plantillas JSON ===")
    
    # Listar archivos .json
    json_files = list_json_files(args.directory)
    
    # Seleccionar archivo
    selected_file = select_file(json_files)
    
    # Cargar información de sesión
    session_data = load_session(args.session_file)
    id_user = session_data.get("id")
    if not id_user:
        print("El archivo de sesión no contiene 'id' del usuario.")
        sys.exit(1)
    
    # Preparar headers con tokens si es necesario
    access_token = session_data.get("access_token_deployment")
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    # Confirmar antes de importar
    confirm = input(f"\n¿Deseas importar la plantilla '{selected_file.name}'? (s/n): ").strip().lower()
    if confirm != 's':
        print("Importación cancelada por el usuario.")
        sys.exit(0)
    
    # Importar plantilla
    response_data = upload_json(selected_file, args.plantilla_url, headers=headers)
    if not response_data:
        print("No se pudo importar la plantilla.")
        sys.exit(1)
    
    plantilla_id = response_data.get("id")
    if not plantilla_id:
        print("La respuesta del servidor no contiene el 'id' de la plantilla.")
        sys.exit(1)
    
    # Asignar plantilla al usuario
    print(f"\nAsignando la plantilla ID {plantilla_id} al usuario ID {id_user}...")
    assign_plantilla_to_user(id_user, plantilla_id, args.assign_url, headers=headers)
    
    # Leer el archivo JSON para obtener "servicio"
    try:
        with selected_file.open('r', encoding='utf-8') as f:
            plantilla_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error al leer el archivo JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        sys.exit(1)
    
    servicio = plantilla_data.get("servicio", "").lower()
    if not servicio:
        print("El archivo JSON no contiene el campo 'servicio'.")
        sys.exit(1)
    
    # Preguntar si desea desplegar la topología
    deploy_confirm = input(f"\n¿Deseas desplegar la topología '{plantilla_data.get('nombre', 'N/A')}'? (s/n): ").strip().lower()
    if deploy_confirm != 's':
        print("Despliegue cancelado por el usuario.")
        sys.exit(0)
    
    # Desplegar topología
    deploy_topology(
        json_data=plantilla_data,
        deploy_linux_url=args.deploy_linux_url,
        deploy_openstack_url=args.deploy_openstack_url,
        headers=headers
    )
    print("\nSubida completada. La pantalla se limpiará en 10 segundos.")
    time.sleep(10)