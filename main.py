import uvicorn

from app.utils.config import HOST
from app.utils.config import PORT

if __name__ == '__main__':
    uvicorn.run("app.app:app", host=HOST, port=PORT, reload=True)
