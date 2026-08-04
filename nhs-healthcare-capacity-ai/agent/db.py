from dotenv import load_dotenv
import os
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import psycopg


load_dotenv()


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is missing. Check your .env file.")

    parsed = urlparse(database_url)
    query = dict(parse_qsl(parsed.query))

    if query.get("sslmode") == "verify-full" and "sslrootcert" not in query:
        query["sslrootcert"] = "system"
        database_url = urlunparse(parsed._replace(query=urlencode(query)))

    return database_url


def connect():
    return psycopg.connect(get_database_url())
