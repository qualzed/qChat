import socket, time, threading
from src.host import message
from src import user, packet
from src.crypto import key_generation, crypto_main

Client = False

def SetClientMode():
     global Client

     toConnectIP = input("Enter IP to connect: ")
     toConnectPort = input("Enter Port to connect: ")
     if toConnectIP:
          Client = True
          packet.server_port = int(toConnectPort)
          RunClient(toConnectIP) # 18.05.2026 | Bad way to fix it

def RunClient(IP: str = "127.0.0.1"):
     try:
          global client_sock, server_addr
          
          client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          client_sock.bind(("0.0.0.0", packet.port)) # If you run it for tests - just change this port
          server_addr = (IP, packet.server_port)
          
          client_sock.sendto(f"{user.NAME} has been connected".encode(), server_addr)
          client_sock.sendto(f"$nm:{user.NAME}".encode(), server_addr)

          crypto_main.generateDHKeys()
          threading.Thread(target=message.RecieveHandler, daemon=True, args=(True,)).start()
          message.MessageHandler()
     except Exception as e:
          print(e)
          time.sleep(5)
          exit(0)