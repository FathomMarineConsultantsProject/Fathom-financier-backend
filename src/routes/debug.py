from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.db.database import get_db

router = APIRouter(prefix="/debug", tags=["Debug"])

@router.get("/dbinfo")
def dbinfo(db: Session = Depends(get_db)):
    dbname = db.execute(text("select current_database()")).scalar()
    user = db.execute(text("select current_user")).scalar()
    host = db.execute(text("select inet_server_addr()")).scalar()
    count = db.execute(text("select count(*) from employees")).scalar()
    return {"current_database": dbname, "current_user": user, "server_ip": str(host), "employees_count": count}