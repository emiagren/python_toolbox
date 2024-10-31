"""
Search tool to lookup an IP:s geographical location.
"""

import requests

def get_ip_location(ip_address, timeout=10):
    """ 
    Fetches the geo-location of a given IP address using the ip-api.com API. 
    """
    # Base URL for the IP API
    url = f"http://ip-api.com/json/{ip_address}"

    try:
        # Make a GET request to the API
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Check if the request was successful

        # Parse the JSON response
        data = response.json()

        # Check if the API returned a success status
        if data['status'] == 'success':
            location_data = {
                'IP': data['query'],
                'Country': data['country'],
                'Region': data['regionName'],
                'City': data['city'],
                'ZIP': data['zip'],
                'Latitude': data['lat'],
                'Longitude': data['lon'],
                'ISP': data['isp']
            }
            return location_data
        else:
            # Handle error returned by the API
            return f"Error: {data['message']}"

    except requests.RequestException as e:
        # Handle any requests exceptions
        return f"Request error: {e}"

def main():
    """
    Main function to prompt the user for an IP address, look up its location,
    and display the results.
    """
    # Take IP address as user input
    ip = input("Enter an IP address to lookup: ")

    # Fetch and display the location info
    location_info = get_ip_location(ip)
    print(location_info)

# Run the main function
if __name__ == "__main__":
    main()
