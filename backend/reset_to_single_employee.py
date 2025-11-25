import sqlite3

DB_PATH = "nagster.db"

def reset_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # sab employees hatao
    cur.execute("DELETE FROM employees")

    # sab activity logs bhi hatao (fresh start)
    cur.execute("DELETE FROM activity_logs")

    # sirf tumhari entry add karo
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
            "EMP001",
            "Kunal Ghugare",
            "kunalghugare28@gmail.com",
            "+91 7841974987",
            "Software Engineer",
            "Engineering",
            "Development",
            "Nagpur",
            "WFH",
            "Full-time",
            "L1",
            "2025-01-01",
            "Manager A",
            "manager@example.com",
            "Inactive",   # 🔴 start me inactive
        ),
    )

    conn.commit()
    conn.close()
    print("✅ DB reset: only EMP001 (Kunal, Inactive) is present now.")

if __name__ == "__main__":
    reset_db()
