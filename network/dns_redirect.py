import os

def enable_dns_redirect(portal_ip="192.168.10.10"):
    # Windows/Linux hosts-based redirect (simple ISP method)

    hosts_entry = f"""
{portal_ip} google.com
{portal_ip} facebook.com
{portal_ip} youtube.com
"""

    with open("hosts_redirect.txt", "w") as f:
        f.write(hosts_entry)