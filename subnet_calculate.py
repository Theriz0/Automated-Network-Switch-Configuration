# network_util.py
# Description: Utility functions for network calculations
# Author: Skandha Prakash

from ipaddress import ip_network

# Network utility functions
def calculate_dhcp_pool_size(ips):
    # Calculate the number of unique IP addresses specified for DHCP.
    unique_ips = set(ips)
    return len(unique_ips)

def calculate_available_hosts(subnet):
    # Calculate the number of usable hosts in a given subnet.
    network = ip_network(subnet, strict=False)
    return network.num_addresses - 2  # Subtract 2 for network and broadcast addresses