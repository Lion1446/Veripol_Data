from bs4 import BeautifulSoup   ##pip3 install beautifulsoup4
import os
import requests                 ##pip3 install requests


def download(url: str, dest_folder: str, filename: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    file_path = os.path.join(dest_folder, filename)
    file_directory = "\\".join(file_path.split("\\")[:-1])
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
    r = requests.get(url, stream=True)
    if r.ok:
        print(f"saving to {os.path.abspath(file_path)}\n", )
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

f = open('Tentative Lists of Aspirants_Candidates __ Commission on Elections.html', 'r')
html_string = f.read()
f.close()
soup = BeautifulSoup(html_string, "html.parser")
links = soup.find_all(class_="subdivcont")
downloadables = []

for link in links:
    payload = {}
    payload[link.a.string] = link.a["href"]
    downloadables.append(payload)

links = soup.find_all(class_="ballottemplate")


for link in links:
    desc = list(link.descendants)
    for d in desc:
        if str(type(d)) == "<class 'bs4.element.NavigableString'>":
            pass
        else:
            if str(type(d.a)) == "<class 'bs4.element.Tag'>":
                payload = {}
                payload[d.a.string] = d.a["href"]
                downloadables.append(payload)

for i in range(len(downloadables)):
    print(f"{i+1}/{len(downloadables)}: {list(downloadables[i].values())[0]}")
    name = list(downloadables[i].values())[0]
    if "TentativeListsofCandidates" in name.split("/")[-3:]:
        filename = "\\".join(name.split("/")[-2:])
        filename = filename.replace("TentativeListsofCandidates", "NATIONAL")
    else:
        filename = "\\".join(name.split("/")[-3:])
    download(list(downloadables[i].values())[0], dest_folder="files", filename=filename)
    
