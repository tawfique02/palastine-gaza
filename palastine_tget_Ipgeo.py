# Don't use it unethically and maintain copyrigt issues.
# Don't copy my style.
import argparse
import socket
import requests
from ipwhois import IPWhois
import json

# Banner for the toolkit
def print_banner():
    banner = """
    ========================================================
    IP Information Gathering Toolkit
    Developer: Md Tawfique Elahey
    Description: Gather geolocation, WHOIS, ASN, and basic info for IP addresses.
    This tool is made for Muslim Ummah.
    ========================================================
    """
    print(banner)

# Function to get Geolocation data
def get_geolocation(ip):
    try:
        url = f"http://ipinfo.io/{ip}/json"
        response = requests.get(url)
        data = response.json()
        geolocation_info = {
            "ip": ip,
            "country": data.get("country", "N/A"),
            "region": data.get("region", "N/A"),
            "city": data.get("city", "N/A"),
            "latitude": data.get("loc", "").split(',')[0] if "loc" in data else "N/A",
            "longitude": data.get("loc", "").split(',')[1] if "loc" in data else "N/A"
        }
        return geolocation_info
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to get WHOIS data
def get_whois_info(ip):
    try:
        ipwhois = IPWhois(ip)
        whois_info = ipwhois.lookup_rdap()
        network_info = whois_info.get('network', {})
        whois_data = {
            "network": {
                "name": network_info.get('name', 'N/A'),
                "handle": network_info.get('handle', 'N/A'),
                "country": network_info.get('country', 'N/A'),
                "abuse_contact": network_info.get('abuseContactEmail', 'N/A')
            }
        }
        return whois_data
    except Exception as e:
        return {"error": str(e)}

# Function to get ASN data
def get_asn_info(ip):
    try:
        ipwhois = IPWhois(ip)
        asn_info = ipwhois.lookup_asn()
        asn_data = {
            "ASN": asn_info.get('asn', 'N/A'),
            "ASN Description": asn_info.get('asn_description', 'N/A'),
            "ASN Country": asn_info.get('country', 'N/A')
        }
        return asn_data
    except Exception as e:
        return {"error": str(e)}

# Function to get basic IP info
def get_basic_info(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        basic_info = {
            "ip": ip,
            "hostname": hostname[0],
            "city": "N/A",  # You can add more IP-to-location mapping if needed
            "region": "N/A",
            "country": "N/A"
        }
        return basic_info
    except socket.herror:
        return {"error": "Unable to resolve IP hostname."}

# Function to save the gathered information to a JSON file
def save_output(data, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\n[*] Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")

# Main function to run the tool
def main():
    print_banner()
    
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="IP Information Gathering Toolkit",
        epilog="Example: python3 ip_info_toolkit.py -i 8.8.8.8 --geolocation --whois --asn --basic --output result.json"
    )
    parser.add_argument('-i', '--ip', required=True, help='Target IP address')
    parser.add_argument('--geolocation', action='store_true', help='Get geolocation info')
    parser.add_argument('--whois', action='store_true', help='Get WHOIS info')
    parser.add_argument('--asn', action='store_true', help='Get ASN info')
    parser.add_argument('--basic', action='store_true', help='Get basic IP info')
    parser.add_argument('--output', help='Save output to file (json)')

    args = parser.parse_args()

    ip = args.ip
    data = {}

    # Gathering IP Information
    if args.geolocation:
        data["Geolocation"] = get_geolocation(ip)
    
    if args.whois:
        data["WHOIS"] = get_whois_info(ip)
    
    if args.asn:
        data["ASN"] = get_asn_info(ip)
    
    if args.basic:
        data["Basic Info"] = get_basic_info(ip)
    
    # Output the gathered information
    if data:
        for section, content in data.items():
            print(f"\n=== {section} ===")
            if isinstance(content, dict):
                for k, v in content.items():
                    print(f"{k}: {v}")
            else:
                print(content)

        # Save to file if requested
        if args.output:
            save_output(data, args.output)

    else:
        print("\n[*] No options selected. Please provide at least one option (geolocation, whois, asn, basic).")

if __name__ == "__main__":
    main()
#[Allahu Akber]
