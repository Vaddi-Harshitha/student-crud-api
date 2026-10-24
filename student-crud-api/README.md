# Student CRUD API

A student management REST API built with Python, FastAPI, SQLAlchemy, and SQLite.

## Features

- Create, list, search, retrieve, update, and delete student records
- Validate email addresses, required fields, age, and date of birth
- Prevent duplicate email addresses
- Support pagination using `skip` and `limit`
- Interactive API documentation using Swagger UI
- Store student records in SQLite

## Technology Stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- SQLite

## Project Structure

The current development setup contains a virtual environment in the outer project folder and Python source files in the inner folder.

```text
student-crud-api/
├── .venv/
└── student-crud-api/
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── requirements.txt
    ├── README.md
    └── students.db
```

## Installation and Setup

Open PowerShell in the outer project folder containing `.venv` and the inner `student-crud-api` folder.

Install the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r .\student-crud-api\requirements.txt
```

## Run the API

Start the server on port 8001:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir .\student-crud-api --port 8001 --reload
```

Keep the terminal open while the server is running. To stop it, press `Ctrl+C`.

Open these URLs in your browser:

- Swagger API documentation: http://127.0.0.1:8001/docs
- Health check: http://127.0.0.1:8001/

## API Endpoints

| Method | Endpoint | Purpose | Success Status |
|---|---|---|---|
| GET | `/` | Check API status | 200 OK |
| POST | `/students` | Create a student | 201 Created |
| GET | `/students` | List students | 200 OK |
| GET | `/students/{student_id}` | Retrieve one student | 200 OK |
| PATCH | `/students/{student_id}` | Update selected fields | 200 OK |
| DELETE | `/students/{student_id}` | Delete a student | 204 No Content |

## Example: Create a Student

In Swagger UI, expand `POST /students`, click **Try it out** if available, and submit:

```json
{
  "name": "Test Student",
  "email": "test.student@example.com",
  "age": 21,
  "course": "Computer Science",
  "date_of_birth": "2005-04-15"
}
```

Use synthetic test data only. The email must be valid, age must be within the accepted range, and date of birth must use `YYYY-MM-DD` format.

## Search and Pagination

The `GET /students` endpoint supports:

- `search`: search by student name, email, or course
- `skip`: number of records to skip
- `limit`: maximum number of records to return

Example:

`GET /students?search=computer&skip=0&limit=20`

## Testing with Swagger UI

1. Start the API.
2. Open http://127.0.0.1:8001/docs.
3. Expand the endpoint you want to test.
4. Click **Try it out** if shown. If **Cancel** and **Reset** are visible, it is already in editing mode.
5. Enter the required parameters and request body.
6. Click **Execute** and check the response status and body.

Common response codes:

- `200 OK`: Request succeeded.
- `201 Created`: Student was created.
- `204 No Content`: Student was deleted.
- `404 Not Found`: Student does not exist.
- `409 Conflict`: Email address is already in use.
- `422 Unprocessable Entity`: Request data failed validation.

The API testing report records the manual test cases and their observed results. Include genuine Swagger screenshots if required by the assignment.

## Dependencies

All required Python packages are listed in `requirements.txt`. Install them using the command in the Installation section.

## Database and Privacy

The application uses SQLite. The database location depends on the database URL in `database.py` and the working directory used to start the server.

Do not delete or replace existing database files unless you have confirmed that they contain no data you need. Do not publish real student personal information, passwords, or secrets.

## Optional AI Extension Ideas

These are optional future enhancements, not part of the core CRUD functionality:

- Course recommendations using a trusted course catalogue
- Plain-language summaries with appropriate authorization
- Natural-language search over permitted student fields

Do not send identifiable student information to an external AI provider without appropriate authorization and safeguards.

## GitHub Submission Checklist

- [ ] Include the Python source files.
- [ ] Include `requirements.txt` and this `README.md`.
- [ ] Exclude `.venv/`, Python cache folders, secrets, and real student data.
- [ ] Check whether `students.db` should be excluded from a public repository.
- [ ] Include the testing report and any required genuine screenshots.
- [ ] Verify the setup and run instructions before submission.
