# Description: imports all the necessary DHCP config from dhcp_config.py 
# and runs it as part of the main workflow

# Author: Skandha Prakash
# Version: 3.2

import configparser
import sys
from dhcp_config import generate_dhcp_config

def main(dc_name):
    # Load configurations
    switch_conf = configparser.ConfigParser()
    devices_conf = configparser.ConfigParser()
    switch_conf.read("switch.conf")
    devices_conf.read("devices.conf")
    
     # Check for required sections in configuration files
    if dc_name not in switch_conf:
        raise ValueError(f"Error: {dc_name} section not found in switch.conf")
    if dc_name not in devices_conf:
        raise ValueError(f"Error: {dc_name} section not found in devices.conf")

    # Basic Datacenter Switch Configuration
    dc_info = switch_conf[dc_name]
    subnet = dc_info.get("subnet")
    gateway = dc_info.get("gateway")
    vlan = dc_info.get("Vlan")
    ports = dc_info.get("Ports", "").split(",")
    interface_type = dc_info.get("InterfaceType", "GigabitEthernet")
    interface_speed = dc_info.get("InterfaceSpeed", "1000")  # Default speed to 1000 if not specified
    dhcp_start = dc_info.get("dhcpStart")
    dhcp_end = dc_info.get("dhcpEnd")
    
    # DMZ and Web Server Configuration
    dmz_subnet = dc_info.get("DMZ")
    dmz_gateway = dc_info.get("DMZ_Gateway")
    dmz_vlan = dc_info.get("DMZ_Vlan")
    webserver_ips = dc_info.get("Webserver_IPs")
    dmz_ports = dc_info.get("DMZ_ports", "").split(",")
    
    apache_servers = dc_info.get("Apache_Servers")
    load_balancers = dc_info.get("Load_Balancers")
    
    # Application Server Configuration
    app_vlan = dc_info.get("App_Vlan")
    app_gateway = dc_info.get("App_Gateway")
    app_subnet = dc_info.get("App_Subnet")
    app_ports = dc_info.get("App_Ports", "").split(",")
    app_ips = dc_info.get("App_IPs")
    app_applications = dc_info.get("App_Applications")
    
    # Active Directory, Database Servers, and App Load Balancers
    active_directories = dc_info.get("ActiveDirectories")
    database_servers = dc_info.get("Database_Servers")
    app_load_balancers = dc_info.get("App_Load_Balancers")
    
    if dc_name not in devices_conf:
        print(f"Error: {dc_name} section not found in devices.conf")
        return

    ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
    
    dhcp_config, dhcp_pool_size, available_hosts, backup_filename = generate_dhcp_config(
        dc_name, subnet, gateway, vlan, ports, interface_type, interface_speed, 
        ip_list, devices_conf, dhcp_start, dhcp_end, dmz_subnet, 
        dmz_gateway, dmz_vlan, webserver_ips, dmz_ports, apache_servers, load_balancers, app_vlan, 
        app_gateway, app_subnet, app_ports, app_ips, app_applications, active_directories, 
        database_servers, app_load_balancers
    )
    
    # Display the result
    print("\n--- DHCP Configuration Summary ---")
    print(f"Data Center: {dc_name}")
    print(f"Subnet: {subnet}")
    print(f"Gateway: {gateway}")
    print(f"Available Hosts: {available_hosts}")
    print(f"Device IPs for DHCP: {dhcp_pool_size}")
    print(f"DMZ Subnet: {dmz_subnet}")
    print(f"DMZ Gateway: {dmz_gateway}")
    print(f"DMZ VLAN: {dmz_vlan}")
    print(f"Webserver IP Range: {webserver_ips}")
    print(f"Apache Servers: {apache_servers}")
    print(f"Load Balancers: {load_balancers}")
    print(f"App Subnet: {app_subnet}")
    print(f"App Gateway: {app_gateway}")
    print(f"App VLAN: {app_vlan}")
    print(f"App IP Range: {app_ips}")
    print(f"Active Directories: {active_directories}")
    print(f"Database Servers: {database_servers}")
    print(f"App Load Balancers: {app_load_balancers}")
    
    if backup_filename:
        print(f"Backup saved to: {backup_filename}")
    print("\nGenerated DHCP Configuration:")
    print(dhcp_config)

# Run the script with the data center name as an argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_switch.py <DC_NAME>")
    else:
        main(sys.argv[1])
