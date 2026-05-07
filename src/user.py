import random, time
from src import console, menu

NAME = f"USER {random.randint(0,100)}" # Default username with random numbers

def CheckUser():
     global NAME
     with open('user.txt', 'w') as userFile:
          NAME = userFile.read()
          if len(NAME) > 12 :
               NAME = NAME[:9]+"..."

def UsernameChange():
     console.clear()
     NewUsername = input("> ")
     if NewUsername:
          if len(NewUsername) > 12:
               print("NO MORE THAN 12 SYMBOLS!")
               console.clear()
               UsernameChange()
          else:
               global NAME
               NAME = NewUsername
               
               print("You have changed your username")
               with open('user.txt', 'w') as userFile:
                    userFile.write(NAME)

               time.sleep(3)
               menu.Menu()
          