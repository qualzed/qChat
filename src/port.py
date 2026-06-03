import time, socket, upnpy
from src import menu, tag, packet, serializer, console
from src.host import client, server
from concurrent.futures import ThreadPoolExecutor

def returnPortMenu():
    return f"""
[{serializer.MAIN_COLOR} 1 {serializer.MAIN_RESET}] Open port {packet.port}
[{serializer.MAIN_COLOR} 2 {serializer.MAIN_RESET}] Find Open Port
[{serializer.MAIN_COLOR} 0 {serializer.MAIN_RESET}] Back to Menu
"""

def PortMenu():
    console.clear()
    print(returnPortMenu())
    choice = int(input(f"{serializer.INPUT_SYMBOL}"))
    match(choice):
        case 1:
            open_port()
        case 2:
            FindOpenPort()
        case 0:
            menu.Menu()
        case _:
            packet.SendVisualMessage(f"{tag.error} Invalid input! Please select and enter the number.")

def check_single_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        
        if result == 0:
            return port
    except Exception:
        pass
    return None

def FindOpenPort():
    if client.Client or server.Server:
        return

    OpenedPorts = []
    ports_to_check = range(5000, 20000)

    with ThreadPoolExecutor(max_workers=1000) as executor:
        results = executor.map(check_single_port, ports_to_check)

        for p in results:
            if p is not None:
                OpenedPorts.append(p)
                
    packet.SendVisualMessage("Opened ports:")
    for port in OpenedPorts:
        packet.SendVisualMessage(f"{port}")

def open_port(port):
    upnp = upnpy.UPnP()
    try:
        devices = upnp.discover()
        if not devices:
            print(f"{tag.error}UPnP device not found.")
            time.sleep(2.5)
            menu.Menu()

        device = devices[0]
        service = device.get_service('WANIPConnection1') or device.get_service('WANPPPConnection1')

        if service:
            lan_addr = upnp.get_local_ip()
            
            service.AddPortMapping(
                NewRemoteHost='',
                NewExternalPort=port,
                NewProtocol='UDP',
                NewInternalPort=port,
                NewInternalClient=lan_addr,
                NewEnabled=1,
                NewPortMappingDescription='qChat',
                NewLeaseDuration=0
            )
            print(f"{tag.success}Port {port} opened successfully on {lan_addr}")
        else:
            print(f"{tag.error}UPnP service not found on router.")

    except Exception as e:
        print(f"{tag.error}UPnP Error: {e}")
    
    time.sleep(3)
    menu.Menu()