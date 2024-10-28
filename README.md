# Leaf and Spine Network Configuration 1.2
Description: This program is utilized to build leaf switch with data-center specific IP subnet and DHCP IP pool for end-user devices.

How to run the program:
python build_switch.py <DC_NAME>

Version 1.0:
Basis for the auto configuration where every device IP and subnetted IP belong to a particualr vlan. An automated python Script was added to pull both device.conf and switch.conf in order to properly take in the /24 subnet in consideration in order to properly provide each gig interface its specified IP address, gateway and lease time for a DHCP network.

Version 1.1:
Changed the interface to port interface so the user can choose what ports they can use for going with either Fastethernet or GigabitEthernet interfaces on switch.conf and updated the python script to take in the interface types for FastEthernet or GigabitEthernet for each port determined by the user in ordwer to help the user give more modular options for making the configuration. 

Version 1.2:
Added DHCP snooping for enhanced security to clearly monitor traffic just in case a rouge DHCP server can intercept traffic and disrupt traffic. Added DHCP snooping boolean logic for both the switch.conf and the python script to detect which ports need DHCP snooping and which ports dont need creating a highest privilege choice for the user depending on the configured ports.
