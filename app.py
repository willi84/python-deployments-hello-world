"""
Application definition
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for your localhost (or any other domain you trust)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Can be a list of origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def home():
    return JSONResponse({"message": "Hello world!"})


@app.get("/404")
async def missing():
    return JSONResponse({"error": "That's gonna be a 'no' from me."}, status_code=404)
