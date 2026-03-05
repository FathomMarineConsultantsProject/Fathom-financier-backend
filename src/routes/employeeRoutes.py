import json
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.db.database import get_db
from src.models.employeeModel import Employee
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


@router.get("")
def get_all_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)

    # ✅ Search across common fields
    if q and q.strip():
        search = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Employee.full_name.ilike(search),
                Employee.email.ilike(search),
                Employee.phone_number.ilike(search),
                Employee.aadhar_number.ilike(search),
                Employee.pan_number.ilike(search),
                Employee.city.ilike(search),
                Employee.state.ilike(search),
            )
        )

    total = query.count()

    employees = (
        query.order_by(Employee.created_at.desc())  # ✅ newest first
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    total_pages = (total + limit - 1) // limit

    return {
        "items": [
            {
                "id": e.id,
                "full_name": e.full_name,
                "latest_qualification": e.latest_qualification,
                "email": e.email,
                "phone_number": e.phone_number,
                "city": e.city,
                "state": e.state,
                "created_at": e.created_at,
            }
            for e in employees
        ],
        "page": page,
        "limit": limit,
        "total": total,
        "totalPages": total_pages,
    }


@router.get("/{employee_id}")
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # ✅ Full profile (based on your Employee model)
    return {
        "id": emp.id,
        "full_name": emp.full_name,
        "latest_qualification": emp.latest_qualification,
        "email": emp.email,
        "phone_number": emp.phone_number,

        "address": emp.address,
        "city": emp.city,
        "state": emp.state,
        "postal_code": emp.postal_code,

        "aadhar_name": emp.aadhar_name,
        "aadhar_number": emp.aadhar_number,

        "passport_number": emp.passport_number,
        "passport_validity": emp.passport_validity,

        "pan_number": emp.pan_number,

        "father_name": emp.father_name,
        "mother_name": emp.mother_name,

        "siblings": emp.siblings,
        "local_guardian": emp.local_guardian,

        "bank_account_holder_name": emp.bank_account_holder_name,
        "bank_account_number": emp.bank_account_number,
        "bank_ifsc_code": emp.bank_ifsc_code,
        "bank_branch_name": emp.bank_branch_name,

        "emergency_contact_name": emp.emergency_contact_name,
        "emergency_contact_phone": emp.emergency_contact_phone,
        "emergency_contact_email": emp.emergency_contact_email,
        "emergency_contact_relation": emp.emergency_contact_relation,

        "hobbies": emp.hobbies,
        "books_like_to_read": emp.books_like_to_read,
        "sports_you_play": emp.sports_you_play,
        "favourite_artist": emp.favourite_artist,
        "favourite_cuisine": emp.favourite_cuisine,
        "favourite_movies_bollywood": emp.favourite_movies_bollywood,

        "tshirt_size": emp.tshirt_size,
        "shoe_size": emp.shoe_size,

        "police_verification": emp.police_verification,
        "police_station": emp.police_station,
        "police_report_path": emp.police_report_path,

        "has_medical_insurance": emp.has_medical_insurance,
        "medical_report_recent": emp.medical_report_recent,
        "medical_report_path": emp.medical_report_path,
        "medical_issues": emp.medical_issues,

        "documents_path": emp.documents_path,
        "cheque_path": emp.cheque_path,

        "created_at": emp.created_at,
    }