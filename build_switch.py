# Description: imports all the necessary DHCP config from dhcp_config.py 
# and runs it as part of the main workflow

# Author: Skandha Prakash
# Version: 3.1

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

    dc_info = switch_conf[dc_name]
    subnet = dc_info.get("subnet")
    gateway = dc_info.get("gateway")
    vlan = dc_info.get("Vlan")
    ports = dc_info.get("Ports", "").split(",")
    interface_type = dc_info.get("InterfaceType", "GigabitEthernet")
    interface_speed = dc_info.get("InterfaceSpeed", "1000")  # Default speed to 1000 if not specified
    
    # Read DHCP start and end IPs
    dhcp_start = dc_info.get("dhcpStart")
    dhcp_end = dc_info.get("dhcpEnd")
    
    # DMZ configurations
    dmz_subnet = dc_info.get("DMZ")
    dmz_gateway = dc_info.get("DMZ_Gateway")
    dmz_vlan = dc_info.get("DMZ_Vlan")
    webserver_ips = dc_info.get("Webserver_IPs")
    dmz_ports = dc_info.get("DMZ_ports", "").split(",")
    
    if dc_name not in devices_conf:
        print(f"Error: {dc_name} section not found in devices.conf")
        return

    ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
    
    dhcp_config, dhcp_pool_size, available_hosts, backup_filename = generate_dhcp_config(
        dc_name, subnet, gateway, vlan, ports, interface_type, interface_speed, 
        ip_list, devices_conf, dhcp_start, dhcp_end, dmz_subnet, 
        dmz_gateway, dmz_vlan, webserver_ips, dmz_ports
    )
    
    # Display the result
    print("\n--- DHCP Configuration Summary ---")
    print(f"Data Center: {dc_name}")
    print(f"Subnet: {subnet}")
    print(f"Gateway: {gateway}")
    print(f"Available Hosts: {available_hosts}")
    print(f"Unique IPs for DHCP: {dhcp_pool_size}")
    print(f"DMZ Subnet: {dmz_subnet}")
    print(f"DMZ Gateway: {dmz_gateway}")
    print(f"DMZ VLAN: {dmz_vlan}")
    print(f"Webserver IP Range: {webserver_ips}")
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
