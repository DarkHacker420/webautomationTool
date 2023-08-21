#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse
from pathlib import Path

# Colors Output
NORMAL = "\e[0m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BOLD = "\033[01;01m"
WHITE = "\033[1;37m"
YELLOW = "\033[1;33m"
LRED = "\033[1;31m"
LGREEN = "\033[1;32m"
LBLUE = "\033[1;34m"
LCYAN = "\033[1;36m"
SORANGE = "\033[0;33m"
DGRAY = "\033[1;30m"
DSPACE = "  "
DTAB = "\t\t"
TSPACE = "   "
TTAB = "\t\t\t"
QSPACE = "    "
QTAB = "\t\t\t\t"
BLINK = "\e[5m"
TICK = "\u2714"
CROSS = "\u274c"

# Check if the script is run as root. If not, then exit.
if os.geteuid() != 0:
    print(
        f"{YELLOW}[!] {LRED}{BOLD}This script must be run as root{NORMAL}",
        file=sys.stderr,
    )
    sys.exit(1)

# Initialize variables
domain = ""
output = ""
excl = ""
threads = ""
bServer = ""
onlysub = ""

# Banner
def banner():
    print(
        f"\n{BOLD}{LRED}"
        "▓█████▄ ▄▄▄      ██▀███  ██ ▄█▀ ██████ ██░ ██ ▄▄▄     ▓█████▄ ▒█████  █     █░ \n"
        "▒██▀ ██▒████▄   ▓██ ▒ ██▒██▄█▒▒██    ▒▓██░ ██▒████▄   ▒██▀ ██▒██▒  ██▓█░ █ ░█░ \n"
        "░██   █▒██  ▀█▄ ▓██ ░▄█ ▓███▄░░ ▓██▄  ▒██▀▀██▒██  ▀█▄ ░██   █▒██░  ██▒█░ █ ░█ \n"
        "░▓█▄   ░██▄▄▄▄██▒██▀▀█▄ ▓██ █▄  ▒   ██░▓█ ░██░██▄▄▄▄██░▓█▄   ▒██   ██░█░ █ ░█ \n"
        "░▒████▓ ▓█   ▓██░██▓ ▒██▒██▒ █▒██████▒░▓█▒░██▓▓█   ▓██░▒████▓░ ████▓▒░░██▒██▓ \n"
        "▒▒▓  ▒ ▒▒   ▓▒█░ ▒▓ ░▒▓▒ ▒▒ ▓▒ ▒▓▒ ▒ ░▒ ░░▒░▒▒▒   ▓▒█░▒▒▓  ▒░ ▒░▒░▒░░ ▓░▒ ▒  \n"
        "░ ▒  ▒  ▒   ▒▒ ░ ░▒ ░ ▒░ ░▒ ▒░ ░▒  ░ ░▒ ░▒░ ░ ▒   ▒▒ ░░ ▒  ▒  ░ ▒ ▒░  ▒ ░ ░  \n"
        "░ ░  ░  ░   ▒    ░░   ░░ ░░ ░░  ░  ░  ░  ░░ ░ ░   ▒   ░ ░  ░░ ░ ░ ▒   ░   ░  \n"
        "░         ░  ░  ░    ░  ░        ░  ░  ░  ░     ░  ░  ░       ░ ░     ░ \n"
        f"\n{NORMAL}{BOLD}{QTAB}{DTAB}{QSPACE}  [●] {BLINK}{LGREEN}@DarkShadow{DGRAY} | {LGREEN}G!2m0{NORMAL}\n"
    )
    print(
        f"{NORMAL}\n[{CROSS}] {NORMAL}Warning: Use with caution. You are responsible for your own actions.{NORMAL}"
    )
    print(
        f"[{CROSS}] {NORMAL}Developers assume no liability and are not responsible for any misuse or damage caused by "
        f"this tool.{NORMAL}\n"
    )


# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="DARKSHADOW - Web Application Enumeration and Vulnerability Scanning Tool"
    )
    parser.add_argument("-d", dest="domain", required=True, help="Domain to scan")
    parser.add_argument("-o", dest="output", required=True, help="Output directory")
    parser.add_argument(
        "-e", dest="excl", required=False, help="List of subdomains to exclude"
    )
    parser.add_argument(
        "-t",
        dest="threads",
        required=False,
        default="50",
        help="Number of threads (default: 50)",
    )
    parser.add_argument(
        "-bs",
        dest="bServer",
        required=False,
        help="IP or hostname of Burp Suite Collaborator server",
    )
    parser.add_argument(
        "-os",
        dest="onlysub",
        required=False,
        help="File containing only subdomains to scan",
    )

    args = parser.parse_args()

    global domain
    global output
    global excl
    global threads
    global bServer
    global onlysub

    domain = args.domain
    output = args.output
    excl = args.excl
    threads = args.threads
    bServer = args.bServer
    onlysub = args.onlysub


# Create output directory and set up log file
def setup_output():
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output):
            os.makedirs(output)

        # Set up the log file
        log_file = os.path.join(output, "darkshadow.log")
        with open(log_file, "w") as f:
            f.write("DarkShadow Log\n")
            f.write("Domain: " + domain + "\n")
            f.write("Output Directory: " + output + "\n")
            f.write("Excluded Subdomains: " + excl + "\n")
            f.write("Threads: " + threads + "\n")
            f.write("Burp Suite Collaborator Server: " + bServer + "\n")
            f.write("Only Subdomains File: " + onlysub + "\n")
            f.write("\n")

        return log_file
    except Exception as e:
        print(
            f"[{CROSS}] {RED}Error setting up output directory and log file: {str(e)}{NORMAL}",
            file=sys.stderr,
        )
        sys.exit(1)


# Run the assetfinder tool to find subdomains
def run_assetfinder():
    try:
        assetfinder_cmd = f"assetfinder -subs-only {domain} > {output}/assetfinder.txt"
        subprocess.run(
            assetfinder_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"[{CROSS}] {RED}Error running assetfinder: {e.stderr}{NORMAL}",
            file=sys.stderr,
        )
        sys.exit(1)


# Exclude subdomains specified in the exclusion list
def exclude_subdomains():
    try:
        if excl:
            with open(excl, "r") as f:
                excluded_subdomains = f.read().splitlines()

            if excluded_subdomains:
                assetfinder_output = os.path.join(output, "assetfinder.txt")
                with open(assetfinder_output, "r") as f:
                    subdomains = f.read().splitlines()

                # Remove excluded subdomains from the list
                subdomains = [
                    subdomain
                    for subdomain in subdomains
                    if subdomain not in excluded_subdomains
                ]

                # Write the updated list to the assetfinder output file
                with open(assetfinder_output, "w") as f:
                    f.write("\n".join(subdomains))
    except Exception as e:
        print(
            f"[{CROSS}] {RED}Error excluding subdomains: {str(e)}{NORMAL}",
            file=sys.stderr,
        )


# Run httprobe to identify live subdomains
def run_httprobe():
    try:
        assetfinder_output = os.path.join(output, "assetfinder.txt")
        httprobe_output = os.path.join(output, "httprobe.txt")
        httprobe_cmd = f"cat {assetfinder_output} | httprobe -threads {threads} -c 50 > {httprobe_output}"
        subprocess.run(
            httprobe_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"[{CROSS}] {RED}Error running httprobe: {e.stderr}{NORMAL}",
            file=sys.stderr,
        )
        sys.exit(1)


# Run nuclei with default templates
def run_nuclei_default():
    try:
        httprobe_output = os.path.join(output, "httprobe.txt")
        nuclei_default_output = os.path.join(output, "nuclei_default_output")
        nuclei_default_cmd = f"nuclei -l {httprobe_output} -t ~/nuclei-templates -o {nuclei_default_output} -no-color"
        subprocess.run(
            nuclei_default_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"[{CROSS}] {RED}Error running nuclei with default templates: {e.stderr}{NORMAL}",
            file=sys.stderr,
        )
        sys.exit(1)


# Run nuclei with custom templates
def run_nuclei_custom():
    try:
        httprobe_output = os.path.join(output, "httprobe.txt")
        nuclei_custom_output = os.path.join(output, "nuclei_custom_output")
        nuclei_custom_cmd = f"nuclei -l {httprobe_output} -t ~/custom-nuclei-templates -o {nuclei_custom_output} -no-color"
        subprocess.run(
            nuclei_custom_cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"[{CROSS}] {RED}Error running nuclei with custom templates: {e.stderr}{NORMAL}",
            file=sys.stderr,
        )
        sys.exit(1)


# Main function
def main():
    banner()
    parse_arguments()
    log_file = setup_output()
    run_assetfinder()
    exclude_subdomains()
    run_httprobe()
    run_nuclei_default()
    run_nuclei_custom()
    print(
        f"[{TICK}] {GREEN}WebCoPilot scan completed. Results saved in {output}{NORMAL}"
    )


if __name__ == "__main__":
    main()
