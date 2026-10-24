from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=1, le=120)
    course: str = Field(min_length=1, max_length=100)
    date_of_birth: date


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=1, le=120)
    course: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: date | None = None


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    course: str
    date_of_birth: date | None