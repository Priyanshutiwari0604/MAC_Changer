# MAC Address Changer Tool

A professional, command-line Python tool for changing network interface MAC addresses on Linux and macOS systems. Built for cybersecurity professionals, penetration testers, and network administrators for educational and authorized testing purposes.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- **Change MAC Address**: Set custom MAC addresses for any network interface
- **Random MAC Generation**: Automatically generate valid, locally-administered MAC addresses
- **Interface Listing**: View all available network interfaces and their current MAC addresses
- **Automatic Verification**: Confirms successful MAC address changes
- **Colorized Output**: Beautiful, easy-to-read terminal interface
- **Input Validation**: Ensures MAC addresses follow proper formatting
- **Cross-Platform**: Supports both Linux and macOS operating systems
- **Safe & Compliant**: Generates locally-administered MAC addresses to avoid conflicts

## Requirements

- Python 3.6 or higher
- Linux or macOS operating system
- Root/sudo privileges
- Standard system utilities:
  - Linux: `ip` command
  - macOS: `ifconfig` command

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mac-address-changer.git
cd mac-address-changer
```

2. Make the script executable:
```bash
chmod +x mac_changer.py
```

3. Run with Python 3:
```bash
sudo python3 mac_changer.py [options]
```

## Usage

### Basic Commands

**List all network interfaces:**
```bash
sudo python3 mac_changer.py -l
```

**Show current MAC address:**
```bash
sudo python3 mac_changer.py -i eth0 -s
```

**Change to a specific MAC address:**
```bash
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

**Change to a random MAC address:**
```bash
sudo python3 mac_changer.py -i wlan0 -r
```

### Command-Line Options

```
-i, --interface    Network interface name (e.g., eth0, en0, wlan0)
-m, --mac          New MAC address (format: XX:XX:XX:XX:XX:XX)
-r, --random       Generate and set a random MAC address
-l, --list         List all available network interfaces
-s, --show         Show current MAC address of interface
-h, --help         Show help message
```

## Examples

### Example 1: Change MAC on Linux
```bash
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

### Example 2: Random MAC on macOS WiFi
```bash
sudo python3 mac_changer.py -i en0 -r
```

### Example 3: View all interfaces
```bash
sudo python3 mac_changer.py -l
```

## How It Works

1. **Validation**: Verifies the MAC address format and interface existence
2. **Current MAC Retrieval**: Reads the current MAC address from the interface
3. **Interface Down**: Temporarily disables the network interface (Linux only)
4. **MAC Change**: Applies the new MAC address using system commands
5. **Interface Up**: Re-enables the network interface (Linux only)
6. **Verification**: Confirms the MAC address was successfully changed

## Technical Details

### MAC Address Generation

The tool generates locally-administered MAC addresses by:
- Setting the second-least significant bit of the first octet to 1 (locally administered)
- Setting the least significant bit to 0 (unicast address)
- This ensures the MAC won't conflict with manufacturer-assigned addresses

### Platform-Specific Implementation

**Linux:**
- Uses `ip link` commands to manipulate interfaces
- Requires bringing interface down/up for changes

**macOS:**
- Uses `ifconfig` to change MAC addresses
- Automatically disassociates from WiFi networks when needed

## Important Notes

### Legal and Ethical Use

This tool is intended for:
- Educational purposes and learning
- Authorized penetration testing
- Network administration tasks
- Privacy protection on personal devices

**Warning:** Changing MAC addresses on networks you don't own or have permission to test may be illegal. Always obtain proper authorization before use.

### Limitations

- Requires root/sudo privileges
- Network connection will be temporarily interrupted during MAC change
- Some wireless adapters may not support MAC address changes
- Changes are typically not persistent across reboots

## Troubleshooting

**"Interface not found" error:**
- Verify the interface name using `-l` option
- Check interface spelling (case-sensitive)

**"Permission denied" error:**
- Run the script with `sudo`
- Ensure you have administrative privileges

**MAC change not persisting:**
- Changes are temporary and reset on reboot
- Consider using system-specific methods for persistent changes

**WiFi disconnection (macOS):**
- This is normal behavior when changing MAC on wireless interfaces
- Reconnect to your network after the change

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and authorized testing purposes only. The author is not responsible for any misuse or damage caused by this program. Users are responsible for complying with applicable laws and regulations in their jurisdiction.

## Author

[Your Name]
- GitHub: [Priyanshu Tiwari](https://github.com/Priyanshutiwari0604)
- LinkedIn: [Priyanshu Tiwari](https://www.linkedin.com/in/priyanshutiwari3006/)

## Acknowledgments

- Inspired by the need for simple, professional network testing tools
- Built with Python's standard library for maximum compatibility
- Thanks to the cybersecurity community for testing and feedback
