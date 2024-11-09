# Description: All DHCP configuration reads both switch.conf and devices.conf here
# Author: Skandha Prakash

import datetime
import os
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

# Backup configuration function
def backup_config(dc_name, config_content):
    # Save the generated DHCP configuration to a backup file.
    backup_dir = "backup"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = os.path.join(backup_dir, f"backup_{dc_name}_{timestamp}.cfg")
    
    os.makedirs(backup_dir, exist_ok=True)  # Ensure the backup directory exists
    try:
        with open(backup_filename, 'w') as backup_file:
            backup_file.write(config_content)
        print(f"Backup configuration saved to file: {backup_filename}")
    except IOError as e:
        print(f"Error creating backup file {backup_filename}: {e}")
        return None
    return backup_filename

# DHCP configuration generation function
def generate_dhcp_config(dc_name, subnet, vlan, ports, interface_type, interface_speed, dhcp_snooping, ip_list, devices_conf):
    network = ip_network(subnet, strict=False)
    gateway = str(network.network_address + 1)
    config = []
    
    # Generate the configuration content
    config.append(f"! {dc_name} DHCP and VLAN Configuration")
    config.append(f"ip dhcp excluded-address {gateway}")
    config.append(f"interface vlan {vlan}")
    config.append(f" ip address {gateway} {network.netmask}")
    config.append(" no shutdown\n")
    
    config.append(f"ip dhcp pool {dc_name}_pool")
    config.append(f" network {network.network_address} {network.netmask}")
    config.append(f" default-router {gateway}")
    config.append(f" dns-server {gateway}")
    config.append(" lease 0 12")

    # Device-specific configurations from devices.conf
    if dc_name in devices_conf:
        ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
        device_types = devices_conf[dc_name].get("DeviceType", "").split(", ")
        allowed_protocols = devices_conf[dc_name].get("AllowedProtocols", "").split(", ")

        for i, ip in enumerate(ip_list):
            device_type = device_types[i] if i < len(device_types) else "Unknown"
            protocols = allowed_protocols if allowed_protocols else ["All"]

            # Device-specific IP reservation and description
            config.append(f"\n! Configuration for {device_type} device at IP {ip}")
            config.append(f"ip dhcp host {ip}")
            config.append(f" description {device_type} device")
            config.append(f" allowed-protocols {', '.join(protocols)}")
    
    for port in ports:
        config.append(f"\ninterface {interface_type} {port.strip()}")
        config.append(" switchport mode access")
        config.append(f" switchport access vlan {vlan}")
        config.append(f" speed {interface_speed}")
        config.append(" no shutdown")
    
    if dhcp_snooping:
        config.append("\nip dhcp snooping")
        config.append(f"ip dhcp snooping vlan {vlan}")
        config.append("ip dhcp snooping trust")
        for port in ports:
            config.append(f"interface {interface_type} {port.strip()}")
            config.append(" ip dhcp snooping limit rate 15")
    
    # Calculate DHCP pool size and available hosts
    dhcp_pool_size = calculate_dhcp_pool_size(ip_list)
    available_hosts = calculate_available_hosts(subnet)
    
    # Create final configuration content and backup it up
    dhcp_config_content = "\n".join(config)
    backup_filename = backup_config(dc_name, dhcp_config_content)
    
    return dhcp_config_content, dhcp_pool_size, available_hosts, backup_filename
