import os

def block_ip(ip):
    # Windows firewall example
    os.system(f'netsh advfirewall firewall add rule name="BLOCK_{ip}" dir=out remoteip={ip} action=block')

def unblock_ip(ip):
    os.system(f'netsh advfirewall firewall delete rule name="BLOCK_{ip}"')