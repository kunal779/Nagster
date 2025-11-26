from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
import sqlite3
import os
import hashlib
import jwt
from typing import Optional, List

DB_PATH = "nagster.db"

# JWT config
SECRET_KEY = "supersecret_nagster_key_change_later"
ALGORITHM = "HS256"

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========= MODELS =========

class ActivityLog(BaseModel):
    employee_id: str
    timestamp: datetime
    active_seconds: int
    idle_seconds: int
    suspicious: bool
    active_app_exe: str | None = None
    active_app_title: str | None = None


class UserSignup(BaseModel):
    username: str
    password: str
    role: str  # "admin" or "manager"


class UserLogin(BaseModel):
    username: str
    password: str


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    designation: str
    domain: str
    department: str
    location: str
    work_mode: str  # WFH / Office / Hybrid
    employee_type: Optional[str] = None
    salary_band: Optional[str] = None
    joining_date: str  # "YYYY-MM-DD"
    manager_name: str
    manager_email: Optional[str] = None


# ========= DB HELPERS =========

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_access_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "iat": int(datetime.utcnow().timestamp()),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


# 🔴 NEW: helper to check if employee exists
def employee_exists(emp_id: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM employees WHERE employee_id = ?", (emp_id,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # activity logs table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            active_seconds INTEGER NOT NULL,
            idle_seconds INTEGER NOT NULL,
            suspicious INTEGER NOT NULL,
            active_app_exe TEXT,
            active_app_title TEXT
        )
        """
    )

    # employees table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            designation TEXT,
            domain TEXT,
            department TEXT,
            location TEXT,
            work_mode TEXT,
            employee_type TEXT,
            salary_band TEXT,
            joining_date TEXT,
            manager_name TEXT,
            manager_email TEXT,
            status TEXT
        )
        """
    )

    # users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


@app.on_event("startup")
def on_startup():
    init_db()
    print("✅ SQLite DB ready at", os.path.abspath(DB_PATH))


# ========== AUTH ROUTES ==========

@app.post("/auth/signup")
def signup(user: UserSignup):
    if user.role not in ("admin", "manager"):
        raise HTTPException(status_code=400, detail="role must be 'admin' or 'manager'")

    existing = get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        (user.username, hash_password(user.password), user.role),
    )
    conn.commit()
    conn.close()

    token = create_access_token(user.username, user.role)
    return {"access_token": token, "role": user.role}


@app.post("/auth/login")
def login(user: UserLogin):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(db_user["username"], db_user["role"])
    return {"access_token": token, "role": db_user["role"]}


@app.get("/auth/me")
def me(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    role = payload.get("role")
    return {"username": username, "role": role}


# ========== BASE ROUTES ==========

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Nagster backend with employees & activity logs"}


@app.post("/activity")
def receive_activity(log: ActivityLog):
    """
    Agent se single-interval summary aati hai.
    Yahan:
      1) activity_logs me insert
      2) us employee ka status = 'Active' kar dete hain
    """

    # 🔴 NEW: ensure this employee is registered in DB
    if not employee_exists(log.employee_id):
        raise HTTPException(
            status_code=404,
            detail=f"Employee {log.employee_id} not registered in company DB",
        )

    log_date = log.timestamp.date().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    # activity log store
    cur.execute(
        """
        INSERT INTO activity_logs (
            employee_id, date, timestamp,
            active_seconds, idle_seconds, suspicious,
            active_app_exe, active_app_title
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            log.employee_id,
            log_date,
            log.timestamp.isoformat(),
            log.active_seconds,
            log.idle_seconds,
            1 if log.suspicious else 0,
            log.active_app_exe,
            log.active_app_title,
        ),
    )

    # jis employee ne log bheja use Active mark karo
    cur.execute(
        "UPDATE employees SET status = 'Active' WHERE employee_id = ?",
        (log.employee_id,),
    )

    conn.commit()
    conn.close()

    print("✅ Stored activity log in DB:", log.dict())
    return {"message": "log stored"}


# ========== EMPLOYEE CRUD ==========

@app.post("/employees/add")
def add_employee(emp: EmployeeCreate):
    """Add a new employee from Add Employee page."""
    conn = get_connection()
    cur = conn.cursor()

    # check if exists
    cur.execute(
        "SELECT employee_id FROM employees WHERE employee_id = ?",
        (emp.employee_id,),
    )
    existing = cur.fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    cur.execute(
        """
        INSERT INTO employees (
            employee_id, name, email, phone,
            designation, domain, department,
            location, work_mode, employee_type,
            salary_band, joining_date,
            manager_name, manager_email, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            emp.employee_id,
            emp.name,
            emp.email,
            emp.phone,
            emp.designation,
            emp.domain,
            emp.department,
            emp.location,
            emp.work_mode,
            emp.employee_type,
            emp.salary_band,
            emp.joining_date,
            emp.manager_name,
            emp.manager_email,
            "Inactive",  # default
        ),
    )
    conn.commit()
    conn.close()
    return {"message": "Employee added"}


@app.delete("/employees/remove/{employee_id}")
def remove_employee(employee_id: str):
    """Remove employee + optional logs (for Remove Employee page)."""
    conn = get_connection()
    cur = conn.cursor()

    # ensure employee exists
    cur.execute(
        "SELECT employee_id FROM employees WHERE employee_id = ?",
        (employee_id,),
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found")

    # delete logs first (optional but clean)
    cur.execute(
        "DELETE FROM activity_logs WHERE employee_id = ?",
        (employee_id,),
    )
    # delete employee
    cur.execute(
        "DELETE FROM employees WHERE employee_id = ?",
        (employee_id,),
    )
    conn.commit()
    conn.close()
    return {"message": "Employee removed"}


@app.get("/employees")
def list_employees(status: str | None = Query(None)):
    """
    All employees basic info.
    Optional ?status=Active or ?status=Inactive
    """
    conn = get_connection()
    cur = conn.cursor()

    if status:
        cur.execute(
            """
            SELECT employee_id, name, designation, domain, department,
                   location, work_mode, status
            FROM employees
            WHERE status = ?
            ORDER BY employee_id
            """,
            (status,),
        )
    else:
        cur.execute(
            """
            SELECT employee_id, name, designation, domain, department,
                   location, work_mode, status
            FROM employees
            ORDER BY employee_id
            """
        )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# 🔴 NEW: single employee fetch for agent verification
@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT employee_id, name, designation, domain, department,
               location, work_mode, status
        FROM employees
        WHERE employee_id = ?
        """,
        (employee_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")

    return dict(row)


# Aliased endpoint: POST /employees
@app.post("/employees")
def create_employee(emp: EmployeeCreate):
    # Reuse existing logic
    return add_employee(emp)


# Aliased endpoint: DELETE /employees/{employee_id}
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    # Reuse existing logic
    return remove_employee(employee_id)


# ========== OVERVIEW / SUMMARY ==========

@app.get("/overview")
def overview(date_str: str | None = Query(None)):
    """
    Daily overview for all employees (for dashboard left panel).

    Status logic:
      - Agar aaj ke din koi activity hi nahi -> Inactive
      - Agar last activity N seconds se purani hai -> Inactive
      - Warna Active
    """
    if date_str:
        target_date = date_str
    else:
        target_date = date.today().isoformat()

    INACTIVE_AFTER_SECONDS = 60  # 60s after last log -> Inactive

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
          e.employee_id,
          e.name,
          e.designation,
          e.domain,
          e.department,
          e.location,
          e.work_mode,
          e.status AS db_status,
          MIN(a.timestamp) AS login_time,
          MAX(a.timestamp) AS logout_time,
          COALESCE(SUM(a.active_seconds), 0) AS total_active,
          COALESCE(SUM(a.idle_seconds), 0) AS total_idle,
          COALESCE(SUM(a.suspicious), 0) AS total_suspicious
        FROM employees e
        LEFT JOIN activity_logs a
          ON e.employee_id = a.employee_id
         AND a.date = ?
        GROUP BY e.employee_id
        ORDER BY e.employee_id
        """,
        (target_date,),
    )

    rows = cur.fetchall()
    conn.close()

    now = datetime.utcnow()
    result = []

    def to_minutes(sec: int):
        return sec // 60

    for row in rows:
        total_active = row["total_active"]
        total_idle = row["total_idle"]
        login_time = row["login_time"]
        logout_time = row["logout_time"]
        db_status = row["db_status"]

        # derive status
        if logout_time is None:
            current_status = "Inactive"
        else:
            try:
                ts = logout_time
                if isinstance(ts, str) and ts.endswith("Z"):
                    ts = ts[:-1]
                last_dt = datetime.fromisoformat(ts)
                diff = (now - last_dt).total_seconds()
                if diff > INACTIVE_AFTER_SECONDS:
                    current_status = "Inactive"
                else:
                    current_status = "Active"
            except Exception:
                current_status = db_status or "Inactive"

        result.append(
            {
                "employee_id": row["employee_id"],
                "name": row["name"],
                "designation": row["designation"],
                "domain": row["domain"],
                "department": row["department"],
                "location": row["location"],
                "work_mode": row["work_mode"],
                "status": current_status,
                "login_time": login_time,
                "logout_time": logout_time,
                "active_minutes": to_minutes(total_active),
                "idle_minutes": to_minutes(total_idle),
                "suspicious_flag_count": row["total_suspicious"],
            }
        )

    return result


@app.get("/summary/{employee_id}")
def get_summary(employee_id: str, date_str: str | None = Query(None)):
    """
    Detailed summary for single employee for a given day.
    """
    if date_str:
        target_date = date_str
    else:
        target_date = date.today().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            COALESCE(SUM(active_seconds), 0) AS total_active,
            COALESCE(SUM(idle_seconds), 0) AS total_idle,
            COALESCE(SUM(suspicious), 0) AS total_suspicious,
            MIN(timestamp) AS login_time,
            MAX(timestamp) AS logout_time
        FROM activity_logs
        WHERE employee_id = ? AND date = ?
        """,
        (employee_id, target_date),
    )
    logs_row = cur.fetchone()

    cur.execute(
        """
        SELECT *
        FROM employees
        WHERE employee_id = ?
        """,
        (employee_id,),
    )
    emp_row = cur.fetchone()
    conn.close()

    if not emp_row:
        raise HTTPException(status_code=404, detail="Employee not found")

    total_active = logs_row["total_active"] if logs_row else 0
    total_idle = logs_row["total_idle"] if logs_row else 0
    total_suspicious = logs_row["total_suspicious"] if logs_row else 0

    def fmt_sec(sec: int):
        hours = sec // 3600
        mins = (sec % 3600) // 60
        return {"hours": hours, "minutes": mins, "seconds": sec}

    emp = dict(emp_row)

    return {
        "employee_id": emp["employee_id"],
        "date": target_date,
        "name": emp["name"],
        "email": emp["email"],
        "phone": emp["phone"],
        "designation": emp["designation"],
        "domain": emp["domain"],
        "department": emp["department"],
        "location": emp["location"],
        "work_mode": emp["work_mode"],
        "employee_type": emp["employee_type"],
        "salary_band": emp["salary_band"],
        "joining_date": emp["joining_date"],
        "manager_name": emp["manager_name"],
        "manager_email": emp["manager_email"],
        "status": emp["status"],
        "login_time": logs_row["login_time"] if logs_row else None,
        "logout_time": logs_row["logout_time"] if logs_row else None,
        "active": fmt_sec(total_active),
        "idle": fmt_sec(total_idle),
        "suspicious_flag_count": total_suspicious,
    }


# ========== ACTIVITY LOG LIST ==========

@app.get("/activity/{employee_id}")
def get_activity_logs(employee_id: str, date_str: str | None = Query(None)):
    """
    Raw activity logs list for an employee for given date.
    Frontend ActivityView iss format me use karega:
      [
        {
          "timestamp": "...",
          "type": "active/idle/suspicious",
          "title": "...",
          "description": "...",
          "duration": "60s",
          "details": "...",
        },
        ...
      ]
    """
    if date_str:
        target_date = date_str
    else:
        target_date = date.today().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    # ensure employee exists
    cur.execute(
        "SELECT employee_id, name FROM employees WHERE employee_id = ?",
        (employee_id,),
    )
    emp = cur.fetchone()
    if not emp:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found")

    cur.execute(
        """
        SELECT *
        FROM activity_logs
        WHERE employee_id = ? AND date = ?
        ORDER BY timestamp ASC
        """,
        (employee_id, target_date),
    )
    rows = cur.fetchall()
    conn.close()

    logs: List[dict] = []

    for row in rows:
        active = row["active_seconds"]
        idle = row["idle_seconds"]
        suspicious = row["suspicious"]
        exe = row["active_app_exe"]
        title = row["active_app_title"]
        ts = row["timestamp"]

        total_sec = (active or 0) + (idle or 0)

        # type decide
        if suspicious:
            activity_type = "suspicious"
        elif active >= idle:
            activity_type = "active"
        else:
            activity_type = "idle"

        if title:
            item_title = title
        elif exe:
            item_title = exe
        else:
            item_title = "Activity interval"

        description_parts = [
            f"Active: {active}s",
            f"Idle: {idle}s",
        ]
        if exe or title:
            description_parts.append(f"App: {exe or '-'} | {title or '-'}")

        log_item = {
            "timestamp": ts,
            "type": activity_type,
            "title": item_title,
            "description": " | ".join(description_parts),
            "duration": f"{total_sec}s" if total_sec else None,
            "details": f"log_id={row['id']}",
        }
        logs.append(log_item)

    return logs

