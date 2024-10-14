"""
Application definition
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def home():
    return JSONResponse({"message": "Hello world!"})


@app.get("/404")
async def missing():
    return JSONResponse({"error": "That's gonna be a 'no' from me."}, status_code=404)
