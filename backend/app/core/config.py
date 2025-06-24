# backend/app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv() # load from .env file

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")