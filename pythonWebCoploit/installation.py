import os
import subprocess
import urllib.request
import shutil
import zipfile


def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        exit(1)


def download_file(url, destination):
    try:
        urllib.request.urlretrieve(url, destination)
    except Exception as e:
        print(f"Error downloading file: {e}")
        exit(1)


def main():
    if os.geteuid() != 0:
        print("This script must be run as root")
        print("Make sure you're root before installing the tools")
        exit(1)

    os.system("clear")
    home_dir = os.path.expanduser("~")
    tools_dir = os.path.join(home_dir, "tools")
    temp_dir = os.path.join(tools_dir, "temp")
    gf_dir = os.path.join(home_dir, ".gf")
    wordlists_dir = os.path.join(home_dir, "wordlists")
    payloads_dir = os.path.join(wordlists_dir, "payloads")

    os.makedirs(tools_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(gf_dir, exist_ok=True)
    os.makedirs(wordlists_dir, exist_ok=True)
    os.makedirs(payloads_dir, exist_ok=True)

    print("Installing all dependencies")
    run_command("sudo apt-get install git -y 2> /dev/null")
    run_command("sudo apt-get install python3 -y 2> /dev/null")
    run_command("sudo apt-get install python3-pip -y 2> /dev/null")
    run_command("sudo apt-get install ruby -y 2> /dev/null")
    run_command("sudo apt-get install golang-go -y 2> /dev/null")
    run_command("sudo apt install snapd -y 2> /dev/null")
    run_command("sudo apt install cmake -y 2> /dev/null")
    run_command("sudo apt install jq -y 2> /dev/null")
    run_command("sudo apt install gobuster -y 2> /dev/null")
    run_command("sudo snap install chromium 2> /dev/null")
    run_command("sudo apt-get install -y parallel 2> /dev/null")

    print("Installing python tools")
    os.chdir(home_dir)
    run_command("git clone https://github.com/aboul3la/Sublist3r.git ~/tools/Sublist3r")
    os.chdir("~/tools/Sublist3r")
    run_command("sudo pip3 install -r requirements.txt 2> /dev/null")
    os.chdir(home_dir)
    run_command(
        "git clone https://github.com/sqlmapproject/sqlmap.git ~/tools/sqlmap/ 2> /dev/null"
    )
    os.chdir(home_dir)
    run_command(
        "git clone https://github.com/ameenmaali/urldedupe.git ~/tools/urldedupe"
    )
    os.chdir("~/tools/urldedupe")
    run_command("cmake CMakeLists.txt")
    run_command("make")
    run_command("mv urldedupe /usr/bin/ 2> /dev/null")
    os.chdir(home_dir)
    run_command(
        "git clone https://github.com/devanshbatham/OpenRedireX.git ~/tools/OpenRedireX"
    )
    os.chdir("~/tools/OpenRedireX")
    run_command("sudo pip3 install -r requirements.txt")
    os.chdir("~/tools/")
    run_command(
        "wget https://github.com/findomain/findomain/releases/latest/download/findomain-linux"
    )
    run_command("chmod +x findomain-linux")
    run_command("mv findomain-linux /usr/bin/findomain 2> /dev/null")

    print("Installing Wordlists & Payloads")
    os.chdir(wordlists_dir)
    download_file(
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt",
        "big.txt",
    )
    download_file(
        "https://gist.githubusercontent.com/Lopseg/33106eb13372a72a31154e0bbab2d2b3/raw"
        "/a79331799a70d0ae0ea906f2b143996d85f71de5/dicc.txt",
        "dicc.txt",
    )
    download_file(
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/dns-Jhaddix.txt",
        "dns.txt",
    )
    download_file(
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/deepmagic.com-prefixes"
        "-top50000.txt",
        "subdomains.txt",
    )
    download_file(
        "https://raw.githubusercontent.com/janmasarik/resolvers/master/resolvers.txt",
        "resolvers.txt",
    )
    download_file(
        "https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt", "fuzz.txt"
    )
    os.chdir(payloads_dir)
    download_file(
        "https://github.com/R0X4R/Garud/edit/master/payloads/lfi.txt", "lfi.txt"
    )

    print("Installing go-lang tools")
    run_command("go get -u github.com/tomnomnom/anew 2> /dev/null")
    run_command("go get -u github.com/tomnomnom/gf 2> /dev/null")
    run_command("go get github.com/michenriksen/aquatone 2> /dev/null")
    run_command("go get -u github.com/tomnomnom/assetfinder 2> /dev/null")
    run_command("GO111MODULE=on go get -u -v github.com/bp0lr/gauplus 2> /dev/null")
    run_command(
        "GO111MODULE=on go get -v github.com/projectdiscovery/httpx/cmd/httpx 2> /dev/null"
    )
    run_command("go get -v github.com/OWASP/Amass/v3/... 2> /dev/null")
    run_command("go get github.com/tomnomnom/waybackurls 2> /dev/null")
    run_command("go get github.com/Emoe/kxss 2> /dev/null")
    run_command("go get github.com/haccer/subjack 2> /dev/null")
    run_command("go get -u github.com/tomnomnom/qsreplace 2> /dev/null")
    os.chdir(temp_dir)
    run_command("git clone https://github.com/projectdiscovery/dnsx.git")
    os.chdir("dnsx/cmd/dnsx")
    run_command("go build")
    run_command("mv dnsx /usr/bin/ &> /dev/null")
    os.chdir(temp_dir)
    run_command("git clone https://github.com/hahwul/dalfox")
    os.chdir("dalfox")
    run_command("go install 2> /dev/null")
    os.chdir(temp_dir)
    run_command("git clone https://github.com/dwisiswant0/crlfuzz")
    os.chdir("crlfuzz/cmd/crlfuzz")
    run_command("go build .")
    run_command("sudo mv crlfuzz /usr/bin/ 2> /dev/null")
    os.chdir(temp_dir)
    run_command("git clone")


if __name__ == "__main__":
    main()
