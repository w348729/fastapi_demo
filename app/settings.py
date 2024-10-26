import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(verbose=True)

env_path = Path('.')
load_dotenv(dotenv_path=env_path, verbose=True)

MONGODB_URL = os.getenv('MONGODB_URL')