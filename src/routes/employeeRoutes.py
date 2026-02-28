import json
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.employeeSchema import EmployeeCreate
from src.services.employeeService import create_employee
from src.services.storage import (
    save_file,
    DOC_DIR,
    CHEQUE_DIR,
    DOC_MAX,
    CHEQUE_MAX,
)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/create")
async def create_employee_api(
    data: str = Form(...),
    documentsFile: UploadFile = File(...),
    bankCancelledCheque: UploadFile = File(...),
    policeReportFile: UploadFile | None = File(None),
    medicalReportFile: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):

    # ✅ Parse JSON data
    try:
        parsed_data = EmployeeCreate(**json.loads(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ✅ Save mandatory files
    documents_path = await save_file(documentsFile, DOC_DIR, DOC_MAX)
    cheque_path = await save_file(bankCancelledCheque, CHEQUE_DIR, CHEQUE_MAX)

    # ✅ Save optional files
    police_report_path = None
    medical_report_path = None

    if policeReportFile:
        police_report_path = await save_file(policeReportFile, DOC_DIR, DOC_MAX)

    if medicalReportFile:
        medical_report_path = await save_file(medicalReportFile, DOC_DIR, DOC_MAX)

    # ✅ Create employee in DB
    employee = create_employee(
        db,
        parsed_data,
        documents_path,
        cheque_path,
        police_report_path,
        medical_report_path,
    )

    return {
        "message": "Employee created successfully",
        "id": employee.id,
    }