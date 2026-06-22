import os

def restart_dhcp():
    # Windows Server DHCP restart example
    os.system("net stop dhcpserver && net start dhcpserver")