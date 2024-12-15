import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import sys
import os

def progress_callback(monitor):
    progress_bar.update(monitor.bytes_read - progress_callback.last_bytes)
    progress_callback.last_bytes = monitor.bytes_read

# Ruta al archivo que deseas subir
file_path = r"C:\Users\Arturon\OneDrive\Escritorio\Imagenes\focal-server-cloudimg-amd64.img"
url = "http://gateway:8002/upload-file/"

# Asegúrate de que el archivo existe
if not os.path.isfile(file_path):
    print("El archivo especificado no existe.")
    sys.exit(1)

with open(file_path, "rb") as file:
    encoder = MultipartEncoder(
        fields={"file": (os.path.basename(file_path), file, "application/x-iso9660-image")}
    )

    progress_bar = tqdm(total=encoder.len, unit='B', unit_scale=True, desc="Subiendo archivo")
    progress_callback.last_bytes = 0

    monitor = MultipartEncoderMonitor(encoder, progress_callback)

    try:
        response = requests.post(
            url,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
            timeout=600  # Aumenta el tiempo de espera si es necesario
        )
        progress_bar.close()
        print("\nRespuesta del servidor:", response.status_code, response.json())
    except requests.exceptions.RequestException as e:
        progress_bar.close()
        print(f"\nError al subir el archivo: {e}")
