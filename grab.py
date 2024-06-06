import os
import requests
import pyrfc6266
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

baseModelID = "366990"
modelURL = f"https://civitai.com/api/v1/models/{baseModelID}?token={os.environ['CIVITAPIKEY']}"

response = requests.get(modelURL)
response_json = response.json()


def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    fileName = pyrfc6266.requests_response_to_filename(response)
    head = response.headers
    if os.path.exists(os.path.join(dest_path, fileName)):
        print(f"File {fileName} already exists")
        downloadSize = str(head.get("Content-Length"))
        fileSize = str(os.path.getsize(os.path.join(dest_path, fileName)))
        print(downloadSize + " vs " + fileSize)
        if downloadSize == fileSize:
            print(f"File {fileName} already downloaded")
            return
    if response.status_code == 200:
        with open(os.path.join(dest_path, fileName), 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {url} to {dest_path}")
    else:
        print(f"Failed to download {url}: {response.status_code}")


def create_path_for_download(type, baseName):
    return os.path.join(type, baseName)



links = []
for version in response_json["modelVersions"]:
    path = create_path_for_download(version["baseModel"], response_json["name"])
    links.append({"link": version["downloadUrl"]+f"?token={os.environ['CIVITAPIKEY']}", "path": path, "name":version["name"]})
    print(f'{version["name"]} {version["id"]} {version["downloadUrl"]}')
print(links)

def download_links(_links, dest_dir):
    for link in tqdm(_links, desc="Downloading files"):
        print(link)
        filepath = os.path.join(os.getcwd(), 'Downloads', dest_dir, link["path"].replace("/", "\\"))
        print(filepath)
        os.makedirs(filepath, exist_ok=True)
        download_file(link["link"], filepath)

download_links(links, "test")
