import time
from src.host import client, server, var
from src import user
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import ANSI

packetSize = 4096 # Bytes
port = 5005 # Default port
server_port = 5005 # Default server port
sock = None # Switch sended packet (To client or to server)

def SendVisualMessage(data: str):
     with patch_stdout():
          print_formatted_text(ANSI(data))

def SendBytes(data: str): # This def is replacing sock.sendto
     if client.Client: 
          client.client_sock.sendto(data, client.server_addr)
     elif server.Server:
          for c in server.clients:
               SendServer(data)

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
               server.server_sock.close()
               server.server_sock = None
          except:
               pass