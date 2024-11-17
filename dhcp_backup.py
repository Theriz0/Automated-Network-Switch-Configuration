# backup_util.py
# Description: Utility functions for backing up configurations
# Author: Skandha Prakash

import datetime
import os

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