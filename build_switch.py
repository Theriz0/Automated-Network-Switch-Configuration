# Description: imports all the necessary DHCP config from dhcp_config.py 
# and runs it as part of the main workflow

# Author: Skandha Prakash
# Version: 2.0

import configparser
import sys
from dhcp_config import generate_dhcp_config

def main(dc_name):
    # Load configurations
    switch_conf = configparser.ConfigParser()
    devices_conf = configparser.ConfigParser()
    switch_conf.read("switch.conf")
    devices_conf.read("devices.conf")
    
    if dc_name not in switch_conf:
        print(f"Error: {dc_name} section not found in switch.conf")
        return

    dc_info = switch_conf[dc_name]
    subnet = dc_info.get("NY_subnet")
    vlan = dc_info.get("Vlan")
    ports = dc_info.get("Ports", "").split(",")
    interface_type = dc_info.get("InterfaceType", "GigabitEthernet")
    interface_speed = dc_info.get("InterfaceSpeed", "1000")  # Default speed to 1000 if not specified
    dhcp_snooping = dc_info.getboolean("DHCP_Snooping", False)
    
    if dc_name not in devices_conf:
        print(f"Error: {dc_name} section not found in devices.conf")
        return

    ip_list = devices_conf[dc_name].get("IPs", "").split(", ")
    
    dhcp_config, dhcp_pool_size, available_hosts, backup_filename = generate_dhcp_config(
        dc_name, subnet, vlan, ports, interface_type, interface_speed, dhcp_snooping, ip_list
    )
    
    # Display the result
    print("\n--- DHCP Configuration Summary ---")
    print(f"Data Center: {dc_name}")
    print(f"Subnet: {subnet}")
    print(f"Available Hosts: {available_hosts}")
    print(f"Unique IPs for DHCP: {dhcp_pool_size}")
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
