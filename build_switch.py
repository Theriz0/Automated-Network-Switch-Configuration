# Program: build_switch.py
# Author: Skandha Prakash
# Version: 1.0

import configparser
import sys
from ipaddress import ip_network

def calculate_dhcp_pool_size(ips):
    # Calculate the number of unique IP addresses specified for DHCP
    unique_ips = set(ips)
    return len(unique_ips)

def generate_dhcp_config(dc_name, subnet, vlan, interface):
    # Split the subnet and mask for configuration purposes
    network = ip_network(subnet, strict=False)
    gateway = str(network.network_address + 1)  # Use the first IP as the gateway
    
    # Generate the DHCP pool configuration based on required size
    config = []
    config.append(f"! {dc_name} DHCP and VLAN Configuration")
    config.append(f"ip dhcp excluded-address {gateway}")
    config.append(f"interface vlan {vlan}")
    config.append(f" ip address {gateway} {network.netmask}")
    config.append(" no shutdown\n")

    # DHCP Pool for the subnet
    config.append(f"ip dhcp pool {dc_name}_pool")
    config.append(f" network {network.network_address} {network.netmask}")
    config.append(f" default-router {gateway}")
    config.append(f" dns-server {gateway}")
    config.append(f" lease 0 12")
    
    return "\n".join(config)

def main(dc_name):
    # Load the configuration files
    switch_conf = configparser.ConfigParser()
    devices_conf = configparser.ConfigParser()
    
    switch_conf.read("switch.conf")
    devices_conf.read("devices.conf")
    
    # Check if the given DC exists in switch config
    if dc_name not in switch_conf:
        print(f"Error: {dc_name} section not found in DC_Switch.conf")
        return

    # Get DC-specific configuration
    dc_info = switch_conf[dc_name]
    subnet = dc_info.get("NY_subnet")
    vlan = dc_info.get("Vlan")
    interface = dc_info.get("Interfaces")

    # Collect IPs from devices.conf for DHCP pool calculation
    if dc_name not in devices_conf:
        print(f"Error: {dc_name} section not found in devices.conf")
        return

    # Extract IPs from devices.conf for the specified data center
    ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
    dhcp_pool_size = calculate_dhcp_pool_size(ip_list)

    # Generate the DHCP configuration
    dhcp_config = generate_dhcp_config(dc_name, subnet, vlan, interface)

    # Output the generated configuration
    print(dhcp_config)

# Run the script with the data center name as an argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_switch.py <DC_NAME>")
    else:
        main(sys.argv[1])
