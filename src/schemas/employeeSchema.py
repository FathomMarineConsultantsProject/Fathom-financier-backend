from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


class EmployeeCreate(BaseModel):
    fullName: str = Field(min_length=2)
    latestQualification: str = Field(min_length=2)

    email: EmailStr
    phoneNumber: str = Field(min_length=10)

    address: str = Field(min_length=5)
    city: str = Field(min_length=2)
    state: str = Field(min_length=2)
    postalCode: str = Field(min_length=4, max_length=10)

    aadharName: str = Field(min_length=2)
    aadharNumber: str = Field(min_length=12, max_length=12)

    passportNumber: Optional[str] = None
    passportValidity: Optional[str] = None

    panNumber: str = Field(min_length=5)

    fatherName: str = Field(min_length=2)
    motherName: str = Field(min_length=2)

    # ✅ New family fields
    siblings: str = Field(min_length=1)
    localGuardian: str = Field(min_length=1)

    bankAccountHolderName: str = Field(min_length=2)
    bankAccountNumber: str = Field(min_length=6, max_length=18)
    bankIfscCode: str = Field(min_length=5)
    bankBranchName: str = Field(min_length=2)

    emergencyContactName: str = Field(min_length=2)
    emergencyContactPhone: str = Field(min_length=10)
    emergencyContactEmail: EmailStr
    emergencyContactRelation: str = Field(min_length=2)

    hobbies: str = Field(min_length=2)
    booksLikeToRead: str = Field(min_length=2)
    sportsYouPlay: str = Field(min_length=2)
    favouriteArtist: str = Field(min_length=2)
    favouriteCuisine: str = Field(min_length=2)
    favouriteMoviesBollywood: str = Field(min_length=2)

    tshirtSize: Literal["XS", "S", "M", "L", "XL", "XXL"]
    shoeSize: str = Field(min_length=1)

    # ✅ Police verification
    policeVerification: Literal["yes", "no"]
    policeStation: Optional[str] = None

    # ✅ Medical
    hasMedicalInsurance: Literal["yes", "no"]
    medicalReportRecent: Literal["yes", "no"]
    medicalIssues: Optional[str] = None