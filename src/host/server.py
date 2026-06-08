import socket, requests, threading
from src import console, packet, tag
from src.host import message, var
from src.crypto import crypto_main

Server: bool = False
clients = [] # Connected clients list
bans = [] # Banned clients list
mutes = [] # Muted clients list
server_sock = None

def getUserName(ip):
     for c in clients:
          if ip == c['ip']:
               return c['name']
          else:
               print(f'{tag.warning}Error to get username from client list')

def NameToIP(username: str): 
     for c in clients:
          if username == c['name']:
               return c['ip'][0] 
     return None
     
class Punishment:
     @staticmethod
     def _apply_punishment_(username: str, reason: str, array: list, punishment: str):
          userIP = NameToIP(username)
          if userIP is not None:
               array.append(userIP)
               match punishment:
                    case "ban":
                         packet.SendVisualMessage(f"{tag.info}You have banned {username} (IP: {userIP}). Reason: {reason}.  {username}'s IP: {NameToIP(username)}")
                         packet.SendServer(f"{var.server_send_ban + username}")
                    case "mute":
                         packet.SendVisualMessage(f"{tag.info}You have muted {username} (IP: {userIP}). Reason: {reason}. {username}'s IP: {NameToIP(username)}")
                         packet.SendServer(f"{var.server_send_mute + username}")
          else:
               packet.SendVisualMessage(f"{tag.warning}IP of {username} was not found.")

     @staticmethod
     def Ban(username: str, reason: str = "No reason"):
          Punishment._apply_punishment_(username, reason, bans, "ban")

     @staticmethod
     def Mute(username: str, reason: str = "No reason"):
          Punishment._apply_punishment_(username, reason, mutes, "mute")

def RunServer():
     global server_sock, Server

     Server = True
     server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     server_sock.settimeout(0.5)
     server_sock.bind(("0.0.0.0", packet.port))
     
     # port.open_port(packet.port) # I think qChat doesn't need it
     
     console.clear()
     public_ip = requests.get('https://api.ipify.org').text
     print(f"{tag.success}You launched a server. Your IP to connect: {public_ip} | Port: {packet.port}") # \nPress {control.server_exit_button} to shutdown the server.
     
     crypto_main.generateRoomKey()
     threading.Thread(target=message.RecieveHandler, daemon=True, args=(True,)).start()
     message.MessageHandler()