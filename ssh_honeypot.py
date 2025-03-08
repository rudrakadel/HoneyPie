# Import library dependencies.
import logging
from logging.handlers import RotatingFileHandler
import paramiko
import threading
import socket
import time
from pathlib import Path

# Constants.
SSH_BANNER = "SSH-2.0-MySSHServer_1.0"
server_key = "C:/Users/Public/Github/HoneyPie/static/server.key"
creds_log_path = "C:/Users/Public/Github/HoneyPie/log_files/creds_audit.log"
cmd_log_path = "C:/Users/Public/Github/HoneyPie/log_files/funnel_audit.log"

# SSH Server Host Key.
host_key = paramiko.RSAKey(filename=server_key)

# Logging Format.
logging_format = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Funnel Logger (Captures all executed commands).
funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler(cmd_log_path, maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

# Credentials Logger (Captures login attempts).
creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler(creds_log_path, maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)

class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
    
    def get_allowed_auths(self, username):
        return "password"

    def check_auth_password(self, username, password):
        creds_logger.info(f'[{self.client_ip}] - Username: {username} | Password: {password}')
        if self.input_username and self.input_password:
            return paramiko.AUTH_SUCCESSFUL if username == self.input_username and password == self.input_password else paramiko.AUTH_FAILED
        return paramiko.AUTH_SUCCESSFUL
    
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        return True

def emulated_shell(channel, client_ip):
    channel.send(b"root@debian-server:$ ")
    command = b""
    while True:  
        char = channel.recv(1)
        channel.send(char)
        if not char:
            channel.close()

        command += char
        if char == b"\r":
            cmd = command.strip().decode()
            if cmd == "exit":
                response = b"\nGoodbye!\n"
                channel.close()
            elif cmd == "pwd":
                response = b"\n/usr/local\r\n"
            elif cmd == "whoami":
                response = b"\nroot\r\n"
            elif cmd == "ls":
                response = b"\npasswords_backup.config\r\n"
            elif cmd == "cat passwords_backup.config":
                response = b"\nadmin:Admin123!\nroot:toor\nservice:service@123\r\n"
            else:
                response = f"\nbash: {cmd}: command not found\r\n".encode()
            
            funnel_logger.info(f'[{client_ip}] Executed: {cmd}')
            channel.send(response)
            channel.send(b"root@debian-server:$ ")
            command = b""

def client_handle(client, addr, username, password, tarpit=False):
    client_ip = addr[0]
    print(f"{client_ip} connected to server.")
    try:
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip=client_ip, input_username=username, input_password=password)
        transport.add_server_key(host_key)
        transport.start_server(server=server)
        channel = transport.accept(100)
        if channel is None:
            print("No channel was opened.")
        
        banner = "Welcome to Debian 11 (Bullseye) Secure SSH Server!\r\n\r\n"
        if tarpit:
            for char in banner * 100:
                channel.send(char)
                time.sleep(8)
        else:
            channel.send(banner.encode())
        
        emulated_shell(channel, client_ip)
    except Exception as error:
        print(error)
    finally:
        try:
            transport.close()
        except Exception:
            pass
        client.close()

def honeypot(address, port, username, password, tarpit=False):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    socks.listen(100)
    print(f"SSH server is listening on port {port}.")
    while True: 
        try:
            client, addr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password, tarpit))
            ssh_honeypot_thread.start()
        except Exception as error:
            print("!!! Exception - Could not open new client connection !!!")
            print(error)

honeypot('127.0.0.1', 2222, username=None, password=None, tarpit=False)
