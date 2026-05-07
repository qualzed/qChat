from src.host import client, server
from src import user

def MessageHandler():
     while 1:  
          msg = input("> ")
          if client.Client:
               client.client_sock.sendto(f"{user.NAME}: {msg}".encode(), client.server_addr)
          if server.Server:
               for client_addr in server.clients:
                    server.server_sock.sendto(f"{user.NAME}: {msg}".encode(), client_addr)

def RecieveHandler():
     while 1:
          if server.Server:
               data, addr = server.server_sock.recvfrom(1024) # 1024 bytes is ready to recieve our host

               if addr not in server.clients:
                    server.clients.add(addr) # Add client to your list

               print(f"{data.decode()}") # Output message from client

          if client.Client:
               data, addr = client.client_sock.recvfrom(1024)
               print(f"{data.decode()}")