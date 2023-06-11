from dotenv import load_dotenv

import os
load_dotenv()

PROJECT_URL = os.getenv("PROJECT_URL")
PUBLIC_API = os.getenv("PUBLIC_API")
DATABASE_PSWD = os.getenv("DATABASE_PSWD")
NFT_STORAGE_API = os.getenv('NFT_STORAGE_API')
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXP_TIME = os.getenv("JWT_EXPIRATION_TIME_MINUTES")
SALT = os.getenv("SALT")
BASE_URL = os.getenv("BASE_URL")
HEADER ={'Content-Type': 'application/json'}
