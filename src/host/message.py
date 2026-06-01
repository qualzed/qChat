from src.host import client, server, var
from src import user, control, packet, tag, serializer, console, menu
from src.file import sendFile
from src.crypto import key_generation, crypto_main
from cryptography.fernet import Fernet
import os

sentFileData = None
sentFileName = None
ReceiverStatus = False

def CheckMessage(data):
     sentData = data.decode(errors='ignore')
     if data.startswith(var.file_flag.encode()): # Here is Gemini Code
          global sentFileData, sentFileName
          
          flag_name_bytes = var.file_flag_name.encode()
          flag_name_index = data.find(flag_name_bytes)
          
          if flag_name_index > len(var.file_flag.encode()):
               sentFileData = data[len(var.file_flag.encode()):flag_name_index]
               sentFileName = data[flag_name_index + len(flag_name_bytes):].decode(errors='ignore')
               
               print("Accept file? (y/n)")
               var.code[0]['state'] = True
               return True
          else:
               print(f"{tag.error}Critical error! File name flag not found.")
               return True

     if sentData.startswith(var.server_send_kick):
          kicked = sentData[len(var.server_send_kick):]
          if user.returnUsername() == kicked or kicked == "everybody":
               packet.SendDisconnect()
               print(f"{tag.info}Write $exit to leave the session.")

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
     global sentFileName, sentFileData, msg
     while 1:  
          msg = input(f"\033[999;1H{serializer.INPUT_SYMBOL}")

          if var.code[0]['state'] == True:
               if msg == control.accept_file_key:
                    print(sentFileName)
                    sendFile.FileSave(name=sentFileName, data=sentFileData)
               var.code[0]['state'] = False

          if msg.startswith('$'):
               for v in var.code:
                    if msg == var.code[0]['code']:
                         v['state'] = not v['state']
                         sendFile.sendFileToUser()

               if msg == "$userlist":
                    for c in server.clients:
                         print(f"{c['ip']} {c['name']}\n")
               
               if msg == "$sendfile":
                    currentUser = str(input("Who is receiver: "))
                    filePath = str(input(f"Path to your file (limit is {packet.packetSize} bytes): "))
                    if os.path.isfile(filePath):
                         size_in_bytes = os.path.getsize(filePath)
                         if server.Server:
                              for c in server.clients:
                                   if currentUser == c['name']:
                                        sentFileName = filePath
                                        sendFile.sendFileRequest(user.returnUsername(), c['ip'], filePath, size_in_bytes, "None") # Fixed error with file sending
                                   else:
                                        print(f"{tag.warning}Undefined user")
                         elif client.Client:
                              sendFile.sendFileRequest(user.returnUsername(), '0.0.0.0', filePath, size_in_bytes, currentUser)
                              pass # here will be code where client send request to server to check is exist this user or not
                    else:
                         print(f"{tag.warning}Undefined file")

               if msg == "$clear": # only visual chat history cleaning
                    console.clear()

               if msg == "$exit": # Server disconnect
                    global RecieverStatus
                    RecieverStatus = False

                    packet.SendDisconnect()
                    console.clear()
                    menu.Menu()

               msg = None
          
          if msg != None:
               if client.Client:
                    client.client_sock.sendto(crypto_main.returnEncrypted(f"{user.NAME}: {msg}"), client.server_addr)
               if server.Server:
                    for c in server.clients:
                         server.server_sock.sendto(crypto_main.returnEncrypted(f"{user.NAME}: {msg}"), c['ip'])

def RecieveHandler(status: bool):
     global RecieverStatus
     RecieverStatus = status
     while RecieverStatus:
          if server.Server:
               try:
                    data, addr = server.server_sock.recvfrom(packet.packetSize)

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

               print("\r\033[K", end="")
               print(f"{crypto_main.returnDecrypted(data)}")
               print(f"{serializer.INPUT_SYMBOL}", end="", flush=True)

          if client.Client:
               try:
                    data, addr = client.client_sock.recvfrom(packet.packetSize)

                    if CheckMessage(data): # Intercepts bytes and check it on flag
                         continue 

                    print("\r\033[K", end="")
                    print(f"{crypto_main.returnDecrypted(data)}") # In the end cause check continue which is upper than sending
                    print(f"{serializer.INPUT_SYMBOL}", end="", flush=True)

               except:
                    continue