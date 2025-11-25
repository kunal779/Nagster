import json
import time
import threading
from datetime import datetime
import os
import requests

from pynput import keyboard, mouse
import psutil

try:
    import win32gui
    import win32process
except ImportError:
    win32gui = None
    win32process = None

import tkinter as tk
from tkinter import messagebox

CONFIG_PATH = "config.json"
DEFAULT_BASE_URL = "http://127.0.0.1:8000"


# ==============================
# Config helpers
# ==============================

def load_config_file():
    """Load config.json if present, and normalise backend_base_url."""
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception as e:
            print("[Nagster] Failed to load config:", e)
            cfg = {}

    # normalise backend_base_url
    if "backend_base_url" not in cfg:
        if "backend_url" in cfg:
            url = cfg["backend_url"]
            if url.endswith("/activity"):
                url = url[:-9]
            cfg["backend_base_url"] = url
        else:
            cfg["backend_base_url"] = DEFAULT_BASE_URL

    return cfg


def save_config_file(cfg: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        print("[Nagster] Config saved:", cfg)
    except Exception as e:
        print("[Nagster] Failed to save config:", e)


# ==============================
# Backend verify helper
# ==============================

def verify_employee_with_backend(emp_id: str, backend_base: str) -> bool:
    url = backend_base.rstrip("/") + f"/employees/{emp_id}"
    print("[Nagster] Verifying employee on:", url)

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            print("[Nagster] Employee verified:", resp.json())
            return True
        else:
            print("[Nagster] Employee invalid:", resp.status_code, resp.text)
            return False
    except Exception as e:
        print("[Nagster] Error verifying employee:", e)
        return False


# ==============================
# Popup: Employee ID + Remember Me + Check
# ==============================

def prompt_employee_id_popup(config: dict):
    """
    Show a small Tkinter popup asking for Employee ID + Remember Me.
    Returns (employee_id, remember_me_bool).
    Exits program if user closes without success.
    """
    backend_base = config.get("backend_base_url", DEFAULT_BASE_URL)
    result = {"employee_id": None, "remember": False}

    root = tk.Tk()
    root.title("Nagster Login")
    root.geometry("320x180")
    root.resizable(False, False)

    # Center the window on screen (optional)
    try:
        root.update_idletasks()
        w = 320
        h = 180
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        root.geometry(f"{w}x{h}+{x}+{y}")
    except Exception:
        pass

    tk.Label(root, text="Enter your Employee ID", font=("Segoe UI", 10)).pack(pady=(15, 5))

    entry = tk.Entry(root, font=("Segoe UI", 10))
    entry.pack(pady=(0, 8))
    entry.focus_set()

    remember_var = tk.IntVar(value=1 if config.get("remember_me") else 0)
    chk = tk.Checkbutton(root, text="Remember me", variable=remember_var, font=("Segoe UI", 9))
    chk.pack()

    def on_check_click():
        emp_id = entry.get().strip()
        if not emp_id:
            messagebox.showerror("Nagster", "Employee ID cannot be empty.")
            return

        if verify_employee_with_backend(emp_id, backend_base):
            remember = bool(remember_var.get())
            result["employee_id"] = emp_id
            result["remember"] = remember

            if remember:
                config["employee_id"] = emp_id
                config["remember_me"] = True
            else:
                config.pop("employee_id", None)
                config["remember_me"] = False

            save_config_file(config)
            root.destroy()
        else:
            messagebox.showerror("Nagster", "Employee not found in company database.")

    btn = tk.Button(root, text="Check", command=on_check_click, width=10)
    btn.pack(pady=(10, 8))

    def on_close():
        # user closed window → exit app
        root.destroy()
        raise SystemExit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    emp_id = result["employee_id"]
    remember = result["remember"]
    if not emp_id:
        # didn't successfully verify
        raise SystemExit(0)

    return emp_id, remember


# ==============================
# Main Agent class
# ==============================

class NagsterAgent:
    def __init__(self, employee_id: str, config: dict | None = None):
        self.employee_id = employee_id

        base_cfg = {
            "backend_base_url": DEFAULT_BASE_URL,
            "send_interval_seconds": 60,
            "idle_threshold_seconds": 300,
            "suspicious_key_threshold": 500,
        }
        if config:
            base_cfg.update(config)
        self.config = base_cfg

        # interval counters (reset after every send)
        self.active_seconds = 0
        self.idle_seconds = 0

        # total counters (session)
        self.total_active_seconds = 0
        self.total_idle_seconds = 0

        self.suspicious_count = 0
        self.last_activity_ts = time.time()
        self.last_send_ts = 0
        self.last_send_time_str = "Never"
        self.backend_status = "Not checked"
        self.running = False

        # suspicious detection
        self.last_key = None
        self.same_key_streak = 0
        self.suspicious_threshold = self.config.get("suspicious_key_threshold", 500)

        # UI will read these
        self.current_app_exe = None
        self.current_app_title = None

        # lock for sharing state
        self.lock = threading.Lock()

    # -------------------------
    # Input event handlers
    # -------------------------

    def on_key(self, key):
        now = time.time()
        with self.lock:
            self.last_activity_ts = now

            try:
                key_name = str(key)
            except Exception:
                key_name = "unknown"

            if key_name == self.last_key:
                self.same_key_streak += 1
            else:
                self.last_key = key_name
                self.same_key_streak = 1

            if self.same_key_streak > self.suspicious_threshold:
                self.suspicious_count += 1
                self.same_key_streak = 0

    def on_mouse_move(self, x, y):
        with self.lock:
            self.last_activity_ts = time.time()

    def on_mouse_click(self, x, y, button, pressed):
        with self.lock:
            self.last_activity_ts = time.time()

    def on_mouse_scroll(self, x, y, dx, dy):
        with self.lock:
            self.last_activity_ts = time.time()

    # -------------------------
    # Active window detection
    # -------------------------

    def get_active_window(self):
        if not win32gui or not win32process:
            return None, None

        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None, None

            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            exe_name = None
            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["pid"] == pid:
                    exe_name = proc.info["name"]
                    break

            title = win32gui.GetWindowText(hwnd)

            return exe_name, title
        except Exception:
            return None, None

    # -------------------------
    # Timer tick
    # -------------------------

    def tick_second(self):
        now = time.time()
        with self.lock:
            idle_threshold = self.config.get("idle_threshold_seconds", 300)
            idle_gap = now - self.last_activity_ts

            if idle_gap <= idle_threshold:
                self.active_seconds += 1
                self.total_active_seconds += 1
            else:
                self.idle_seconds += 1
                self.total_idle_seconds += 1

            exe, title = self.get_active_window()
            self.current_app_exe = exe
            self.current_app_title = title

    # -------------------------
    # Payload builder
    # -------------------------

    def build_payload(self):
        now = datetime.utcnow()

        with self.lock:
            payload = {
                "employee_id": self.employee_id,
                "timestamp": now.isoformat(),     # No "Z"
                "active_seconds": self.active_seconds,
                "idle_seconds": self.idle_seconds,
                "suspicious": self.suspicious_count > 0,
                "active_app_exe": self.current_app_exe,
                "active_app_title": self.current_app_title,
            }

            # reset only interval counters
            self.active_seconds = 0
            self.idle_seconds = 0
            self.suspicious_count = 0
            self.same_key_streak = 0

            self.last_send_ts = time.time()
            self.last_send_time_str = now.strftime("%H:%M:%S")

        return payload

    # -------------------------
    # Send activity to backend
    # -------------------------

    def send_to_backend(self):
        payload = self.build_payload()
        backend_url = self.config["backend_base_url"].rstrip("/") + "/activity"

        try:
            resp = requests.post(
                backend_url,
                json=payload,
                timeout=5,
            )

            if resp.status_code == 200:
                with self.lock:
                    self.backend_status = "Connected"
                print("[Nagster] Sent activity:", payload)

            elif resp.status_code == 404:
                with self.lock:
                    self.backend_status = "Employee not registered"
                print("[Nagster] Backend says employee is invalid. Stopping agent.")
                self.stop()
                return

            else:
                with self.lock:
                    self.backend_status = f"Error: {resp.status_code}"
                print("[Nagster] Backend error:", resp.status_code, resp.text)

        except Exception as e:
            with self.lock:
                self.backend_status = "Failed: cannot reach backend"
            print("[Nagster] Failed to send:", repr(e))

    # -------------------------
    # Worker loop
    # -------------------------

    def worker_loop(self):
        self.running = True
        interval = self.config["send_interval_seconds"]

        print("[Nagster] Worker started")

        keyboard_listener = keyboard.Listener(on_press=self.on_key)
        mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll,
        )
        keyboard_listener.start()
        mouse_listener.start()

        try:
            while self.running:
                self.tick_second()
                now = time.time()
                if now - self.last_send_ts >= interval:
                    self.send_to_backend()
                time.sleep(1)
        finally:
            keyboard_listener.stop()
            mouse_listener.stop()
            print("[Nagster] Worker stopped")

    def stop(self):
        self.running = False


# =============================================================
# UI
# =============================================================

class NagsterUI:
    def __init__(self, agent: NagsterAgent):
        self.agent = agent

        self.root = tk.Tk()
        self.root.title("Nagster Agent")
        self.root.geometry("380x260")
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close_attempt)

        self.status_label = tk.Label(self.root, text="Agent Status: STARTING", font=("Segoe UI", 10, "bold"))
        self.status_label.pack(pady=(10, 4))

        self.backend_label = tk.Label(self.root, text="Backend: Unknown", font=("Segoe UI", 9))
        self.backend_label.pack(pady=2)

        self.last_send_label = tk.Label(self.root, text="Last log sent: Never", font=("Segoe UI", 9))
        self.last_send_label.pack(pady=2)

        self.activity_label = tk.Label(
            self.root,
            text="Active (interval): 0s  |  Idle (interval): 0s",
            font=("Segoe UI", 9)
        )
        self.activity_label.pack(pady=4)

        self.total_label = tk.Label(
            self.root,
            text="Total Active: 0s  |  Total Idle: 0s",
            font=("Segoe UI", 9)
        )
        self.total_label.pack(pady=2)

        self.app_label = tk.Label(self.root, text="Active app: -", font=("Segoe UI", 8), fg="#666")
        self.app_label.pack(pady=3)

        self.info_label = tk.Label(
            self.root,
            text=f"Employee ID: {self.agent.employee_id}",
            font=("Segoe UI", 8),
            fg="#444",
        )
        self.info_label.pack(pady=5)

        self.stop_button = tk.Button(
            self.root,
            text="Stop & Exit",
            command=self.on_stop_click,
            bg="#d40000",
            fg="white",
            padx=10,
            pady=5
        )
        self.stop_button.pack(pady=4)

        self.worker_thread = threading.Thread(target=self.agent.worker_loop, daemon=True)
        self.worker_thread.start()

        self.update_ui()

    def on_close_attempt(self):
        # [X] se close disable, sirf Stop & Exit se band hoga
        pass

    def on_stop_click(self):
        # Stop karne se pehle ek final log bhej do
        try:
            print("[Nagster] Sending final activity log before exit...")
            self.agent.send_to_backend()
        except Exception as e:
            print("[Nagster] Final send failed:", repr(e))

        self.agent.stop()
        self.root.after(500, self.root.destroy)

    def format_hms(self, total_seconds: int) -> str:
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        if h > 0:
            return f"{h}h {m}m {s}s"
        elif m > 0:
            return f"{m}m {s}s"
        else:
            return f"{s}s"

    def update_ui(self):
        if self.agent.running:
            self.status_label.config(text="Agent Status: ACTIVE", fg="#0A8A25")
        else:
            self.status_label.config(text="Agent Status: STOPPED", fg="#C41E1E")

        with self.agent.lock:
            backend = self.agent.backend_status
            last_send = self.agent.last_send_time_str
            active = self.agent.active_seconds
            idle = self.agent.idle_seconds
            suspicious = self.agent.suspicious_count
            exe = self.agent.current_app_exe
            title = self.agent.current_app_title
            total_active = self.agent.total_active_seconds
            total_idle = self.agent.total_idle_seconds

        self.backend_label.config(text=f"Backend: {backend}")
        self.last_send_label.config(text=f"Last log sent: {last_send}")

        self.activity_label.config(
            text=f"Active (interval): {active}s  |  Idle (interval): {idle}s  |  Suspicious: {suspicious}"
        )

        self.total_label.config(
            text=f"Total Active: {self.format_hms(total_active)}  |  Total Idle: {self.format_hms(total_idle)}"
        )

        if exe or title:
            self.app_label.config(text=f"Active app: {exe or '-'} | {title or '-'}")
        else:
            self.app_label.config(text="Active app: -")

        self.root.after(1000, self.update_ui)

    def run(self):
        self.root.mainloop()


# =============================================================
# MAIN
# =============================================================

def main():
    # 1) Load config from file
    cfg = load_config_file()
    backend_base = cfg.get("backend_base_url", DEFAULT_BASE_URL)

    # 2) Check if Remember Me + saved ID exists and is valid
    employee_id = None
    if cfg.get("remember_me") and cfg.get("employee_id"):
        emp = cfg["employee_id"]
        print("[Nagster] Using saved Employee ID:", emp)
        if verify_employee_with_backend(emp, backend_base):
            employee_id = emp
        else:
            print("[Nagster] Saved Employee ID invalid, clearing it.")
            cfg["remember_me"] = False
            cfg.pop("employee_id", None)
            save_config_file(cfg)

    # 3) If not remembered or invalid, show popup
    if not employee_id:
        employee_id, _ = prompt_employee_id_popup(cfg)
        backend_base = cfg.get("backend_base_url", backend_base)

    # 4) Start agent + UI
    agent = NagsterAgent(employee_id=employee_id, config=cfg)
    ui = NagsterUI(agent)
    print("[Nagster] UI starting...")
    ui.run()
    print("[Nagster] UI closed.")


if __name__ == "__main__":
    main()
