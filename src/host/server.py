import socket, requests, keyboard, threading
from src import console, port, control, user, packet, tag
from src.host import message, server, client

Server: bool = False
clients = [] # Connected clients list
server_sock = None

def getUserName(ip):
     for c in clients:
          if ip == c['ip']:
               return c['name']
          else:
               print(f'{tag.warning}Error to get username from client list')

def NameToIP(name: str): # This function will return IP if user with given name is found
     for c in clients:
          if name == c['name']:
               receiver_ip = c['ip']
               return receiver_ip

def RunServer():
     global server_sock, Server

     Server = True
     server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     server_sock.bind(("0.0.0.0", packet.port))
     
     # port.open_port(packet.port) # I think qChat doesn't need it
     
     console.clear()
     public_ip = requests.get('https://api.ipify.org').text
     print(f"{tag.success}You launched a server. Your IP to connect: {public_ip} | Port: {packet.port}") # \nPress {control.server_exit_button} to shutdown the server.
     
     threading.Thread(target=message.RecieveHandler, daemon=True).start()
     message.MessageHandler()