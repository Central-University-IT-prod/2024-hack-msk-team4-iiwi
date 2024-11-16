import os

from dotenv import load_dotenv

load_dotenv()

MONGO_DSN = os.environ.get("MONGO_DSN")
MTS_API_URL = os.environ.get("MTS_API_URL")
MTS_API_PASSWORD = os.environ.get("MTS_API_PASSWORD")
MTS_API_LOGIN = os.environ.get("MTS_API_LOGIN")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.environ.get("ALGORITHM")
SECURITY_KEY = os.environ.get("SECURITY_KEY")