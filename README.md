<<<<<<< HEAD
# wil-project
=======
APEX Procurement (JSON-backed) — Run instructions

Backend (Flask)
----------------
cd backend
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="..."            # or set in environment
export AZURE_OPENAI_ENDPOINT="https://your-azure-endpoint"
export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
export APEX_DB_PATH="./data/db.json"  # optional

python -m app.main

Frontend (React + Vite)
-----------------------
cd frontend
npm install
# optionally set VITE_API_BASE_URL in .env or export
npm run dev  # opens at http://localhost:5173

Notes
-----
- The backend default port is 8000. The frontend expects API at http://localhost:8000 unless VITE_API_BASE_URL is set.
- The JSON DB file is at data/db.json and is auto-created.
- Agent uses OpenAI via Azure function-calling when configured; otherwise a simple fallback parser is used.
>>>>>>> c2e9f86 (Commit)
