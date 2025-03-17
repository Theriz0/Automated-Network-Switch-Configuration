# Leaf and Spine Network Configuration 4.0

## Description

This program automates the configuration of leaf switches within a leaf-spine network architecture, tailored for specific data centers. It generates DHCP configurations, VLAN settings, and interface configurations based on data center-specific parameters defined in `switch.conf` and `devices.conf`.

Key features include:

* **Data Center Specific Configurations:** Supports multiple data centers with distinct configurations for subnets, VLANs, gateways, and device-specific settings.
* **DHCP Automation:** Generates DHCP pool configurations, including address ranges and exclusions, based on defined subnets.
* **VLAN and Interface Configuration:** Configures VLANs and interfaces with specified speeds and access modes.
* **DMZ Configuration:** Integrates DMZ configurations for web servers, including IP ranges, VLANs, and port assignments.
* **Application Server Configuration:** Sets up application server VLANs, IP ranges, and port assignments.
* **Device-Specific Settings:** Allows for configuring device types, allowed protocols, and IP reservations.
* **Backup Functionality:** Automatically backs up generated configurations to a timestamped file in the `backup` directory.
* **Gateway Configuration:** Supports DHCP, DMZ, and Application Gateway configurations.
* **Network Calculation:** Calculates DHCP pool size and available hosts for each subnet.
* **Comprehensive Logging:** Provides detailed summaries of the generated configurations and backup status.

## How to Run the Program

1.  **Ensure Configuration Files Exist:**
    * `switch.conf`: Contains data center-specific network configurations (subnets, VLANs, gateways, etc.).
    * `devices.conf`: Contains device-specific information (IPs, device types, allowed protocols).
2.  **Run the Script:**
    * Open a terminal or command prompt.
    * Navigate to the directory containing `build_switch.py`.
    * Execute the script with the desired data center name as an argument:

    ```bash
    python build_switch.py <DC_NAME>
    ```

    Replace `<DC_NAME>` with the name of the data center as defined in your configuration files (e.g., `DC_NY`, `DC_DA`).

## Configuration Files

### `switch.conf`

This file contains the general network configurations for each data center.
