import os
from src import packet, tag
from src.host import client, server, var
from src import user
from src.file import chunks

fileData = None
reqFile = None

def writeFileToBytes(receiver, sock, size: float, path: str = "Unknown.qChat"):
     if size > packet.packetSize:
          for chunk_data in chunks.chunk(path):
               sock.sendto(chunk_data, receiver)
          filename = os.path.basename(path).encode()
          sock.sendto(b'$chunks:END:' + filename, receiver)
     else:
          with open(path, 'rb') as f:
               file_data = f.read()
          sock.sendto(var.file_flag.encode() + file_data + var.file_flag_name.encode() + os.path.basename(path).encode(), receiver)

def sendFileRequest(senderName: str, receiver: str, filename: str, size: float, username: str): # 21.05.2026 user: str - was added
     # if(size > packet.packetSize): # fixed 21.05.2026
          # packet.SendVisualMessage(f"{tag.warning}You cant send any file that bigger then {packet.packetSize} bytes.")
          # return

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
     sendFileToUser(receiver=receiver)
     writeFileToBytes(receiver=receiver, sock=sender_data, size=size, path=filename)

def FileSave(name: str, data: bytes): # save on receiver computer
     download_path = "downloads"
     if not os.path.exists(download_path):
          os.makedirs(download_path)

     with open(f"{download_path}/{name}", "wb") as file:
          try:
               file.write(data)
               packet.SendVisualMessage(f"{tag.success}File has been downloaded success! Check out {download_path} folder.")
          except Exception as e:
               packet.SendVisualMessage(f"{tag.error}Error while download has accured: {e}")

def sendFileToUser(receiver: str):
     if user.getUserMode() == "server":
          sender_data = server.server_sock
     elif user.getUserMode() == "client":
          sender_data = client.client_sock
     else:
          return

     sender_data.sendto(var.code[1]['code'].encode(), receiver)