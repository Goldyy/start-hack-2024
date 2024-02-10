# This is the main file to run the frontend of the application

from dotenv import load_dotenv

from hackathon.src.backend.main import start_backend
from hackathon.src.frontend.main import start_frontend

load_dotenv()

start_frontend()
start_backend()
