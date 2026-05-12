from src.host import server, client
from src import user, console, port
import  time

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
menu = """
[1]: Run Server
[2]: Run Client
[3]: Change Username
[4]: Check Port and Open port
"""

def Launch():
     print(text)

     time.sleep(1)
     console.clear()

     Menu()

def Menu():
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
               port.check_port_open(5005)