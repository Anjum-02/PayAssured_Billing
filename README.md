# PayAssured – Invoice Recovery Case Tracker (Sample Implementation)
...
See README inside for full instructions.
⚙️ Setup Instructions (Run the Project)

This project has two parts:

- **Backend → FastAPI (Python)**
- **Frontend → Node.js (Express + EJS)**

Follow the steps below exactly to run the project locally.

---

## 🟦 1️⃣ Backend Setup (FastAPI – Python)

### Step 1 — Go to the backend folder
```bash
cd backend
Step 2 — Create a virtual environment
bash
Copy code
python -m venv .venv
Step 3 — Activate the environment (Windows PowerShell)
bash
Copy code
.\.venv\Scripts\Activate.ps1
Step 4 — Install backend dependencies
bash
Copy code
pip install -r requirements.txt
Step 5 — Start the FastAPI backend server
bash
Copy code
uvicorn app:app --reload --port 8000
✔ Backend will now run at:
API Docs → http://127.0.0.1:8000/docs

Base URL → http://127.0.0.1:8000

🟩 2️⃣ Frontend Setup (Node.js – Express)
Step 1 — Go to the frontend folder
bash
Copy code
cd frontend
Step 2 — Install dependencies
bash
Copy code
npm install
Step 3 — Set backend API URL
bash
Copy code
$env:BACKEND_URL = "http://127.0.0.1:8000"
Step 4 — Start the frontend server
bash
Copy code
npm start
✔ Frontend will now run at:
http://localhost:3000

🟧 3️⃣ Database Setup
SQLite (Default)
No setup required.
The file database.db is automatically created inside backend/ when the backend starts.

MySQL (Optional)
Import the SQL file:

pgsql
Copy code
db/schema.sql
This creates the required clients and cases tables.

🟪 4️⃣ How to Test the Application
Start backend server

Start frontend server

Open browser → http://localhost:3000

Create a new case

View Case List page

Open Case Detail page

Update status + follow-up notes

Confirm that updates appear immediately

✔ The project is ready to run and easy to set up on any machine.