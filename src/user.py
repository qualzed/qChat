import random, time, requests, json
from src import console, menu, tag, serializer
from src.host import client, server

NAME = f"USER {random.randint(0,100)}" # Default username with random numbers

def getUserMode():
     if client.Client:
          return "client"
     elif server.Server:
          return "server"
     else:
          return "unknown"
     
def returnPersonalIP():
     return requests.get('https://api.ipify.org').text

def returnUsername():
     return NAME

def CheckUser():
     global NAME
     if len(NAME) > 12 :
          NAME = NAME[:9]+"..."

def UsernameChange():
     global NAME
     console.clear()
     NewUsername = input(f"{tag.info}Your current username is {NAME}\n> ")
     if NewUsername:
          if len(NewUsername) > 12:
               print(f"{tag.warning}NO MORE THAN 12 SYMBOLS!")

               time.sleep(3)
               console.clear()
               UsernameChange()
          else:
               NAME = NewUsername
               
               print(f"{tag.success}You have changed your username")
               
               serializer.UpdateJSON("username", NewUsername)

               time.sleep(3)
               menu.Menu()