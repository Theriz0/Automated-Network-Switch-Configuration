# Description: All DHCP configuration reads both switch.conf and devices.conf here
# Author: Skandha Prakash

from ipaddress import ip_network
from dhcp_backup import backup_config
from subnet_calculate import calculate_dhcp_pool_size, calculate_available_hosts 

# DHCP configuration generation function
def generate_dhcp_config(dc_name, subnet, gateway, vlan, ports, interface_type, interface_speed, 
                          ip_list, devices_conf, dhcp_start, dhcp_end, dmz_subnet, dmz_gateway, dmz_vlan,
                          webserver_ips, dmz_ports, apache_servers, load_balancers, app_vlan, app_gateway, 
                          app_subnet, app_ports, app_ips, app_applications,
                          active_directories, database_servers, app_load_balancers):
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
    
    # Device-specific configurations from devices.conf
    if dc_name in devices_conf:
        ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
        device_types = devices_conf[dc_name].get("DeviceType", "").split(", ")
        allowed_protocols = devices_conf[dc_name].get("AllowedProtocols", "").split(", ")
        authorization_levels = devices_conf[dc_name].get("Authorization", "").split(", ")
        dhcp_gateway = devices_conf[dc_name].get("DHCP_Gateway", "None")
        dmz_gateway = devices_conf[dc_name].get("DMZ_Gateway", "None")
        app_gateway = devices_conf[dc_name].get("App_Gateway", "None")

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
            
            # DHCP Gateway Configuration
            if dhcp_gateway and dhcp_gateway != "None":
                config.append(f"\n! DHCP Gateway Configuration for {dc_name}")
                config.append(f"ip default-gateway {dhcp_gateway}")
            
            # DMZ Gateway Configuration
            if dmz_gateway and dmz_gateway != "None":
                config.append(f"\n! DMZ Gateway Configuration for {dc_name}")
                config.append(f"ip default-gateway {dmz_gateway}")

            # App Gateway Configuration
            if app_gateway and app_gateway != "None":
                config.append(f"\n! Application Gateway Configuration for {dc_name}")
                config.append(f"ip route {app_gateway}")
    
    for port in ports:
        config.append(f"\ninterface {interface_type} {port.strip()}")
        config.append(" switchport mode access")
        config.append(f" switchport access vlan {vlan}")
        config.append(f" speed {interface_speed}")
        config.append(" no shutdown")
    
    # DMZ Configuration
    if dmz_subnet and dmz_gateway and dmz_vlan:
        dmz_network = ip_network(dmz_subnet, strict=False)
        config.append(f"\n! DMZ Configuration for {dc_name}")
        config.append(f"interface vlan {dmz_vlan}")
        config.append(f" ip address {dmz_gateway} {dmz_network.netmask}")
        config.append(" no shutdown\n")

        config.append(f"ip dhcp pool {dc_name}_dmz_pool")
        config.append(f" network {dmz_network.network_address} {dmz_network.netmask}")
        config.append(f" default-router {dmz_gateway}")
        config.append(f" address range {webserver_ips.split(' - ')[0]} {webserver_ips.split(' - ')[1]}")
        
        # Add port configurations for the DMZ VLAN
        for dmz_port in dmz_ports:
            config.append(f"\ninterface {interface_type} {dmz_port.strip()}")
            config.append(" switchport mode access")
            config.append(f" switchport access vlan {dmz_vlan}")
            config.append(f" speed {interface_speed}")
            config.append(" no shutdown")
            
        # Apache Server Configuration
        config.append(f"\n! Apache Server Configuration for {dc_name}")
        config.append(f" address range {apache_servers}")
    
        # Load Balancer Configuration
        config.append(f"\n! Load Balancer Configuration for {dc_name}")
        config.append(f" address range {load_balancers}")
    
    # App_VLAN Configuration
    if app_subnet and app_gateway and app_vlan:
        app_network = ip_network(app_subnet, strict=False)
        config.append(f"\n! App_VLAN Configuration for {dc_name}")
        config.append(f"interface vlan {app_vlan}")
        config.append(f" ip address {app_gateway} {app_network.netmask}")
        config.append(" no shutdown\n")

        config.append(f"ip dhcp pool {dc_name}_app_pool")
        config.append(f" network {app_network.network_address} {app_network.netmask}")
        config.append(f" default-router {app_gateway}")
        config.append(f" address range {app_ips.split(' - ')[0]} {app_ips.split(' - ')[1]}")
        
        # Add port configurations for the App VLAN
        for app_port in app_ports:
            config.append(f"\ninterface {interface_type} {app_port.strip()}")
            config.append(" switchport mode access")
            config.append(f" switchport access vlan {app_vlan}")
            config.append(f" speed {interface_speed}")
            config.append(" no shutdown")
            
        # Active Directory Configuration
        config.append(f"\n! Active Directory Configuration for {dc_name}")
        config.append(f" address range {active_directories.split(' - ')[0]} {active_directories.split(' - ')[1]}")
        
        # Database Server Configuration
        config.append(f"\n! Database Server Configuration for {dc_name}")
        config.append(f" address range {database_servers.split(' - ')[0]} {database_servers.split(' - ')[1]}")
        
        # App Load Balancer Configuration
        config.append(f"\n! App Load Balancer Configuration for {dc_name}")
        config.append(f" address range {app_load_balancers.split(' - ')[0]} {app_load_balancers.split(' - ')[1]}")

        # Applications hosted on App VLAN
        config.append(f"\n! Applications hosted on App_VLAN: {app_applications}")    
        
    # Calculate DHCP pool size and available hosts
    dhcp_pool_size = calculate_dhcp_pool_size(ip_list)
    available_hosts = calculate_available_hosts(subnet)
    
    # Create final configuration content and backup it up
    dhcp_config_content = "\n".join(config)
    backup_filename = backup_config(dc_name, dhcp_config_content)
    
    return dhcp_config_content, dhcp_pool_size, available_hosts, backup_filename
