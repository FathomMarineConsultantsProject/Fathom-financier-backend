from fastapi import FastAPI
from src.db.database import engine, Base
from src.routes.employeeRoutes import router as employee_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Fathom Employee API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(employee_router)

@app.get("/")
def health():
    return {"status": "running"}