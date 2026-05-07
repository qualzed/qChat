import miniupnpc, time
from src import menu

def open_port(port):
    upnp = miniupnpc.UPnP()
    try:
        if upnp.discover() > 0:
            upnp.selectigd()
            upnp.addportmapping(port, 'UDP', upnp.lanaddr, port, 'qChat', '')
            print(f"Port {port} was open with UPnP")
        else:
            print("UPnP device not found. Check router settings.")
    except Exception as e:
        if "Success" in str(e):
            print(f"Port {port} is likely already open (Success).")
        else:
            print(f"UPnP Error: {e}")
            
def check_port_open(port):
    upnp = miniupnpc.UPnP()
    try:
        if upnp.discover() > 0:
            upnp.selectigd()
        if upnp.getspecificportmapping(port, 'UDP'):
            print(f"Port {port} is already open.")
        else:
            upnp.addportmapping(port, 'UDP', upnp.lanaddr, port, 'qChat', '')
            print(f"Success! Port {port} is open with UPnP.")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(3)
    menu.Menu()