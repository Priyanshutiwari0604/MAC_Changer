#!/usr/bin/env python3
"""
MAC Address Changer Tool
A professional network interface MAC address manipulation tool for educational and authorized testing purposes.
Author: [Your Name]
"""

import subprocess
import re
import sys
import argparse
import random
import platform
import json
import os
import logging
from datetime import datetime
from typing import Optional, Tuple, Dict
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class MACChanger:
    """Main MAC Address Changer class"""
    
    def __init__(self):
        self.system = platform.system()
        if self.system not in ['Linux', 'Darwin']:
            self._error("This tool currently supports Linux and macOS only.")
            sys.exit(1)
    
    def _print_banner(self):
        """Display tool banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════╗
║           MAC ADDRESS CHANGER TOOL v1.0               ║
║        Network Interface MAC Manipulation             ║
║        For Educational & Authorized Testing           ║
╚═══════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def _success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}[+] {message}{Colors.END}")
    
    def _info(self, message: str):
        """Print info message"""
        print(f"{Colors.BLUE}[*] {message}{Colors.END}")
    
    def _warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}[!] {message}{Colors.END}")
    
    def _error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}[-] {message}{Colors.END}")
    
    def get_current_mac(self, interface: str) -> Optional[str]:
        """
        Retrieve the current MAC address of the specified interface
        
        Args:
            interface: Network interface name (e.g., eth0, en0)
        
        Returns:
            MAC address string or None if not found
        """
        try:
            if self.system == 'Darwin':  # macOS
                result = subprocess.check_output(['ifconfig', interface], 
                                                stderr=subprocess.DEVNULL)
            else:  # Linux
                result = subprocess.check_output(['ip', 'link', 'show', interface],
                                                stderr=subprocess.DEVNULL)
            
            result = result.decode('utf-8')
            
            # Search for MAC address pattern
            mac_pattern = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', result)
            
            if mac_pattern:
                return mac_pattern.group(0)
            else:
                return None
                
        except subprocess.CalledProcessError:
            self._error(f"Interface '{interface}' not found or no permission.")
            return None
        except Exception as e:
            self._error(f"Error getting MAC address: {str(e)}")
            return None
    
    def generate_random_mac(self) -> str:
        """
        Generate a random MAC address with locally administered bit set
        
        Returns:
            Random MAC address string
        """
        # Set the locally administered bit (second least significant bit of first octet)
        # This ensures the MAC is recognized as locally administered, not universally administered
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        mac[0] = (mac[0] & 0xfe) | 0x02  # Set locally administered, unicast
        
        return ':'.join(f'{octet:02x}' for octet in mac)
    
    def validate_mac(self, mac: str) -> bool:
        """
        Validate MAC address format
        
        Args:
            mac: MAC address string to validate
        
        Returns:
            True if valid, False otherwise
        """
        pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        return bool(pattern.match(mac))
    
    def change_mac(self, interface: str, new_mac: str) -> bool:
        """
        Change the MAC address of the specified interface
        
        Args:
            interface: Network interface name
            new_mac: New MAC address to set
        
        Returns:
            True if successful, False otherwise
        """
        if not self.validate_mac(new_mac):
            self._error("Invalid MAC address format. Use format: XX:XX:XX:XX:XX:XX")
            return False
        
        self._info(f"Changing MAC address for {interface} to {new_mac}")
        
        try:
            if self.system == 'Darwin':  # macOS
                # Disassociate from network (if WiFi)
                subprocess.run(['sudo', 'airport', '-z'], 
                             stderr=subprocess.DEVNULL, check=False)
                
                # Change MAC
                subprocess.run(['sudo', 'ifconfig', interface, 'ether', new_mac],
                             check=True, stderr=subprocess.PIPE)
                
            else:  # Linux
                # Bring interface down
                subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'],
                             check=True, stderr=subprocess.PIPE)
                
                # Change MAC
                subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'address', new_mac],
                             check=True, stderr=subprocess.PIPE)
                
                # Bring interface up
                subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'],
                             check=True, stderr=subprocess.PIPE)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self._error(f"Failed to change MAC address. Error: {e.stderr.decode() if e.stderr else 'Unknown'}")
            self._warning("Make sure you have sudo privileges.")
            return False
        except Exception as e:
            self._error(f"Unexpected error: {str(e)}")
            return False
    
    def list_interfaces(self):
        """List all available network interfaces"""
        self._info("Available network interfaces:")
        try:
            if self.system == 'Darwin':
                result = subprocess.check_output(['ifconfig', '-l'], 
                                                stderr=subprocess.DEVNULL)
                interfaces = result.decode('utf-8').strip().split()
            else:
                result = subprocess.check_output(['ip', 'link', 'show'],
                                                stderr=subprocess.DEVNULL)
                interfaces = re.findall(r'\d+: ([^:]+):', result.decode('utf-8'))
            
            for iface in interfaces:
                mac = self.get_current_mac(iface)
                if mac:
                    print(f"  • {iface:15} MAC: {mac}")
                else:
                    print(f"  • {iface:15} MAC: N/A")
                    
        except Exception as e:
            self._error(f"Error listing interfaces: {str(e)}")
    
    def verify_change(self, interface: str, expected_mac: str) -> bool:
        """
        Verify if MAC address was successfully changed
        
        Args:
            interface: Network interface name
            expected_mac: Expected MAC address
        
        Returns:
            True if MAC matches expected, False otherwise
        """
        current_mac = self.get_current_mac(interface)
        if current_mac and current_mac.lower() == expected_mac.lower():
            self._success(f"MAC address successfully changed to {current_mac}")
            return True
        else:
            self._error("MAC address change verification failed.")
            return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Professional MAC Address Changer Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i eth0 -m 00:11:22:33:44:55    Change MAC to specific address
  %(prog)s -i wlan0 -r                      Change MAC to random address
  %(prog)s -l                                List all network interfaces
  %(prog)s -i eth0 -s                        Show current MAC address

Note: This tool requires sudo/root privileges to change MAC addresses.
        """
    )
    
    parser.add_argument('-i', '--interface', 
                       help='Network interface name (e.g., eth0, en0, wlan0)')
    parser.add_argument('-m', '--mac', 
                       help='New MAC address (format: XX:XX:XX:XX:XX:XX)')
    parser.add_argument('-r', '--random', 
                       action='store_true',
                       help='Generate and set a random MAC address')
    parser.add_argument('-l', '--list', 
                       action='store_true',
                       help='List all available network interfaces')
    parser.add_argument('-s', '--show', 
                       action='store_true',
                       help='Show current MAC address of interface')
    
    args = parser.parse_args()
    
    # Initialize MAC changer
    changer = MACChanger()
    changer._print_banner()
    
    # List interfaces mode
    if args.list:
        changer.list_interfaces()
        sys.exit(0)
    
    # Require interface for other operations
    if not args.interface and not args.list:
        parser.print_help()
        sys.exit(1)
    
    # Show current MAC
    if args.show:
        current_mac = changer.get_current_mac(args.interface)
        if current_mac:
            changer._info(f"Current MAC address for {args.interface}: {current_mac}")
        sys.exit(0)
    
    # Get current MAC before changing
    old_mac = changer.get_current_mac(args.interface)
    if not old_mac:
        sys.exit(1)
    
    changer._info(f"Current MAC address: {old_mac}")
    
    # Determine new MAC address
    if args.random:
        new_mac = changer.generate_random_mac()
        changer._info(f"Generated random MAC: {new_mac}")
    elif args.mac:
        new_mac = args.mac
    else:
        changer._error("Please specify either -m/--mac or -r/--random")
        sys.exit(1)
    
    # Change MAC address
    if changer.change_mac(args.interface, new_mac):
        # Verify the change
        changer.verify_change(args.interface, new_mac)
    else:
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Operation cancelled by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[-] Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)
