from src.host import server, client
from src import user, console, port, tag, packet
import time, os
from colorama import just_fix_windows_console, Fore

mColor = Fore.GREEN # Main color
mReset = Fore.RESET

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

menu = f"""
[{mColor} 1 {mReset}] Run Server
[{mColor} 2 {mReset}] Run Client
[{mColor} 3 {mReset}] Change Username
[{mColor} 4 {mReset}] Check Port and Open port

{tag.info}Settings window will soon
"""

def Launch():
     print(text)

     time.sleep(1)
     console.clear()

     Menu()

def Menu():
     if os.name == "nt":
          just_fix_windows_console()

     console.clear()
     print(menu)
     
     choice = int(input("> "))
     match(choice):
          case 1:
               server.RunServer()
          case 2:
               client.SetClientMode()
          case 3:
               user.UsernameChange()
          case 4:
               port.open_port(packet.port)