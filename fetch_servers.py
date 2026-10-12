import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.gametracker.com/search/left4dead2/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_l4d2_servers():
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Request error: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    servers = []

    # GameTracker layout: look for IP strings like 123.45.67.89:27015
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b')

    rows = soup.find_all("tr")
    for row in rows:
        text = row.get_text()
        match = ip_pattern.search(text)
        if match:
            ip = match.group(0)
            # Find any link in row for server name
            link = row.find("a")
            name = link.text.strip() if link else "L4D2 Server"
            servers.append({"name": name, "ip": ip})

    return servers

if __name__ == "__main__":
    server_list = fetch_l4d2_servers()
    
    with open("servers.md", "w", encoding="utf-8") as f:
        f.write("# Active L4D2 Servers\n\n")
        if not server_list:
            f.write("No servers retrieved at this time.\n")
        else:
            for s in server_list:
                f.write(f"* **{s['name']}** — `connect {s['ip']}`\n")
                
    print(f"Successfully processed {len(server_list)} servers.")
