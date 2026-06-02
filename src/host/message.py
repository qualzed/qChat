from src.host import client, server, var
from src import user, control, packet, tag, serializer, console, menu
from src.file import sendFile
from src.crypto import key_generation, crypto_main
import datetime
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import ANSI

sentFileData = None
sentFileName = None
ReceiverStatus = False
session = PromptSession()

def CheckLocalMessage(data: str): # This def will check before send it to client/server
     global sentFileName, sentFileData

     if var.code[0]['state'] == True:
          if data == control.accept_file_key:
               packet.SendVisualMessage(sentFileName)
               sendFile.FileSave(name=sentFileName, data=sentFileData)
          var.code[0]['state'] = False

     if data.startswith('$'):
          for v in var.code:
               if data == var.code[0]['code']:
                    v['state'] = not v['state']
                    sendFile.sendFileToUser()

          if data == "$userlist":
               for c in server.clients:
                    packet.SendVisualMessage(f"{c['ip'][0]} {c['name']}\n") # c['ip'][0] - it returns only IP, without port
          
          if data == "$sendfile":
               currentUser = session.prompt("Who is receiver: ")
               filePath = session.prompt(f"Path to your file (limit is {packet.packetSize} bytes): ")
               if os.path.isfile(filePath):
                    size_in_bytes = os.path.getsize(filePath)
                    if server.Server:
                         for c in server.clients:
                              if currentUser == c['name']:
                                   sentFileName = filePath
                                   sendFile.sendFileRequest(user.returnUsername(), c['ip'], filePath, size_in_bytes, "None") # Fixed error with file sending
                              else:
                                   packet.SendVisualMessage(f"{tag.warning}Undefined user")
                    elif client.Client:
                         sendFile.sendFileRequest(user.returnUsername(), '0.0.0.0', filePath, size_in_bytes, currentUser)
                         pass # here will be code where client send request to server to check is exist this user or not
               else:
                    packet.SendVisualMessage(f"{tag.warning}Undefined file")

          if data == "$clear": # only visual chat history cleaning
               console.clear()

          if data == "$ban":
               if server.Server:
                    currentUser = session.prompt("Who you want to ban: ")
                    if server.NameToIP(currentUser) is not None:
                         server.BanByName(currentUser)

          if data == "$exit": # Server disconnect
               global RecieverStatus
               RecieverStatus = False
               packet.SendDisconnect()
               console.clear()
               menu.Menu()
     
          return True

def CheckMessage(data):
     sentData = data.decode(errors='ignore')
     if data.startswith(var.file_flag.encode()): # Here is Gemini Code
          global sentFileData, sentFileName
          
          flag_name_bytes = var.file_flag_name.encode()
          flag_name_index = data.find(flag_name_bytes)
          
          if flag_name_index > len(var.file_flag.encode()):
               sentFileData = data[len(var.file_flag.encode()):flag_name_index]
               sentFileName = data[flag_name_index + len(flag_name_bytes):].decode(errors='ignore')
               
               packet.SendVisualMessage("Accept file? (y/n)")
               var.code[0]['state'] = True
               return True
          else:
               packet.SendVisualMessage(f"{tag.error}Critical error! File name flag not found.")
               return True

     if sentData.startswith(var.server_send_ban):
          kicked = sentData[len(var.server_send_ban):]
          if kicked == "everybody":
               packet.SendDisconnect()
               packet.SendVisualMessage(f"{tag.info}Write $exit to leave the session.")
          elif kicked == user.returnUsername():
               packet.SendDisconnect()
               packet.SendVisualMessage(
                    f"{tag.warning}You have been kicked from the server.\nUse {serializer.MAIN_COLOR}$exit{serializer.MAIN_RESET}"
               )

          return True

     if client.Client:
          if data.startswith(var.crypto_key_flag.encode()):
               server_pub_bytes = data[len(var.crypto_key_flag.encode()):]
               client_pub_bytes = crypto_main.generateDHKeys()

               client.temp_cipher = crypto_main.deriveTemporaryKey(server_pub_bytes) # Create a temporary cipher on the client side
               client.client_sock.sendto(var.client_pub_flag.encode() + client_pub_bytes, client.server_addr)
               return True

          if data.startswith(var.room_key_flag.encode()):
               encrypted_room_key = data[len(var.room_key_flag.encode()):]
               decrypted_room_key = client.temp_cipher.decrypt(encrypted_room_key)
               crypto_main.setRoomKey(decrypted_room_key)
               return True

     if server.Server:
          if data.startswith(var.client_pub_flag.encode()):
               client_pub_bytes = data[len(var.client_pub_flag.encode()):]
               temp_cipher = crypto_main.deriveTemporaryKey(client_pub_bytes)
               
               if temp_cipher:
                    from src.crypto import key_generation
                    encrypted_room_key = temp_cipher.encrypt(key_generation.key.encode())
                    for c in server.clients:
                         server.server_sock.sendto(var.room_key_flag.encode() + encrypted_room_key, c['ip'])
               return True

     if sentData.startswith(var.code[0]['code']):
          return True # Just skip

def MessageHandler():
     while 1:
          with patch_stdout():
               msg = session.prompt(ANSI(f"{serializer.INPUT_SYMBOL}"))

          if not msg or not msg.strip():
               print(f"\033[1A\033[2K", end="", flush=True)
               continue

          print(f"\033[1A\033[2K", end="", flush=True)
          formatted_msg = f"[ {datetime.datetime.now().strftime('%I:%M %p').lstrip('0')} ] You: {msg}" # Timestamp
          packet.SendVisualMessage(formatted_msg)

          if CheckLocalMessage(msg):
               continue
          
          if msg is not None:
               if client.Client:
                    client.client_sock.sendto(
                         crypto_main.returnEncrypted(
                              f"[ {datetime.datetime.now().strftime('%I:%M %p').lstrip('0')} ] {user.NAME}: {msg}"
                         ), client.server_addr
                    )
               if server.Server:
                    for c in server.clients:
                         server.server_sock.sendto(
                              crypto_main.returnEncrypted(
                                   f"[ {datetime.datetime.now().strftime('%I:%M %p').lstrip('0')} ] {user.NAME}: {msg}"
                              ), c['ip']
                         )

def RecieveHandler(status: bool):
     global RecieverStatus
     RecieverStatus = status
     while RecieverStatus:
          if server.Server:
               try:
                    data, addr = server.server_sock.recvfrom(packet.packetSize)

                    if addr[0] in server.bans:
                         continue

                    if CheckMessage(data): # Intercepts bytes and check it on flag
                         continue 
               except:
                    continue

               if addr not in [c['ip'] for c in server.clients]:
                    decode = data.decode().strip()
                    if decode.startswith("$nm:"):
                         username = decode[4:]
                         server.clients.append({'ip': addr, 'name': username})
                         # Send Cipher to connected Client
                         server_pub_bytes = crypto_main.generateDHKeys()
                         server.server_sock.sendto(var.crypto_key_flag.encode() + server_pub_bytes, addr)
                         continue

               if data.decode() == "$nm:": # skip check if the user was connected before
                    continue

               for c in server.clients:
                    if(c['ip'] != addr):
                         server.server_sock.sendto(data, c['ip'])

               packet.SendVisualMessage(data=crypto_main.returnDecrypted(data))

          if client.Client:
               try:
                    data, addr = client.client_sock.recvfrom(packet.packetSize)

                    if CheckMessage(data): # Intercepts bytes and check it on flag
                         continue 

                    with patch_stdout():
                         packet.SendVisualMessage(f"{crypto_main.returnDecrypted(data)}") # In the end cause check continue which is upper than sending

               except:
                    continue