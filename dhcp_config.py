# Description: All DHCP configuration reads both switch.conf and devices.conf here
# Author: Skandha Prakash

from ipaddress import ip_network
from dhcp_backup import backup_config
from subnet_calculate import calculate_dhcp_pool_size, calculate_available_hosts 

# DHCP configuration generation function
def generate_dhcp_config(dc_name, subnet, gateway, vlan, ports, interface_type, interface_speed, 
                         dhcp_snooping, ip_list, devices_conf, auth_method, admin_role, 
                         readonly_role, dhcp_start, dhcp_end):
    network = ip_network(subnet, strict=False)
    gateway = str(network.network_address + 1)
    config = []
    
    # Generate the configuration content
    config.append(f"! {dc_name} DHCP and VLAN Configuration")
    config.append(f"ip dhcp excluded-address {gateway}")
    config.append(f"interface vlan {vlan}")
    config.append(f" ip address {gateway} {network.netmask}")
    config.append(f" default-router {gateway}")
    config.append(" no shutdown\n")
    
    config.append(f"ip dhcp pool {dc_name}_pool")
    config.append(f" network {network.network_address} {network.netmask}")
    config.append(f" default-router {gateway}")
    config.append(f" dns-server {gateway}")
    config.append(f" address range {dhcp_start} {dhcp_end}")
    
    # Authorization configuration
    config.append("\n! Authorization settings")
    config.append(f"aaa new-model")
    
    if auth_method == "RADIUS":
        config.append("aaa authentication login default group radius local")
        config.append("aaa authorization exec default group radius if-authenticated")
    elif auth_method == "TACACS+":
        config.append("aaa authentication login default group tacacs+ local")
        config.append("aaa authorization exec default group tacacs+ if-authenticated")
    else:
        config.append("aaa authentication login default local")
    
    config.append(f"username {admin_role} privilege 15 secret your_secure_password")
    config.append(f"username {readonly_role} privilege 5 secret your_secure_password")
    
    # Device-specific configurations from devices.conf
    if dc_name in devices_conf:
        ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
        device_types = devices_conf[dc_name].get("DeviceType", "").split(", ")
        allowed_protocols = devices_conf[dc_name].get("AllowedProtocols", "").split(", ")
        authorization_levels = devices_conf[dc_name].get("Authorization", "").split(", ")

        for i, ip in enumerate(ip_list):
            device_type = device_types[i] if i < len(device_types) else "Unknown"
            protocols = allowed_protocols if allowed_protocols else ["All"]
            auth_level = authorization_levels[i] if i < len(authorization_levels) else "Unknown"

            # Device-specific IP reservation and description
            config.append(f"\n! Configuration for {device_type} device at IP {ip}")
            config.append(f"ip dhcp host {ip}")
            config.append(f" description {device_type} device")
            config.append(f" allowed-protocols {', '.join(protocols)}")
            config.append(f" authorization-role {auth_level}")
    
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
