from app.api.server import app
from app.utils.config import Config
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)