import os, keyboard
from src import control, packet, tag
from src.host import client, server, var
from src import user

fileData = None
reqFile = None

def writeFileToBytes(receiver, sock, path: str = "Unknown.qChat"):
     global fileData
     with open(path, 'rb') as f:
          fileData = f.read()
          sock.sendto(var.file_flag.encode() + fileData + var.file_flag_name.encode() + path.encode(), receiver)

def sendFileRequest(senderName: str, receiver: str, filename: str, size: float, username: str): # 21.05.2026 user: str - was added
     if(size > packet.packetSize): # fixed 21.05.2026
          print(f"{tag.warning}You cant send any file that bigger then {packet.packetSize} bytes.")
          return

     msg = f"\n{senderName} has sent you file '{filename}' size: {round(size, 2)} byte(-s)"
     
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return
     
     if receiver == '0.0.0.0':
          sender_data = client.client_sock # Force client mode cause in message.py client cant read client list, only server
          receiver = client.server_addr # Send it to server anyway, then server will check it and return to current client
     
     sender_data.sendto(msg.encode(), receiver)
     sender_data.sendto(var.code[0]['code'].encode(), receiver)
     packet.SendTimeout()
     writeFileToBytes(receiver=receiver, sock=sender_data, path=filename)

def FileSave(name: str, data: bytes): # save on receiver computer
     download_path = "downloads"
     if not os.path.exists(download_path):
          os.makedirs(download_path)

     with open(f"{download_path}/{name}", "wb") as file:
          try:
               file.write(data)
               print(f"{tag.success}\nFile has been downloaded success! Check out {download_path} folder.")
          except Exception as e:
               print(f"{tag.error}\nError while download has accured: {e}")

def sendFileToUser(receiver: str):
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return

     sender_data.sendto(var.code[1]['code'].encode(), receiver)