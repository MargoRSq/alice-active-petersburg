import uvicorn

from sys import argv

if __name__ == '__main__':
    uvicorn.run("app.app:app", host=argv[2], port=int(argv[1]), reload=True)
