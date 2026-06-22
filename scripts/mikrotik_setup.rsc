/ip address add address=192.168.10.1/24 interface=bridge

/ip pool add name=hotspot_pool ranges=192.168.10.10-192.168.10.254

/ip dhcp-server add name=dhcp1 interface=bridge address-pool=hotspot_pool disabled=no

/ip dhcp-server network add address=192.168.10.0/24 gateway=192.168.10.1 dns-server=8.8.8.8

/ip hotspot setup
# Follow prompts:
# interface: bridge
# address: 192.168.10.1
# pool: hotspot_pool
# dns: 8.8.8.8