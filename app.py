from fastapi import FastAPI
from src.db.database import engine, Base
from src.routes.employeeRoutes import router as employee_router
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from src.routes.debug import router as debug_router



app = FastAPI(title="Fathom Employee API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://fmc-employee-details-form.vercel.app", "https://fmc-employee-details-form-fmc-projects-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



try:
    Base.metadata.create_all(bind=engine)
except OperationalError as e:
    print("DB not ready:", e)

app.include_router(employee_router)
app.include_router(debug_router)

@app.get("/")
def health():
    return {"status": "running"}