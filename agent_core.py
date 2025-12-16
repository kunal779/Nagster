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
        print("[Nagster] Config saved")
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
            print("[Nagster] Employee verified")
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
            "send_interval_seconds": 8,  # Har 8 second baad update
            "idle_threshold_seconds": 300,
            "idle_logout_seconds": 300,
            "suspicious_key_threshold": 500,
            "logout_action": "lock",
            "detailed_logging": True,  # Enable detailed activity logging
        }
        if config:
            base_cfg.update(config)
        self.config = base_cfg

        # Real-time activity tracking
        self.current_activity = "idle"  # idle, typing, mouse, scrolling, etc.
        self.activity_start_time = time.time()
        self.activity_history = []  # Store activities for the last 8 seconds
        
        # Session counters
        self.session_activities = []  # All activities in current session
        self.total_keypresses = 0
        self.total_mouse_events = 0
        self.total_window_changes = 0
        
        # 8-second interval counters
        self.interval_keypresses = 0
        self.interval_mouse_clicks = 0
        self.interval_mouse_moves = 0
        self.interval_scrolls = 0
        self.interval_window_changes = 0
        
        # Active/idle tracking
        self.active_seconds = 0
        self.idle_seconds = 0
        self.total_active_seconds = 0
        self.total_idle_seconds = 0
        
        # Suspicious detection
        self.suspicious_count = 0
        self.session_suspicious_count = 0
        self.suspicious_activities = []  # Suspicious activities in current interval

        self.last_activity_ts = time.time()
        self.last_send_ts = 0
        self.last_send_time_str = "Never"
        self.backend_status = "Not checked"
        self.running = False

        # Keyboard tracking
        self.last_key = None
        self.same_key_streak = 0
        self.suspicious_threshold = self.config.get("suspicious_key_threshold", 500)
        self.key_times = []
        self.key_times_window_sec = 60
        
        # Mouse tracking
        self.last_mouse_move_ts = time.time()
        self.last_mouse_click_ts = time.time()
        
        # Window tracking
        self.last_window_change_ts = time.time()
        self.last_active_hwnd = None
        self.current_app_exe = None
        self.current_app_title = None
        self.current_app_start_time = time.time()
        self.app_usage_history = []  # Apps used in current interval
        
        # Activity buffer for real-time updates
        self.realtime_buffer = []  # Store activities as they happen
        
        # Lock for thread safety
        self.lock = threading.Lock()

    # -------- Input handlers (Real-time tracking) --------

    def on_key(self, key):
        now = time.time()
        with self.lock:
            self.last_activity_ts = now
            self.total_keypresses += 1
            self.interval_keypresses += 1
            
            # Track what key was pressed
            try:
                key_name = str(key)
                # Simplify key names
                if "'" in key_name:
                    key_name = key_name.replace("'", "")  # 'a' -> a
                elif "Key." in key_name:
                    key_name = key_name.replace("Key.", "")  # Key.space -> space
            except Exception:
                key_name = "unknown"
            
            # Detect activity type
            activity_type = "typing"
            if key_name in ["space", "enter", "tab"]:
                activity_type = "navigating"
            elif key_name in ["ctrl", "alt", "shift", "cmd", "win"]:
                activity_type = "shortcut"
            
            # Log this keypress in real-time buffer
            activity = {
                "timestamp": datetime.fromtimestamp(now).isoformat(),
                "type": activity_type,
                "subtype": "keypress",
                "details": {
                    "key": key_name,
                    "app_exe": self.current_app_exe,
                    "app_title": self.current_app_title
                },
                "activity": f"Pressed key: {key_name}"
            }
            self._add_to_realtime_buffer(activity)
            self._update_activity_history("keypress", key_name)
            
            # Suspicious detection
            if key_name == self.last_key:
                self.same_key_streak += 1
            else:
                self.last_key = key_name
                self.same_key_streak = 1

            if self.same_key_streak > self.suspicious_threshold:
                self.suspicious_count += 1
                self.session_suspicious_count += 1
                self.same_key_streak = 0
                # Log suspicious activity
                suspicious_activity = {
                    "timestamp": datetime.fromtimestamp(now).isoformat(),
                    "type": "suspicious",
                    "reason": f"Repeated key '{key_name}' {self.same_key_streak} times",
                    "key": key_name
                }
                self.suspicious_activities.append(suspicious_activity)

            self.key_times.append(now)
            cut_off = now - self.key_times_window_sec
            self.key_times = [t for t in self.key_times if t >= cut_off]

            self.check_fake_activity(now, key_name)

    def on_mouse_move(self, x, y):
        now = time.time()
        with self.lock:
            self.last_activity_ts = now
            self.last_mouse_move_ts = now
            self.total_mouse_events += 1
            self.interval_mouse_moves += 1
            
            # Only log significant mouse movements (not every tiny movement)
            if self.interval_mouse_moves % 10 == 0:  # Log every 10th movement
                activity = {
                    "timestamp": datetime.fromtimestamp(now).isoformat(),
                    "type": "mouse",
                    "subtype": "move",
                    "details": {
                        "x": x,
                        "y": y,
                        "app_exe": self.current_app_exe,
                        "app_title": self.current_app_title
                    },
                    "activity": f"Mouse moved to ({x}, {y})"
                }
                self._add_to_realtime_buffer(activity)
                self._update_activity_history("mouse_move", f"position: ({x}, {y})")

    def on_mouse_click(self, x, y, button, pressed):
        now = time.time()
        with self.lock:
            self.last_activity_ts = now
            self.last_mouse_move_ts = now
            self.last_mouse_click_ts = now
            self.total_mouse_events += 1
            self.interval_mouse_clicks += 1
            
            button_name = str(button).replace("Button.", "")
            action = "pressed" if pressed else "released"
            
            activity = {
                "timestamp": datetime.fromtimestamp(now).isoformat(),
                "type": "mouse",
                "subtype": "click",
                "details": {
                    "button": button_name,
                    "action": action,
                    "x": x,
                    "y": y,
                    "app_exe": self.current_app_exe,
                    "app_title": self.current_app_title
                },
                "activity": f"Mouse {button_name} {action} at ({x}, {y})"
            }
            self._add_to_realtime_buffer(activity)
            self._update_activity_history("mouse_click", f"{button_name} {action}")

    def on_mouse_scroll(self, x, y, dx, dy):
        now = time.time()
        with self.lock:
            self.last_activity_ts = now
            self.last_mouse_move_ts = now
            self.total_mouse_events += 1
            self.interval_scrolls += 1
            
            direction = "down" if dy < 0 else "up"
            amount = abs(dy)
            
            activity = {
                "timestamp": datetime.fromtimestamp(now).isoformat(),
                "type": "mouse",
                "subtype": "scroll",
                "details": {
                    "direction": direction,
                    "amount": amount,
                    "x": x,
                    "y": y,
                    "app_exe": self.current_app_exe,
                    "app_title": self.current_app_title
                },
                "activity": f"Scrolled {direction} ({amount} units)"
            }
            self._add_to_realtime_buffer(activity)
            self._update_activity_history("scroll", f"{direction} {amount} units")

    def _add_to_realtime_buffer(self, activity):
        """Add activity to real-time buffer"""
        self.realtime_buffer.append(activity)
        # Keep buffer size reasonable
        if len(self.realtime_buffer) > 50:
            self.realtime_buffer = self.realtime_buffer[-50:]
    
    def _update_activity_history(self, activity_type, details):
        """Update activity history for summary"""
        self.activity_history.append({
            "type": activity_type,
            "details": details,
            "timestamp": time.time(),
            "app": self.current_app_exe
        })
        # Keep last 100 activities
        if len(self.activity_history) > 100:
            self.activity_history = self.activity_history[-100:]

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
            # Check idle/active
            idle_threshold = self.config.get("idle_threshold_seconds", 300)
            idle_gap = now - self.last_activity_ts
            
            if idle_gap <= idle_threshold:
                self.active_seconds += 1
                self.total_active_seconds += 1
            else:
                self.idle_seconds += 1
                self.total_idle_seconds += 1
            
            # Update window info
            exe, title, hwnd = self.get_active_window()
            
            # Check if window changed
            if hwnd is not None and hwnd != self.last_active_hwnd:
                self.last_active_hwnd = hwnd
                self.last_window_change_ts = now
                self.total_window_changes += 1
                self.interval_window_changes += 1
                
                # Log window change
                if exe != self.current_app_exe or title != self.current_app_title:
                    if self.current_app_exe is not None:
                        # Log end of previous app usage
                        prev_duration = now - self.current_app_start_time
                        if prev_duration >= 1:  # Only log if used for at least 1 second
                            self.app_usage_history.append({
                                "app_exe": self.current_app_exe,
                                "app_title": self.current_app_title,
                                "duration": prev_duration,
                                "end_time": datetime.fromtimestamp(now).isoformat()
                            })
                    
                    # Start tracking new app
                    self.current_app_exe = exe
                    self.current_app_title = title
                    self.current_app_start_time = now
                    
                    # Log window switch activity
                    activity = {
                        "timestamp": datetime.fromtimestamp(now).isoformat(),
                        "type": "window",
                        "subtype": "switch",
                        "details": {
                            "from_app": self.current_app_exe,
                            "to_app": exe,
                            "title": title
                        },
                        "activity": f"Switched to {exe if exe else 'Unknown app'}"
                    }
                    self._add_to_realtime_buffer(activity)
                    self._update_activity_history("window_switch", f"to {exe}")

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
            
            # Log fake activity
            fake_activity = {
                "timestamp": datetime.fromtimestamp(now).isoformat(),
                "type": "suspicious",
                "reason": "fake_activity_detected",
                "details": f"Uniform key spam detected (key: {key_name})"
            }
            self.suspicious_activities.append(fake_activity)
            self.trigger_logout(reason="fake_activity")

    # -------- Logout / session control --------

    def trigger_logout(self, reason: str):
        print(f"[Nagster] Triggering logout due to: {reason}")
        with self.lock:
            self.backend_status = f"Logging out: {reason}"
            self.running = False

        try:
            self.send_to_backend()  # Send final update
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

    # -------- Backend communication (Har 8 second baad) --------

    def build_payload(self):
        now = datetime.utcnow()
        current_time = time.time()

        with self.lock:
            # Prepare activity summary for last 8 seconds
            activity_summary = []
            if self.activity_history:
                # Group activities by type for summary
                activity_counts = {}
                for act in self.activity_history[-50:]:  # Last 50 activities
                    act_type = act["type"]
                    activity_counts[act_type] = activity_counts.get(act_type, 0) + 1
                
                for act_type, count in activity_counts.items():
                    activity_summary.append({
                        "type": act_type,
                        "count": count
                    })
            
            # Get real-time activities from buffer
            realtime_activities = self.realtime_buffer.copy()
            
            # Current app info
            current_app = {
                "exe": self.current_app_exe,
                "title": self.current_app_title,
                "start_time": datetime.fromtimestamp(self.current_app_start_time).isoformat() if self.current_app_start_time else None
            }
            
            # App usage in last 8 seconds
            recent_apps = []
            if self.current_app_exe and self.current_app_start_time:
                current_duration = current_time - self.current_app_start_time
                recent_apps.append({
                    "app_exe": self.current_app_exe,
                    "app_title": self.current_app_title,
                    "duration_seconds": min(current_duration, 8),  # Max 8 seconds
                    "percentage": min((current_duration / 8) * 100, 100)
                })
            
            # Add any other apps used in this interval
            for app_usage in self.app_usage_history:
                recent_apps.append(app_usage)
            
            # Prepare detailed payload
            payload = {
                "employee_id": self.employee_id,
                "timestamp": now.isoformat(),
                "interval_start": datetime.fromtimestamp(current_time - 8).isoformat(),
                "interval_end": now.isoformat(),
                
                # Activity metrics
                "active_seconds": self.active_seconds,
                "idle_seconds": self.idle_seconds,
                "suspicious": self.suspicious_count > 0,
                
                # Detailed activity counts
                "keypresses": self.interval_keypresses,
                "mouse_clicks": self.interval_mouse_clicks,
                "mouse_moves": self.interval_mouse_moves,
                "scrolls": self.interval_scrolls,
                "window_changes": self.interval_window_changes,
                
                # Current state
                "current_app": current_app,
                "current_activity": self._get_current_activity_type(),
                
                # Activity details
                "activity_summary": activity_summary,
                "recent_activities": realtime_activities[-10:],  # Last 10 activities
                "app_usage": recent_apps,
                
                # Suspicious activities if any
                "suspicious_activities": self.suspicious_activities,
                
                # Totals for context
                "total_active_seconds": self.total_active_seconds,
                "total_idle_seconds": self.total_idle_seconds,
                "total_keypresses": self.total_keypresses,
                "total_mouse_events": self.total_mouse_events,
                "total_window_changes": self.total_window_changes,
                
                "interval_seconds": 8,
                "is_realtime_update": True
            }
            
            # Reset interval counters
            self._reset_interval_counters()
            
            self.last_send_ts = current_time
            self.last_send_time_str = now.strftime("%H:%M:%S")

        return payload
    
    def _get_current_activity_type(self):
        """Determine current activity type based on recent actions"""
        now = time.time()
        last_5_seconds = now - 5
        
        # Check recent activities
        recent_keys = 0
        recent_clicks = 0
        recent_moves = 0
        
        for activity in self.activity_history[-20:]:
            if activity["timestamp"] > last_5_seconds:
                if "keypress" in activity["type"]:
                    recent_keys += 1
                elif "click" in activity["type"]:
                    recent_clicks += 1
                elif "move" in activity["type"]:
                    recent_moves += 1
        
        if recent_keys > 5:
            return "typing_heavily"
        elif recent_keys > 0:
            return "typing"
        elif recent_clicks > 3:
            return "clicking"
        elif recent_moves > 10:
            return "navigating"
        elif now - self.last_activity_ts < 5:
            return "active"
        else:
            return "idle"
    
    def _reset_interval_counters(self):
        """Reset counters for next 8-second interval"""
        self.active_seconds = 0
        self.idle_seconds = 0
        self.interval_keypresses = 0
        self.interval_mouse_clicks = 0
        self.interval_mouse_moves = 0
        self.interval_scrolls = 0
        self.interval_window_changes = 0
        self.suspicious_count = 0
        self.suspicious_activities = []
        self.app_usage_history = []
        
        # Keep some history for continuity
        if len(self.activity_history) > 20:
            self.activity_history = self.activity_history[-20:]
        if len(self.realtime_buffer) > 20:
            self.realtime_buffer = self.realtime_buffer[-20:]

    def send_to_backend(self):
        payload = self.build_payload()
        backend_url = self.config["backend_base_url"].rstrip("/") + "/activity"

        try:
            resp = requests.post(
                backend_url,
                json=payload,
                timeout=10,
            )

            if resp.status_code == 200:
                with self.lock:
                    self.backend_status = "Connected"
                
                # Print activity summary
                activity_desc = self._describe_activity(payload)
                print(f"[Nagster] 8-sec update sent: {activity_desc}")
                
                # Also add to session history
                self.session_activities.append({
                    "timestamp": payload["timestamp"],
                    "summary": activity_desc,
                    "active_seconds": payload["active_seconds"],
                    "app": payload["current_app"]["exe"] if payload["current_app"]["exe"] else "Unknown"
                })

            elif resp.status_code == 404:
                with self.lock:
                    self.backend_status = "Employee not registered"
                print("[Nagster] Backend says employee is invalid. Stopping agent.")
                self.stop()
                return

            else:
                with self.lock:
                    self.backend_status = f"Error: {resp.status_code}"
                print("[Nagster] Backend error:", resp.status_code)

        except Exception as e:
            with self.lock:
                self.backend_status = "Failed: cannot reach backend"
            print("[Nagster] Failed to send:", repr(e))
    
    def _describe_activity(self, payload):
        """Create a human-readable description of the activity"""
        desc = []
        
        if payload["keypresses"] > 0:
            desc.append(f"{payload['keypresses']} keys")
        if payload["mouse_clicks"] > 0:
            desc.append(f"{payload['mouse_clicks']} clicks")
        if payload["scrolls"] > 0:
            desc.append(f"{payload['scrolls']} scrolls")
        
        app_name = payload["current_app"]["exe"]
        if app_name:
            # Extract just the exe name without extension
            if "." in app_name:
                app_name = app_name.split(".")[0]
            desc.append(f"on {app_name}")
        
        if payload["active_seconds"] >= 7:
            desc.append("(very active)")
        elif payload["active_seconds"] >= 4:
            desc.append("(active)")
        elif payload["active_seconds"] > 0:
            desc.append("(some activity)")
        else:
            desc.append("(idle)")
        
        return " ".join(desc)

    # -------- Worker loop --------

    def worker_loop(self):
        self.running = True
        interval = self.config["send_interval_seconds"]  # 8 seconds
        idle_logout = self.config.get("idle_logout_seconds", 300)

        print(f"[Nagster] Worker started - Har {interval} second baad update bhejega")

        # Start input listeners
        keyboard_listener = keyboard.Listener(on_press=self.on_key)
        mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll,
        )
        keyboard_listener.start()
        mouse_listener.start()

        try:
            last_tick = time.time()
            while self.running:
                current_time = time.time()
                
                # Update every second for accurate tracking
                if current_time - last_tick >= 1:
                    self.tick_second()
                    last_tick = current_time
                
                # Check conditions
                with self.lock:
                    idle_gap = current_time - self.last_activity_ts
                    session_flags = self.session_suspicious_count

                # Auto-logout checks
                if idle_gap >= idle_logout:
                    print(f"[Nagster] Auto logout: {int(idle_gap)} seconds idle")
                    self.trigger_logout(reason="idle_timeout")
                    break

                if session_flags > 3:
                    print(f"[Nagster] Auto logout: {session_flags} suspicious flags")
                    self.trigger_logout(reason="too_many_suspicious_flags")
                    break

                # Har 8 second baad send karo
                if current_time - self.last_send_ts >= interval:
                    self.send_to_backend()

                # CPU efficient sleep
                time.sleep(0.1)  # 100ms
                
        finally:
            keyboard_listener.stop()
            mouse_listener.stop()
            print("[Nagster] Worker stopped")

    def stop(self):
        self.running = False