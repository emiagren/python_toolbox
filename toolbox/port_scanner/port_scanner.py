"""
Nmap port scanner with TCP, service, OS detection, and vulnerability scanning.
"""

import argparse
import datetime
import nmap

def get_parser():
    """Returns a command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="""
        A network scanner using Nmap for TCP connect, 
        service/version detection, OS detection, and vulnerability scanning.
        """
        )
    parser.add_argument("host", help="The IP address or hostname to scan.")
    parser.add_argument(
        "scan_type", 
        choices=["tcp", "service", "os", "vuln"],
        help="Scan type: 'tcp', 'service', 'os', or 'vuln'."
        )
    parser.add_argument("--ports", help="Specify a port range (e.g., '20-80') for 'tcp' scan only.")
    return parser

def save_to_file(host, scan_type, content):
    """Helper to save scan results to a file with a dynamic filename."""
    filename = f"{host}_{scan_type}_scan.txt"
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content)
        f.write("\n" + "="*50 + "\n\n")

def perform_scan(scanner, host, arguments, scan_type):
    """Performs a scan with specified arguments and returns results."""
    print(f"Performing {scan_type.capitalize()} Scan on {host} with arguments: {arguments}...")
    scanner.scan(host, arguments=arguments)

    if not scanner[host].all_protocols():
        return "No open ports or services found.\n"

    result = f"{scan_type.capitalize()} Scan Results for {host} - {datetime.datetime.now().replace(microsecond=0)}\n"
    for proto in scanner[host].all_protocols():
        result += f"Protocol: {proto}\n"
        ports = scanner[host][proto].keys()
        for port in sorted(ports):
            details = scanner[host][proto][port]
            result += f"Port: {port}, State: {details['state']}"
            if 'name' in details:
                result += f", Service: {details['name']}"
            if 'version' in details:
                result += f", Version: {details.get('version', 'N/A')}"
            result += "\n"
    return result

def tcp_connect_scan(scanner, host, port_range):
    """Performs a TCP Connect Scan (-sT)."""
    arguments = f"-sT -p {port_range}" if port_range else "-sT -p 1-65535"
    result = perform_scan(scanner, host, arguments, "TCP Connect")
    save_to_file(host, "tcp_connect", result)
    print(result)

def service_version_detection(scanner, host):
    """Performs a Service and Version Detection Scan (-sV)."""
    result = perform_scan(scanner, host, "-sV", "Service and Version Detection")
    save_to_file(host, "service_version", result)
    print(result)

def os_scan(scanner, host):
    """Performs an OS Detection Scan (-O) and adds OS-specific output."""
    result = perform_scan(scanner, host, "-O", "OS Detection")
    if 'osclass' in scanner[host]:
        result += "OS Details:\n"
        for osclass in scanner[host]['osclass']:
            result += f"OS: {osclass['osfamily']} {osclass.get('osgen', '')}, Accuracy: {osclass['accuracy']}%\n"
    save_to_file(host, "os_detection", result)
    print(result)

def vulnerability_scan(scanner, host):
    """Performs a Vulnerability Scan using Nmap scripts (--script vuln)."""
    print(f"Performing Vulnerability Scan on {host}...")
    scanner.scan(host, arguments="--script vuln")

    result = f"Vulnerability Scan Results for {host} - {datetime.datetime.now().replace(microsecond=0)}\n"
    if 'hostscript' in scanner[host]:
        for script in scanner[host]['hostscript']:
            result += f"Script: {script['id']}, Output: {script['output']}\n"
    else:
        result += "No vulnerabilities found.\n"

    save_to_file(host, "vulnerability", result)
    print(result)

def main():
    """Main function to parse arguments and initiate scans."""
    parser = get_parser()
    args = parser.parse_args()

    scanner = nmap.PortScanner()

    try:
        if args.scan_type == "tcp":
            tcp_connect_scan(scanner, args.host, args.ports)
        elif args.scan_type == "service":
            service_version_detection(scanner, args.host)
        elif args.scan_type == "os":
            os_scan(scanner, args.host)
        elif args.scan_type == "vuln":
            vulnerability_scan(scanner, args.host)
    except nmap.PortScannerError as e:
        print(f"Scan error: {e}")
    except KeyError:
        print("Scan failed. Host might be unreachable or scan type is unsupported by the target.")

if __name__ == '__main__':
    main()
