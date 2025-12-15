# agent_core.py

import json
import os
import time
import threading
from datetime import datetime
import requests
import ctypes
import statistics

from pynput import keyboard, mouse
import psutil

try:
    import win32gui
    import win32process
except ImportError:
    win32gui = None
    win32process = None

CONFIG_PATH = "config.json"
DEFAULT_BASE_URL = "https://nagster.onrender.com"

# Simple keys jo spam ke liye use hote hain
SIMPLE_KEYS = {
    "Key.space",
    "Key.esc",
    "Key.up",
    "Key.down",
    "Key.left",
    "Key.right",
}


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
# Main Agent class
# ==============================

class NagsterAgent:
    def __init__(self, employee_id: str, config: dict | None = None):
        self.employee_id = employee_id

        base_cfg = {
            "backend_base_url": DEFAULT_BASE_URL,
            "send_interval_seconds": 60,
            "idle_threshold_seconds": 300,
            "idle_logout_seconds": 300,
            "suspicious_key_threshold": 500,
            "logout_action": "disconnect",
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

        # interval suspicious count
        self.suspicious_count = 0
        self.session_suspicious_count = 0

        self.last_activity_ts = time.time()
        self.last_send_ts = 0
        self.last_send_time_str = "Never"
        self.backend_status = "Not checked"
        self.running = False

        # suspicious / fake detection
        self.last_key = None
        self.same_key_streak = 0
        self.suspicious_threshold = self.config.get("suspicious_key_threshold", 500)

        # mouse / window tracking
        now = time.time()
        self.last_mouse_move_ts = now
        self.last_window_change_ts = now
        self.last_active_hwnd = None

        # timing pattern for keys
        self.key_times = []
        self.key_times_window_sec = 60

        # UI will read these
        self.current_app_exe = None
        self.current_app_title = None

        # lock for sharing state
        self.lock = threading.Lock()

    # -------- Input handlers --------

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
                self.session_suspicious_count += 1
                self.same_key_streak = 0

            self.key_times.append(now)
            cut_off = now - self.key_times_window_sec
            self.key_times = [t for t in self.key_times if t >= cut_off]

            self.check_fake_activity(now, key_name)

    def on_mouse_move(self, x, y):
        with self.lock:
            now = time.time()
            self.last_activity_ts = now
            self.last_mouse_move_ts = now

    def on_mouse_click(self, x, y, button, pressed):
        with self.lock:
            now = time.time()
            self.last_activity_ts = now
            self.last_mouse_move_ts = now

    def on_mouse_scroll(self, x, y, dx, dy):
        with self.lock:
            now = time.time()
            self.last_activity_ts = now
            self.last_mouse_move_ts = now

    # -------- Window / activity tracking --------

    def get_active_window(self):
        if not win32gui or not win32process:
            return None, None, None

        try:
            hwnd = win32gui.GetForegroundWindow()
            if not hwnd:
                return None, None, None

            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            exe_name = None
            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["pid"] == pid:
                    exe_name = proc.info["name"]
                    break

            title = win32gui.GetWindowText(hwnd)

            return exe_name, title, hwnd
        except Exception:
            return None, None, None

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

            exe, title, hwnd = self.get_active_window()
            self.current_app_exe = exe
            self.current_app_title = title

            if hwnd is not None and hwnd != self.last_active_hwnd:
                self.last_active_hwnd = hwnd
                self.last_window_change_ts = now

    # -------- Fake activity detection --------

    def check_fake_activity(self, now: float, key_name: str):
        if key_name not in SIMPLE_KEYS:
            return

        if self.same_key_streak < 50:
            return

        no_mouse_for = now - self.last_mouse_move_ts
        no_window_for = now - self.last_window_change_ts

        if no_mouse_for < 15 or no_window_for < 15:
            return

        if len(self.key_times) < 10:
            return

        deltas = [
            self.key_times[i] - self.key_times[i - 1]
            for i in range(1, len(self.key_times))
        ]
        avg = sum(deltas) / len(deltas)
        try:
            stddev = statistics.pstdev(deltas)
        except Exception:
            stddev = 0.0

        if stddev < 0.02 and avg > 0.05:
            print(
                "[Nagster] Fake activity detected: uniform key spam, "
                "no mouse, no window change."
            )
            self.suspicious_count += 1
            self.session_suspicious_count += 1
            self.trigger_logout(reason="fake_activity")

    # -------- Logout / session control --------

    def trigger_logout(self, reason: str):
        print(f"[Nagster] Triggering logout due to: {reason}")
        with self.lock:
            self.backend_status = f"Logging out: {reason}"
            self.running = False

        try:
            self.send_to_backend()
        except Exception as e:
            print("[Nagster] Final send during logout failed:", e)

        action = self.config.get("logout_action", "lock")

        try:
            if action == "disconnect":
                print("[Nagster] Disconnecting remote session (tsdiscon)")
                os.system("tsdiscon")
            elif action == "logoff":
                print("[Nagster] Logging off user (shutdown /l)")
                os.system("shutdown /l")
            else:
                print("[Nagster] Locking workstation")
                ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            print("[Nagster] Session control command failed:", e)

    # -------- Backend communication --------

    def build_payload(self):
        now = datetime.utcnow()

        with self.lock:
            payload = {
                "employee_id": self.employee_id,
                "timestamp": now.isoformat(),
                "active_seconds": self.active_seconds,
                "idle_seconds": self.idle_seconds,
                "suspicious": self.suspicious_count > 0,
                "active_app_exe": self.current_app_exe,
                "active_app_title": self.current_app_title,
            }

            self.active_seconds = 0
            self.idle_seconds = 0
            self.suspicious_count = 0
            self.same_key_streak = 0

            self.last_send_ts = time.time()
            self.last_send_time_str = now.strftime("%H:%M:%S")

        return payload

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

    # -------- Worker loop --------

    def worker_loop(self):
        self.running = True
        interval = self.config["send_interval_seconds"]
        idle_logout = self.config.get("idle_logout_seconds", 300)

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

                with self.lock:
                    idle_gap = now - self.last_activity_ts
                    session_flags = self.session_suspicious_count

                if idle_gap >= idle_logout:
                    print(
                        "[Nagster] Auto logout due to idle for",
                        int(idle_gap),
                        "seconds",
                    )
                    self.trigger_logout(reason="idle_timeout")
                    break

                if session_flags > 3:
                    print("[Nagster] Auto logout: suspicious flags >", 3)
                    self.trigger_logout(reason="too_many_suspicious_flags")
                    break

                if now - self.last_send_ts >= interval:
                    self.send_to_backend()

                time.sleep(1)
        finally:
            keyboard_listener.stop()
            mouse_listener.stop()
            print("[Nagster] Worker stopped")

    def stop(self):
        self.running = False
