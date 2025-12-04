from fastapi import FastAPI, HTTPException, Query
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from pydantic import BaseModel
from datetime import date

app = FastAPI(title="PayAssured Case Tracker - Backend")

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: str
    company_name: Optional[str] = None
    city: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    invoice_number: str
    invoice_amount: float
    invoice_date: date
    due_date: date
    status: str = "New"
    last_follow_up_notes: Optional[str] = None

class ClientCreate(BaseModel):
    client_name: str
    company_name: Optional[str] = None
    city: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class CaseCreate(BaseModel):
    client_id: int
    invoice_number: str
    invoice_amount: float
    invoice_date: date
    due_date: date
    status: Optional[str] = "New"
    last_follow_up_notes: Optional[str] = None

class CasePatch(BaseModel):
    status: Optional[str] = None
    last_follow_up_notes: Optional[str] = None

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        clients = session.exec(select(Client)).all()
        if not clients:
            c1 = Client(client_name="ABC Traders", company_name="ABC Pvt Ltd", city="Bengaluru", contact_person="Ravi", phone="9876543210", email="ravi@abc.com")
            c2 = Client(client_name="XYZ Solutions", company_name="XYZ Ltd", city="Mumbai", contact_person="Sita", phone="9123456780", email="sita@xyz.com")
            session.add_all([c1, c2])
            session.commit()
            case1 = Case(client_id=c1.id, invoice_number="INV-001", invoice_amount=50000.0, invoice_date=date(2025,10,1), due_date=date(2025,11,1), status="In Follow-up", last_follow_up_notes="Called client, awaiting response.")
            case2 = Case(client_id=c2.id, invoice_number="INV-101", invoice_amount=75000.0, invoice_date=date(2025,9,15), due_date=date(2025,10,15), status="New", last_follow_up_notes="Assigned to tele-calling team.")
            session.add_all([case1, case2])
            session.commit()

@app.post("/clients", status_code=201)
def create_client(payload: ClientCreate):
    client = Client.from_orm(payload)
    with Session(engine) as session:
        session.add(client)
        session.commit()
        session.refresh(client)
        return client

@app.get("/clients", response_model=List[Client])
def list_clients():
    with Session(engine) as session:
        return session.exec(select(Client)).all()

@app.post("/cases", status_code=201)
def create_case(payload: CaseCreate):
    with Session(engine) as session:
        client = session.get(Client, payload.client_id)
        if not client:
            raise HTTPException(status_code=400, detail="Client not found")
        case = Case.from_orm(payload)
        session.add(case)
        session.commit()
        session.refresh(case)
        return case

@app.get("/cases", response_model=List[Case])
def list_cases(status: Optional[str] = Query(None), sort: Optional[str] = Query(None)):
    with Session(engine) as session:
        q = select(Case)
        if status:
            q = q.where(Case.status == status)
        if sort == "due_date.asc":
            q = q.order_by(Case.due_date.asc())
        if sort == "due_date.desc":
            q = q.order_by(Case.due_date.desc())
        return session.exec(q).all()

@app.get("/cases/{case_id}", response_model=Case)
def get_case(case_id: int):
    with Session(engine) as session:
        case = session.get(Case, case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        return case

@app.patch("/cases/{case_id}")
def patch_case(case_id: int, payload: CasePatch):
    with Session(engine) as session:
        case = session.get(Case, case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        if payload.status is not None:
            case.status = payload.status
        if payload.last_follow_up_notes is not None:
            case.last_follow_up_notes = payload.last_follow_up_notes
        session.add(case)
        session.commit()
        session.refresh(case)
        return case
