## Event Planner API

FastAPI-based REST API for managing events and users. Provides user signup/signin with JWT auth and CRUD for events backed by MongoDB via Beanie ODM.

### Features
- User signup and signin with hashed passwords
- JWT-based authentication (Bearer tokens)
- CRUD endpoints for events
- MongoDB storage using Beanie (motor + Pydantic models)
- Docker and Docker Compose support
- Pytest with example tests

---

### Prerequisites
- Python 3.10+
- MongoDB (local or container)
- Docker & Docker Compose (optional, for containerized run)

---

### Environment Variables
The app reads settings via Pydantic `BaseSettings` from an env file.

- `DATABASE_URL` (required): Mongo connection string including default DB name, e.g. `mongodb://localhost:27017/planner`
- `SECRET_KEY` (required): Secret used to sign JWTs

Local development uses `.env` by default (`database/connection.py` Config sets `env_file = ".env"`).

For Compose, `.env.prod` is referenced in `docker-compose.yml` and should include the same variables. The repo ignores `.env.prod` by default.

Example `.env`:
```env
DATABASE_URL=mongodb://localhost:27017/planner
SECRET_KEY=change-this-in-production
```

---

### Installation (Local)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # if you create one; otherwise create .env using the example above
```

Run the API locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

Interactive docs:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

---

### Run with Docker Compose
`docker-compose.yml` defines two services: `api` and `database` (MongoDB). Ensure `.env.prod` exists with `DATABASE_URL` pointing to the Mongo container and `SECRET_KEY` set.

Example `.env.prod`:
```env
DATABASE_URL=mongodb://database:27017/planner
SECRET_KEY=please-rotate-and-keep-secret
```

Build and run:
```bash
docker compose up --build
```

API will be available at `http://localhost:8080`.

---

### API Endpoints

Base URL: `/`

Auth: Bearer token for protected event mutations. Obtain via signin.

#### User
- `POST /user/signup`
  - Body (JSON): `{ "email": "user@example.com", "password": "strong-pass" }`
  - Responses: `200` `{ "message": "User created successfully" }`, `409` on duplicate email

- `POST /user/signin`
  - Form (x-www-form-urlencoded): `username=<email>&password=<password>`
  - Response: `200` `{ "access_token": "...", "token_type": "Bearer" }`

#### Events
- `GET /event/`
  - Response: `200` `List[Event]`

- `GET /event/{id}`
  - Response: `200` `Event`, `404` if not found

- `POST /event/new` (requires auth)
  - Headers: `Authorization: Bearer <token>`
  - Body (JSON) example:
    ```json
    {
      "title": "FastAPI Book Launch",
      "image": "https://example.com/image.png",
      "description": "Book discussion",
      "tags": ["python", "fastapi"],
      "location": "Google Meet"
    }
    ```
  - Response: `200` `{ "message": "Event created successfully" }`

- `PUT /event/{id}` (requires auth; only creator can update)
  - Headers: `Authorization: Bearer <token>`
  - Body: Partial fields from Event
  - Responses: `200` `Event`, `400` if not owner, `404` if not found

- `DELETE /event/{id}` (requires auth; only creator can delete)
  - Headers: `Authorization: Bearer <token>`
  - Responses: `200` `{ "message": "Event deleted successfully." }`, `400`, `404`

- `DELETE /event/` (unprotected, clears in-memory list)

---

### Testing
Run tests with pytest:
```bash
pytest -q
```

Coverage (if configured):
```bash
pytest --cov=.
coverage html  # open htmlcov/index.html
```

The `.coverage` file is ignored by Git.

---

### Notes
- CORS is currently wide open (`*`) in `main.py`. Restrict in production.
- JWT uses HS256 with `SECRET_KEY`; ensure strong, rotated secrets.
- Ensure `DATABASE_URL` includes a default database name for Beanie initialization.


