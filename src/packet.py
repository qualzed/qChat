import time
from src.host import client, server, var
from src import user

packetSize = 4096 # Bytes
port = 5005 # Default port
server_port = 5005 # Default server port
sock = None # Switch sended packet (To client or to server)

def SendBytes(data: str): # This def is replacing sock.sendto
     if client.Client: 
          client.client_sock.sendto(data, client.server_addr)
     elif server.Server:
          for c in server.clients:
               server.server_sock.sendto(data, c['ip'])

def SendTimeout():
     time.sleep(0.05) # Timeout

def SendServer(data: str):
     if server.Server:
          for c in server.clients:
               server.server_sock.sendto(f"{data}".encode(), c['ip'])

def SendDisconnect():
     if client.Client:
          try:
               client.Client = False
               if client.client_sock is not None:
                    client.client_sock.close()
                    client.client_sock = None
          except:
               pass
     else:
          try:
               SendServer(f"{user.returnUsername()} has closed the server. You have been disconnected.")
               SendServer(f"{var.server_send_kick}everybody")
               if server.server_sock is not None:
                    server.server_sock.close()
                    server.server_sock = None
          except:
               pass