#This script is made for educational purposes and ethical ahcking purposes. Please, don't use this script for unethical purposes.
import argparse
import socket
import requests
from ipwhois import IPWhois
import json

def print_banner():
    banner = """
    ========================================================
    IP Information Gathering Toolkit
    Developer: Md Tawfique Elahey
    Description: Gather geolocation, WHOIS, ASN, and basic info for IP addresses.
    ========================================================
    """
    print(banner)

def get_geolocation(ip):
    try:
        url = f"http://ipinfo.io/{ip}/json"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return {
            "ip": ip,
            "country": data.get("country", "N/A"),
            "region": data.get("region", "N/A"),
            "city": data.get("city", "N/A"),
            "latitude": data.get("loc", "").split(',')[0] if "loc" in data else "N/A",
            "longitude": data.get("loc", "").split(',')[1] if "loc" in data else "N/A"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Error processing geolocation: {str(e)}"}

def get_whois_info(ip):
    try:
        ipwhois = IPWhois(ip)
        whois_info = ipwhois.lookup_rdap()
        network_info = whois_info.get('network', {})
        return {
            "network": {
                "name": network_info.get('name', 'N/A'),
                "handle": network_info.get('handle', 'N/A'),
                "country": network_info.get('country', 'N/A'),
                "abuse_contact": network_info.get('abuseContactEmail', 'N/A')
            }
        }
    except Exception as e:
        return {"error": f"Error retrieving WHOIS info: {str(e)}"}

def get_asn_info(ip):
    try:
        ipwhois = IPWhois(ip)
        asn_info = ipwhois.lookup_asn()
        return {
            "ASN": asn_info.get('asn', 'N/A'),
            "ASN Description": asn_info.get('asn_description', 'N/A'),
            "ASN Country": asn_info.get('country', 'N/A')
        }
    except Exception as e:
        return {"error": f"Error retrieving ASN info: {str(e)}"}

def get_basic_info(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        return {
            "ip": ip,
            "hostname": hostname[0],
            "city": "N/A",
            "region": "N/A",
            "country": "N/A"
        }
    except socket.herror:
        return {"error": "Unable to resolve IP hostname."}

def save_output(data, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\n[*] Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="IP Information Gathering Toolkit")
    parser.add_argument('-i', '--ip', required=True, help='Target IP address')
    parser.add_argument('--geolocation', action='store_true', help='Get geolocation info')
    parser.add_argument('--whois', action='store_true', help='Get WHOIS info')
    parser.add_argument('--asn', action='store_true', help='Get ASN info')
    parser.add_argument('--basic', action='store_true', help='Get basic IP info')
    parser.add_argument('--output', help='Save output to file (json)')
    
    args = parser.parse_args()

    ip = args.ip
    data = {}

    if args.geolocation:
        data["Geolocation"] = get_geolocation(ip)
    if args.whois:
        data["WHOIS"] = get_whois_info(ip)
    if args.asn:
        data["ASN"] = get_asn_info(ip)
    if args.basic:
        data["Basic Info"] = get_basic_info(ip)

    if data:
        for section, content in data.items():
            print(f"\n=== {section} ===")
            if isinstance(content, dict):
                for k, v in content.items():
                    print(f"{k}: {v}")
            else:
                print(content)

        if args.output:
            save_output(data, args.output)
    else:
        print("\n[*] No options selected. Please provide at least one option (geolocation, whois, asn, basic).")

if __name__ == "__main__":
    main()
