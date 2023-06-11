import requests as r
from loguru import logger as LOG
from config import NFT_STORAGE_API


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