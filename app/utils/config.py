from starlette.config import Config

config = Config("../.env")

DATABASE_URL: str = config("SQLALCH_DATABASE_URL")

YW_TOKEN: str = config("YW_TOKEN")

# GS_CLIENT_ID: str = config("GS_CLIENT_ID")
# GS_CLIENT_SECRET: str = config("GS_CLIENT_SECRET")
# GMAIL: str = config("GMAIL")