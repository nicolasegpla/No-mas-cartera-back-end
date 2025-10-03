from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",     # Para desarrollo local
    ],  # o ["*"] si estás en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def test(request: Request):
    print("Origin: ", request.headers.get("origin"))
    print("IP: ", request.client.host if request.client else "No client")
    return {"message": "Hola no mas cartera API!"}
