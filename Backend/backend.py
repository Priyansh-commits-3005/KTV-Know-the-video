import draft1 as d1

# print(d1.mainfunction("https://www.youtube.com/watch?v=9XaS93WMRQQ"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# Allow all origins for demonstration purposes. In a production environment, you should specify your frontend's domain.
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://www.youtube.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

URL = '';

@app.post("/api/results")
async def post_data(video_url: str):
    print("Received URL: ", video_url)
    try:
        URL = video_url
        print(URL)
        result = d1.mainfunction(URL)

        return {"status": "success", "message": "url received", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))