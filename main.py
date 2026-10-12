from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


# =========================
# STUDENT DATA MODEL
# =========================

class Student(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0, le=100)
    course: str = Field(min_length=2)


# =========================
# STUDENTS LIST
# =========================

students = [
    {
        "id": 1,
        "name": "Gouri",
        "age": 22,
        "course": "Python"
    },
    {
        "id": 2,
        "name": "Rohit",
        "age": 23,
        "course": "FastAPI"
    }
]


# =========================
# HOME API
# =========================

@app.get("/")
def home():
    return {
        "message": "Student Management System API is running"
    }


# =========================
# GET ALL STUDENTS
# =========================

@app.get("/students")
def get_students():
    return {
        "students": students
    }


# =========================
# SEARCH STUDENT BY NAME
# =========================

@app.get("/students/search")
def search_student(name: str):

    results = []

    for student in students:
        if name.lower() in student["name"].lower():
            results.append(student)

    return {
        "students": results
    }


# =========================
# FILTER STUDENTS BY COURSE
# =========================

@app.get("/students/course/{course_name}")
def get_students_by_course(course_name: str):

    results = []

    for student in students:
        if student["course"].lower() == course_name.lower():
            results.append(student)

    return {
        "course": course_name,
        "students": results
    }


# =========================
# STUDENT COUNT
# =========================

@app.get("/students/count")
def get_student_count():

    return {
        "total_students": len(students)
    }


# =========================
# GET STUDENT BY ID
# =========================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return {
                "student": student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# =========================
# CREATE STUDENT
# =========================

@app.post("/students")
def create_student(student: Student):

    new_id = max(
        [student["id"] for student in students],
        default=0
    ) + 1

    new_student = {
        "id": new_id,
        "name": student.name,
        "age": student.age,
        "course": student.course
    }

    students.append(new_student)

    return {
        "message": "Student created successfully",
        "student": new_student
    }


# =========================
# UPDATE STUDENT
# =========================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: Student
):

    for existing_student in students:

        if existing_student["id"] == student_id:

            existing_student["name"] = student.name
            existing_student["age"] = student.age
            existing_student["course"] = student.course

            return {
                "message": "Student updated successfully",
                "student": existing_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# =========================
# DELETE STUDENT
# =========================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully",
                "student": student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )