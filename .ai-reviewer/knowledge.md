# already reviewer notes

## Architecture

This is a small FastAPI Student Management System implemented entirely in `main.py`. It exposes CRUD, search, filtering, counting, and health-style endpoints over a module-level in-memory `students` list. Pydantic validates incoming student payloads through the `Student` model.

## Conventions

- Keep API routes grouped by purpose with clear section comments, as in `main.py` (`GET STUDENTS`, `CREATE STUDENT`, etc.).
- Student request fields are validated with Pydantic `Field` constraints in `main.py`: names and courses require at least two characters, and ages must be between 1 and 100.
- Collection responses use an envelope object, e.g. `{"students": results}` from `get_students()` and search/filter endpoints.
- Single-resource responses are also wrapped, e.g. `{"student": student}` in `get_student()`, while mutations include a human-readable `"message"` alongside the resource.
- IDs are integer values and are generated as one greater than the current maximum, using `default=0` for an empty collection (`create_student()`).
- Name search is case-insensitive substring matching (`search_student()`); course filtering is case-insensitive exact matching (`get_students_by_course()`).
- Missing student IDs consistently raise `HTTPException(status_code=404, detail="Student not found")` in get, update, and delete handlers.
- Route declarations must preserve the current ordering: static paths such as `/students/search`, `/students/course/{course_name}`, and `/students/count` appear before `/students/{student_id}` to avoid the dynamic ID route capturing them.

## Intentional non-standard choices

- Persistence is deliberately an in-memory module-level list (`students` in `main.py`), rather than a database or repository layer.
- IDs are assigned manually from the current maximum rather than via a database sequence.
- Endpoints return plain dictionaries without explicit response models; `Student` is used for request validation and mutation input only.
- Update is full replacement via `PUT`, requiring all `Student` fields rather than supporting partial updates.

## Watch out for

- Do not add a new `/students/{...}` route before the static search, course, or count routes; this can cause FastAPI routing conflicts or incorrect handler selection.
- Preserve case-insensitive behavior for name and course matching unless the API contract is intentionally changed.
- New mutation logic must update the shared `students` list so subsequent GET, count, and search requests observe the change.
- Do not silently return an empty or success response for unknown IDs; match the existing 404 behavior and exact error detail.
- Be cautious with ID generation: `max(...) + 1` is not safe for concurrent requests and can reuse IDs after deletion in some future implementations. Flag changes that imply production-grade persistence without addressing this limitation.