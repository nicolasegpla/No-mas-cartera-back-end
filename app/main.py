from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.routers import clientes, facturas, abonos, auth_empresa

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

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(facturas.router, prefix="/facturas", tags=["Facturas"])
app.include_router(abonos.router, prefix="/abonos", tags=["Abonos"])
app.include_router(auth_empresa.router, prefix="/auth", tags=["Autenticación Empresa"])