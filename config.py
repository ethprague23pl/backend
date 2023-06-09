from dotenv import load_dotenv

import os
load_dotenv()

PROJECT_URL = os.getenv("PROJECT_URL")
PUBLIC_API = os.getenv("PUBLIC_API")
DATABASE_PSWD = os.getenv("DATABASE_PSWD")
NFT_STORAGE_API = os.getenv('NFT_STORAGE_API')