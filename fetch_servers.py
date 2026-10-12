import requests
from bs4 import BeautifulSoup

# GameTracker L4D2 URL
URL = "https://www.gametracker.com/search/left4dead2/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_l4d2_servers():
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    servers = []

    # Parse server table rows
    rows = soup.find_all("tr")
    for row in rows:
        ip_cell = row.find("td", class_="ip")
        name_cell = row.find("td", class_="name")
        
        if ip_cell and name_cell:
            ip = ip_cell.text.strip()
            name = name_cell.text.strip()
            servers.append({"name": name, "ip": ip})

    return servers

if __name__ == "__main__":
    server_list = fetch_l4d2_servers()
    with open("servers.md", "w") as f:
        f.write("# Active L4D2 Servers\n\n")
        if not server_list:
            f.write("No servers retrieved or page layout changed.\n")
        for s in server_list:
            f.write(f"* **{s['name']}** — `connect {s['ip']}`\n")
    print("Updated servers.md successfully!")
