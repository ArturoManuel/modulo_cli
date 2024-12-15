import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import sys

import time
from pathlib import Path
import json

def list_img_files(directory: str):
    """
    Lista todos los archivos .img en el directorio especificado.

    Args:
        directory (str): Ruta al directorio que contiene archivos .img.

    Returns:
        List[Path]: Lista de rutas a archivos .img.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"El directorio especificado no existe: {dir_path}")
        sys.exit(1)
    
    img_files = list(dir_path.glob("*.img"))
    if not img_files:
        print("No se encontraron archivos .img en el directorio especificado.")
        sys.exit(1)
    
    return img_files


def upload_file(file_path: Path, upload_url: str):
    """
    Sube el archivo especificado al endpoint proporcionado con una barra de progreso.

    Args:
        file_path (Path): Ruta al archivo a subir.
        upload_url (str): URL del endpoint al que se subirá el archivo.
    """
    def progress_callback(monitor):
        progress_bar.update(monitor.bytes_read - progress_callback.last_bytes)
        progress_callback.last_bytes = monitor.bytes_read

    try:
        with file_path.open("rb") as file:
            encoder = MultipartEncoder(
                fields={"file": (file_path.name, file, "application/x-iso9660-image")}
            )

            progress_bar = tqdm(total=encoder.len, unit='B', unit_scale=True, desc="Subiendo archivo")
            progress_callback.last_bytes = 0

            monitor = MultipartEncoderMonitor(encoder, progress_callback)

            response = requests.post(
                upload_url,
                data=monitor,
                headers={"Content-Type": monitor.content_type},
                timeout=600  # Ajusta el tiempo de espera según sea necesario
            )
            progress_bar.close()
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            print("\nRespuesta del servidor:", response.status_code, response.json())
    except requests.exceptions.RequestException as e:
        progress_bar.close()
        print(f"\nError al subir el archivo: {e}")

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


def upload_selected_image():
    """
    Función principal que lista archivos .img, permite al usuario seleccionar uno y lo sube al endpoint.
    """
    DIRECTORY = r"C:/Users/Arturon/VisualStudioCode/modulo_cli_2/modulo_cli/imagenes"
    UPLOAD_URL = "http://gateway:8002/upload-file/"

    print("=== CLI de Subida de Archivos .img ===")

    # Listar archivos .img
    img_files = list_img_files(DIRECTORY)

    # Seleccionar archivo
    selected_file = select_file(img_files)

    # Confirmar antes de subir
    confirm = input(f"\n¿Deseas subir el archivo '{selected_file.name}'? (s/n): ").strip().lower()
    if confirm != 's':
        print("Subida cancelada por el usuario.")
        sys.exit(0)

    # Subir archivo
    upload_file(selected_file, UPLOAD_URL)
    print("\nSubida completada. La pantalla se limpiará en 20 segundos.")
    time.sleep(20)