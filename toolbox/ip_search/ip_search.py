"""
Tool for looking up an IP's geographical location.
"""

import argparse
import requests

def get_parser():
    """Returns a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Look up the geographical location of an IP address.")
    parser.add_argument("ip", help="The IP address to look up.")
    return parser

def get_ip_location(ip_address, timeout=10):
    """ 
    Fetches the geo-location of a given IP address using the ip-api.com API. 
    """
    # Base URL for the IP API
    url = f"http://ip-api.com/json/{ip_address}"

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Ensures non-200 responses are caught as exceptions
        data = response.json()

        if data['status'] == 'success':
            return {
                'IP': data['query'],
                'Country': data['country'],
                'Region': data['regionName'],
                'City': data['city'],
                'ZIP': data['zip'],
                'Latitude': data['lat'],
                'Longitude': data['lon'],
                'ISP': data['isp']
            }
        else:
            # Handle error returned by the API
            return f"Error: {data.get('message', 'Lookup failed')}."

    except requests.RequestException as e:
        return f"Request error: {e}"

def main():
    """
    Main function to parse command-line arguments, look up the IP address location,
    and display the results.
    """
    parser = get_parser()
    args = parser.parse_args()

    # Fetch location data
    location_info = get_ip_location(args.ip)

    # Print location info or error message
    if isinstance(location_info, dict):
        for key, value in location_info.items():
            print(f"{key}: {value}")
    else:
        print(location_info)

if __name__ == "__main__":
    main()
