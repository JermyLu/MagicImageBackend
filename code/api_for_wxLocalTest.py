import json
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/test")
async def status(data: dict):
    print(data)
    return "test test test"

if __name__ == '__main__':
    # uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="./key.pem", ssl_certfile="./cert.pem")
    uvicorn.run(app, port=8080)
