from src.header import *
import argparse, time, os
from colorama import just_fix_windows_console

parser = argparse.ArgumentParser(description="Dev mode")
parser.add_argument("-m", "--mode", type=str, required=False, help="User connection mode")
parser.add_argument("-p", "--port", type=str, required=False, help="User connection port")
args = parser.parse_args()

if args.mode == "dev":
     try:
          time.sleep(3)
          packet.port = int(args.port)
          user.NAME = "devClient"
          client.Client = True
          client.RunClient("127.0.0.1")
     except Exception as e:
          print(e)
          input() # Wait for enter

if __name__ == "__main__":
     try:
          if os.name == "nt": # Once
               just_fix_windows_console()

          console.clear()
          serializer.ReadJSON()
          user.CheckUser()
          menu.Launch()
     except Exception as e:
          print(e)
          input() # Wait for enter