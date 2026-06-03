from src.host import server, client
from src import user, console, port, tag, packet, serializer, settings
import time, os
from colorama import just_fix_windows_console, Fore

devUserMode: bool = False

text = """
             .oooooo.   oooo                      .
            d8P'  `Y8b  `888                    .o8
 .ooooo oo 888           888 .oo.    .oooo.   .o888oo
d88' `888  888           888P"Y88b  `P  )88b    888
888   888  888           888   888   .oP"888    888
888   888  `88b    ooo   888   888  d8(  888    888 .
`V8bod888   `Y8bood8P'  o888o o888o `Y888""8o   "888"
      888.
      8P'
      "
"""

def menu():
     return f"""
[{serializer.MAIN_COLOR} 1 {serializer.MAIN_RESET}] Run Server
[{serializer.MAIN_COLOR} 2 {serializer.MAIN_RESET}] Run Client
[{serializer.MAIN_COLOR} 3 {serializer.MAIN_RESET}] Settings
[{serializer.MAIN_COLOR} 4 {serializer.MAIN_RESET}] Check Port and Open port
"""

_devMenu = f"""
{tag.info}You have entered developer mode, please select the mode to run
{tag.info}In developer mode, when launching a client or server, the default port + 1 is used. 
{tag.info}This is necessary for a successful connection.

{tag.info}Type 0 to run server and connect to yourself
"""

def Launch():
     print(text)

     time.sleep(0.5)
     console.clear()

     Menu()

def devMenu():
     global devUserMode
     serializer.MAIN_COLOR = Fore.RED # Red color if you are in developer mode
     devUserMode = not devUserMode
     packet.port = packet.port + 1 # changing default port

     menu()
     console.clear()
     print(_devMenu + menu())

     choice = int(input(f"{serializer.INPUT_SYMBOL}"))
     if choice == 0:
          os.system(f'start cmd /k "python main.py -m dev -p {packet.port}"')
          packet.port = packet.port - 1
          user.NAME = "devServer"
          server.RunServer()

def Menu(): # https://github.com/qualzed/qChat/pull/1
     console.clear()
     print(menu())

     try:
          choice = int(input(f"{serializer.INPUT_SYMBOL}"))
     except ValueError:
          print(f"{tag.error} Invalid input! Please select and enter the number.")
          time.sleep(1)
          Menu()
          return
     
     match(choice):
          case 1:
               server.RunServer()
          case 2:
               client.SetClientMode()
          case 3: # Settings
               settings.settingsMenu()
          case 4:
               port.PortMenu()
          case 999:
               devMenu()
          case _:
               packet.SendVisualMessage(f"{tag.error} Invalid input! Please select and enter the number.")
               time.sleep(1)
               Menu()