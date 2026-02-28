from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    latest_qualification = Column(String, nullable=False)

    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    aadhar_name = Column(String, nullable=False)
    aadhar_number = Column(String, nullable=False)

    passport_number = Column(String, nullable=True)
    passport_validity = Column(String, nullable=True)

    pan_number = Column(String, nullable=False)

    father_name = Column(String, nullable=False)
    mother_name = Column(String, nullable=False)

    # ✅ New family fields
    siblings = Column(String, nullable=False)
    local_guardian = Column(String, nullable=False)

    bank_account_holder_name = Column(String, nullable=False)
    bank_account_number = Column(String, nullable=False)
    bank_ifsc_code = Column(String, nullable=False)
    bank_branch_name = Column(String, nullable=False)

    emergency_contact_name = Column(String, nullable=False)
    emergency_contact_phone = Column(String, nullable=False)
    emergency_contact_email = Column(String, nullable=False)
    emergency_contact_relation = Column(String, nullable=False)

    hobbies = Column(String, nullable=False)
    books_like_to_read = Column(String, nullable=False)
    sports_you_play = Column(String, nullable=False)
    favourite_artist = Column(String, nullable=False)
    favourite_cuisine = Column(String, nullable=False)
    favourite_movies_bollywood = Column(String, nullable=False)

    tshirt_size = Column(String, nullable=False)
    shoe_size = Column(String, nullable=False)

    # ✅ Police
    police_verification = Column(String, nullable=False)
    police_station = Column(String, nullable=True)
    police_report_path = Column(String, nullable=True)

    # ✅ Medical
    has_medical_insurance = Column(String, nullable=False)
    medical_report_recent = Column(String, nullable=False)
    medical_report_path = Column(String, nullable=True)
    medical_issues = Column(String, nullable=True)

    # ✅ File paths
    documents_path = Column(String, nullable=False)
    cheque_path = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())