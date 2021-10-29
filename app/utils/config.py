from starlette.config import Config

config = Config(".env")

DATABASE_URL: str = config("SQLALCH_DATABASE_URL")
HOST: str = config("HOST")