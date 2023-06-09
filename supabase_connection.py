from supabase import create_client, Client
import json
import io
import requests as r 

from PIL import Image
from config import PROJECT_URL, PUBLIC_API, DATABASE_PSWD, NFT_STORAGE_API
from loguru import logger as LOG

def db_client():
    url: str = PROJECT_URL
    key: str = PUBLIC_API
    supabase: Client = create_client(url, key)
    return supabase


def upload_file_on_ipfs(file):
        api_key: str = NFT_STORAGE_API

        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        LOG.info("Uploading image to NFTStorage")

        resp = r.post(
            "https://api.nft.storage/upload",
            headers=headers,
            data=file,
        )

        if resp.status_code == 200:
            LOG.info("Image uploaded successfully")
            cid = resp.json()["value"]["cid"]
            link = f"https://{cid}.ipfs.nftstorage.link"
            LOG.info(f"Link to image is {link}")
            return link
        else:
            err = f"File upload failed with status code {resp.status_code}"
            LOG.exception(err)
            raise Exception(err)

def get_png(plik):
    image_bytes = io.BytesIO()
    template_image_path: str = plik
    template_image = Image.open(template_image_path)

    template_image.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    ipfs_url = upload_file_on_ipfs(image_bytes)
    return ipfs_url


#get_png('Gingnose_mammoth_d2c6feb5-e472-4620-a594-b7cdeb9a0325.png')