# Python Toolbox
This Python Toolbox provides a command-line interface to easily manage and run various utility tools, each contained within its own folder. The main script displays a menu of available tools, allowing users to select and execute the main function of each tool. 
All scripts can be run as a standalone script.

## Features
- **Dynamic Tool Loading**: Automatically detects tools based on folder structure, without hardcoding each tool.
- **Simple Menu Interface**: Presents a numbered menu for selecting and running each tool.
- **Customizable Tools**: Each tool resides in a subfolder with its own Python file, which can be extended with additional functionality as needed.

## Requirements

To run the tools in this toolbox, you’ll need the following:

1. **Python 3** - Ensure Python is installed on your system.
2. **External Libraries and Modules**:
    - **cryptography** - Used for encryption and decryption functions in `crypto_tool.py`.
    - **hashlib** - Used for hashing in `hash_cracker.py`.
    - **requests** - For handling the api call in `ip_search.py`  
    - **nmap** - Used for scanning in port_scanner.py

## Installation
1. Clone this repo to your local machine  
`git clone https://github.com/emiagren/python_toolbox.git`
2. Install the required libraries  
`pip install -r requirements.txt`
3. Run the main script:  
`python toolbox_main.py`

## Usage
- **Run the toolbox main script**:  
   `python toolbox_main.py`  
- **Run a tool independantly**:  
    `python tool_name.py`  
- **Add a new tool** by creating a subfolder in the `toolbox` directory, naming it `tool_name`, and including a `tool_name.py` file with a `main()` function.

<br>
<br>

# Crypto Tool
This script provides a command-line tool to generate a key, encrypt files, and decrypt them using symmetric encryption with Python's `cryptography` library.

## Usage (independantly)
1. **Generate a Key**:  
   `python crypto_tool.py generate_key`  
2. **Encrypt or Decrypt a file**:  
   `python crypto_tool.py encrypt <filename> <keyfile>` 
   `python crypto_tool.py decrypt <filename.encrypted> <keyfile>`

<br>
<br>

# Hash Cracker 
A Python script to brute-force crack hashed passwords using a wordlist. This script takes a target hash and a wordlist file as input, hashes each word in the wordlist, and checks for a match with the target hash. It supports multiple hashing algorithms (default: SHA-256).

## Usage
1. To run the script independantly:    
`python hash_cracker.py`
1. Enter the hashed password.
2. Enter the path to the wordlist file. (e.g. wordlist.txt)
3. Enter the hashing algorithm (default is sha256).

<br>
<br>

# IP Search
This Python script allows you to look up the geographical location of an IP address using the ip-api.com API. The script takes an IP address as user input and provides location details such as the country, region, city, ZIP code, latitude, longitude, and ISP if available. It handles common errors and provides specific messages if the IP address is private, reserved, or not found in the database.

## Usage
1. To run the script independantly:  
`python ip_search.py`  
Enter an IP address when prompted. (e.g 8.8.8.8.)  

<br>
<br>

# Port Scanner  
This Python script provides a simple interface to perform various network scans on a specified host using Nmap. Users can get information about open ports, service versions, operating system details, and potential vulnerabilities. Each scan result is printed to the console and saved to a file with a time stamp for easy reference.

## Features
- TCP Connect Scan (-sT): Checks the state of each port (open, closed, filtered, etc.) and allows scanning either all ports or a specific range.
- Service and Version Detection (-sV): Identifies the service and version running on each open port.
- OS Detection Scan (-O): Detects the hostname and operating system of the target host.
- Vulnerability Scan (--script vuln): Uses Nmap's vulnerability scripts to check for known vulnerabilities.

## Usage
1. To run the script independantly:  
`python nmap_scanner.py`  
2. Enter the IP address or hostname of the target.
3. Select a scan option from the menu.
<br>

The scan results will be displayed in the console and saved to a corresponding .txt file in the script's directory.
<br>

This script is intended for ethical and authorized network scanning only. Ensure you have permission before scanning any network or host.