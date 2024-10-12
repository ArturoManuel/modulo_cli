import threading
import subprocess
import paramiko
import socket
import select
import os
import sys

def create_ssh_tunnel(ssh_host, ssh_port, ssh_user, ssh_password, local_ports, remote_host, remote_ports):
    try:
        # Configurar la conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Conectando a {ssh_user}@{ssh_host}:{ssh_port}...")

        client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)
        transport = client.get_transport()
        if transport is None:
            print("Error al obtener el transporte SSH.")
            return

        # Crear y gestionar los sockets para los puertos locales
        sockets = []
        for local_port, remote_port in zip(local_ports, remote_ports):
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            local_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            local_socket.bind(('localhost', local_port))
            local_socket.listen(1)
            sockets.append((local_socket, remote_port))

        print(f"Túneles SSH establecidos en los puertos locales {local_ports}...")

        # Mantener los túneles activos esperando conexiones
        while True:
            readable, _, _ = select.select([s[0] for s in sockets], [], [])
            client_socket, addr = readable[0].accept()
            print(f"Conexión recibida desde {addr}")

            # Buscar el puerto remoto correspondiente
            for s, remote_port in sockets:
                if s.getsockname() == client_socket.getsockname():
                    break

            # Abrir un canal hacia el puerto remoto
            channel = transport.open_channel('direct-tcpip', (remote_host, remote_port), addr)
            if channel is None:
                print("No se pudo abrir el canal.")
                client_socket.close()
                continue

            # Conectar el canal al socket local
            try:
                while True:
                    readable, _, _ = select.select([client_socket, channel], [], [])
                    if client_socket in readable:
                        data = client_socket.recv(1024)
                        if len(data) == 0:
                            break
                        channel.send(data)
                    if channel in readable:
                        data = channel.recv(1024)
                        if len(data) == 0:
                            break
                        client_socket.send(data)
            finally:
                channel.close()
                client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Conexión SSH cerrada.")

def run_main():
    """Ejecuta el script main.py en un proceso separado."""
    try:
        print("Iniciando la aplicación...")
        subprocess.run([sys.executable, 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar main.py: {e}")

if __name__ == "__main__":
    # Datos de conexión SSH
    ssh_host = "10.20.12.183"
    ssh_port = 5800
    ssh_user = "ubuntu"
    ssh_password = "20190411"

    # Puertos locales y remotos
    local_ports = [8000, 8001]  # Autenticación y Slice Manager
    remote_ports = [8000, 8001]

    # Crear un hilo para la conexión SSH
    tunnel_thread = threading.Thread(
        target=create_ssh_tunnel,
        args=(ssh_host, ssh_port, ssh_user, ssh_password, local_ports, "localhost", remote_ports),
        daemon=True
    )

    # Iniciar el hilo del túnel SSH
    tunnel_thread.start()

    # Ejecutar main.py en el proceso principal
    run_main()
