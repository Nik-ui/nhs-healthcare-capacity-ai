from dotenv import load_dotenv
import os

import psycopg


load_dotenv()


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is missing. Check your .env file.")

    return database_url


def connect():
    return psycopg.connect(get_database_url())