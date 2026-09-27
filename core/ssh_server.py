"""
CHIMERA - Core SSH Honeypot Server
Simulates a vulnerable SSH server using Paramiko.
Accepts any username/password and drops the attacker into a fake shell.
"""

import socket
import threading
import paramiko
import logging
from datetime import datetime

# ---------- Basic Logging Setup ----------
logging.basicConfig(
    filename="logs/chimera.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

HOST_KEY = paramiko.RSAKey.generate(2048)  # مفتاح مؤقت، هنثبته بملف لاحقًا
SERVER_PORT = 2222


class ChimeraSSHServer(paramiko.ServerInterface):
    """Handles authentication and channel requests for the fake SSH server."""

    def __init__(self, client_ip):
        self.event = threading.Event()
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        # نقبل أي يوزر/باسورد عشان نجذب المهاجم (زي أي هوني بوت حقيقي)
        logging.info(f"[{self.client_ip}] Login attempt -> user: {username} | pass: {password}")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


def handle_connection(client_socket, client_ip):
    """Handles a single incoming SSH connection."""
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(HOST_KEY)

        server = ChimeraSSHServer(client_ip)
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            logging.warning(f"[{client_ip}] No channel established.")
            return

        server.event.wait(10)
        channel.send("Welcome to svr-prod-04\r\n")

        session_active = True

        while session_active:
            channel.send("root@svr-prod-04:~# ")
            command = ""

            while True:
                char = channel.recv(1).decode("utf-8", errors="ignore")
                if not char:
                    session_active = False
                    break
                if char in ("\r", "\n"):
                    channel.send("\r\n")
                    break
                if char == "\x7f":  # Backspace
                    command = command[:-1]
                    continue
                command += char
                channel.send(char)  # echo يوضح الكتابة للمهاجم

            command = command.strip()

            if not command:
                continue

            logging.info(f"[{client_ip}] CMD: {command}")

            if command.lower() in ("exit", "quit", "logout"):
                channel.send("logout\r\n")
                session_active = False
                break
            else:
                # مؤقتًا: رد ثابت بسيط، هنستبدله بـ LLM في الملف الجاي
                channel.send(f"bash: {command.split()[0]}: command not found\r\n")

        channel.close()
        transport.close()

    except Exception as e:
        logging.error(f"[{client_ip}] Error: {e}")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", SERVER_PORT))
    server_socket.listen(100)

    print(f"[CHIMERA] Listening on port {SERVER_PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        client_ip = addr[0]
        print(f"[+] New connection from {client_ip}")
        thread = threading.Thread(target=handle_connection, args=(client_socket, client_ip))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    start_server()
