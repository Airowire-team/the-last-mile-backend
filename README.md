# Last Mile

Python microservices scaffold. The project-team and customer services have API
starters; other services and infrastructure files are placeholders.

## Run the project-team service

From the project root, run these commands in PowerShell:

```powershell
Set-Location .\services\project-team-service
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

On subsequent runs, only the last command is needed from the service directory.
This Python service does not use `npm run dev` or require a `package.json`.

- Health endpoint: <http://127.0.0.1:8000/health>
- Interactive API documentation: <http://127.0.0.1:8000/docs>

The health endpoint returns
`{"status":"ok","service":"project-team-service"}` and checks only that the API
is responding. It does not check PostgreSQL. Database access and team/member
endpoints are not yet implemented.

Keep credentials in local `.env` files, which are excluded from Git.

## Customer service status

From `services\customer-service\app`, run:

```powershell
Set-Location ..
python -m pip install -r requirements.txt
$env:PYTHONPATH = (Resolve-Path '..\..').Path
python -m uvicorn app.main:app --reload --port 8000
```

Running `python main.py` directly only imports the application; it does not
launch a server. The health endpoint is at <http://127.0.0.1:8000/health>.
Authentication is not implemented, so all booking endpoints return HTTP 503
until a real token verifier is configured.

The database session dependency reads `DATABASE_URL` from the process
environment when a session is first requested. To load the service's local
`.env` file when launching with Uvicorn, use `--env-file .env` from the service
directory. The database and booking table must already exist.