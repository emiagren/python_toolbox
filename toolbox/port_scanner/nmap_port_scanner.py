"""
Nmap port scanner
"""

import nmap
import datetime

def save_to_file(filename, content):
    """Function to save scan results to file."""
    with open(filename, 'a') as f:
        f.write(content)
        f.write("\n" + "="*50 + "\n\n")

def tcp_connect_scan(scanner, host):
    """Performs a TCP connect scan (-sT) and prints the state of each port."""
    range_choice = input("Do you want to scan all ports (1-65535) or a specific range? (all/range): ").lower()
    
    if range_choice == 'range':
        port_range = input("Enter the port range (e.g., 20-80): ")
        arguments = f"-sT -p {port_range}"
    else:
        arguments = "-sT -p 1-65535"

    print(f"Performing TCP Connect Scan on {host} with arguments: {arguments}...")
    scanner.scan(host, arguments=arguments)
    
    result = f"TCP Connect Scan Results for {host} - {datetime.datetime.now().replace(microsecond=0)}\n"
    
    if not scanner[host].all_protocols():
        result += "No ports found.\n"
    else:
        for proto in scanner[host].all_protocols():
            result += f"Protocol: {proto}\n"
            ports = scanner[host][proto].keys()
            for port in sorted(ports):
                state = scanner[host][proto][port]['state']
                result += f"Port: {port}, State: {state}\n"

    print(result)
    save_to_file(f"{host}_tcp_connect_scan.txt", result)

def service_version_detection(scanner, host):
    """Performs a service and version detection scan (-sV) and prints the service and version."""
    print(f"Performing Service and Version Detection Scan on {host}...")
    scanner.scan(host, arguments='-sV')
    
    result = f"Service and Version Detection Scan Results for {host} - {datetime.datetime.now().replace(microsecond=0)}\n"
    
    if not scanner[host].all_protocols():
        result += "No services found.\n"
    else:
        for proto in scanner[host].all_protocols():
            result += f"Protocol: {proto}\n"
            ports = scanner[host][proto].keys()
            for port in sorted(ports):
                service = scanner[host][proto][port]['name']
                version = scanner[host][proto][port].get('version', 'N/A')
                result += f"Port: {port}, Service: {service}, Version: {version}\n"
    
    print(result)
    save_to_file(f"{host}_service_version.txt", result)

def os_scan(scanner, host):
    """Performs an OS detection scan (-O) and prints the hostname and OS information."""
    print(f"Performing OS Detection Scan on {host}...")
    scanner.scan(host, arguments='-O')
    
    result = f"OS Detection Scan Results for {host} - {datetime.datetime.now().replace(microsecond=0)}\n"
    
    hostname = scanner[host].hostname()
    result += f"Hostname: {hostname}\n"
    
    if 'osclass' in scanner[host]:
        for osclass in scanner[host]['osclass']:
            result += f"OS Type: {osclass['osfamily']}, OS Version: {osclass['osgen']}, Accuracy: {osclass['accuracy']}%\n"
    else:
        result += "Could not detect OS information.\n"
    
    print(result)
    save_to_file(f"{host}_os_scan.txt", result)

def vulnerability_scan(scanner, host):
    """Performs a vulnerability scan using Nmap's script engine (--script vuln)."""
    print(f"Performing Vulnerability Scan on {host}...")
    scanner.scan(host, arguments='--script vuln')
  
    result = f"Vulnerability Scan Results for {host} 
    - {datetime.datetime.now().replace(microsecond=0)}\n"

    if 'hostscript' in scanner[host]:
        for script in scanner[host]['hostscript']:
            result += f"Script: {script['id']}, Output: {script['output']}\n"
    else:
        result += "No vulnerabilities found.\n"

    print(result)
    save_to_file(f"{host}_vulnerability_scan.txt", result)

def main():
    scanner = nmap.PortScanner()
    host = input("Enter the IP address or hostname to scan: ")

    while True:
        print("\n--- Nmap Scan Menu ---")
        print("1. TCP Connect Scan")
        print("2. Service and Version Detection")
        print("3. OS Detection Scan")
        print("4. Vulnerability Scan")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            tcp_connect_scan(scanner, host)
        elif choice == '2':
            service_version_detection(scanner, host)
        elif choice == '3':
            os_scan(scanner, host)
        elif choice == '4':
            vulnerability_scan(scanner, host)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
