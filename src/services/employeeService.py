from sqlalchemy.orm import Session
from src.models.employeeModel import Employee
from src.schemas.employeeSchema import EmployeeCreate


def create_employee(
    db: Session,
    employee: EmployeeCreate,
    documents_path: str,
    cheque_path: str,
    police_report_path,
    medical_report_path
):
    db_employee = Employee(
        full_name=employee.fullName,
        latest_qualification=employee.latestQualification,

        email=employee.email,
        phone_number=employee.phoneNumber,

        address=employee.address,
        city=employee.city,
        state=employee.state,
        postal_code=employee.postalCode,

        aadhar_name=employee.aadharName,
        aadhar_number=employee.aadharNumber,

        passport_number=employee.passportNumber,
        passport_validity=employee.passportValidity,

        pan_number=employee.panNumber,

        father_name=employee.fatherName,
        mother_name=employee.motherName,

        bank_account_holder_name=employee.bankAccountHolderName,
        bank_account_number=employee.bankAccountNumber,
        bank_ifsc_code=employee.bankIfscCode,
        bank_branch_name=employee.bankBranchName,

        emergency_contact_name=employee.emergencyContactName,
        emergency_contact_phone=employee.emergencyContactPhone,
        emergency_contact_email=employee.emergencyContactEmail,
        emergency_contact_relation=employee.emergencyContactRelation,

        hobbies=employee.hobbies,
        books_like_to_read=employee.booksLikeToRead,
        sports_you_play=employee.sportsYouPlay,
        favourite_artist=employee.favouriteArtist,
        favourite_cuisine=employee.favouriteCuisine,
        favourite_movies_bollywood=employee.favouriteMoviesBollywood,

        tshirt_size=employee.tshirtSize,
        shoe_size=employee.shoeSize,

        has_medical_insurance=employee.hasMedicalInsurance,
        medical_issues=employee.medicalIssues,
        police_verification=employee.policeVerification,
police_station=employee.policeStation,

siblings=employee.siblings,
local_guardian=employee.localGuardian,

medical_report_recent=employee.medicalReportRecent,

police_report_path=police_report_path,
medical_report_path=medical_report_path,

        documents_path=documents_path,
        cheque_path=cheque_path,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee