from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from models import Student
from schemas import StudentCreate, StudentResponse, StudentUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student CRUD API",
    description="A simple student management backend built with FastAPI and SQLite.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "Student CRUD API is running", "docs": "/docs"}


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists.",
        )
    return student


@app.get("/students", response_model=list[StudentResponse], tags=["Students"])
def list_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    search: str | None = Query(default=None, min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    statement = select(Student).order_by(Student.id).offset(skip).limit(limit)
    if search:
        statement = (
            select(Student)
            .where(
                Student.name.ilike(f"%{search}%")
                | Student.email.ilike(f"%{search}%")
                | Student.course.ilike(f"%{search}%")
            )
            .order_by(Student.id)
            .offset(skip)
            .limit(limit)
        )
    return db.scalars(statement).all()


@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@app.patch("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="Provide at least one field to update.")

    for field, value in updates.items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists.",
        )
    return student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
