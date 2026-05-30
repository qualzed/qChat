import upnpy
import time
from src import menu, tag

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