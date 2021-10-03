from starlette.config import Config

config = Config(".env")

DATABASE_URL: str = config("SQLALCH_DATABASE_URL")
YW_TOKEN: str = config("YW_TOKEN")
HOST: str = config("HOST")
