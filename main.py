import uvicorn

from sys import argv
from app.utils.config import HOST

if __name__ == '__main__':`
    uvicorn.run("app.app:app", host=HOST, port=int(argv[1]), reload=True)
