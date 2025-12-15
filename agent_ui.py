# agent_ui.py

import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime

from agent_core import (
    NagsterAgent,
    load_config_file,
    save_config_file,
    verify_employee_with_backend,
    DEFAULT_BASE_URL,
)

# Clean Professional Colors
COLORS = {
    "primary": "#2563eb",
    "primary_light": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "background": "#f8fafc",
    "card": "#ffffff",
    "border": "#e2e8f0",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
    "text_light": "#94a3b8"
}

class CompactNagsterUI:
    def __init__(self, agent: NagsterAgent):
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Nagster Agent")
        self.root.geometry("400x300")
        self.root.minsize(380, 280)
        self.root.configure(bg=COLORS["background"])
        self.root.resizable(True, True)
        
        # Center window
        self.center_window()
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_attempt)
        
        self.worker_thread = threading.Thread(
            target=self.agent.worker_loop, daemon=True
        )
        self.worker_thread.start()
        
        self.update_ui()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=COLORS["background"], padx=20, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS["background"])
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=COLORS["background"])
        title_frame.pack(side="left")
        
        tk.Label(
            title_frame,
            text="⚡",
            font=("Segoe UI", 16),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(side="left")
        
        tk.Label(
            title_frame,
            text="Nagster",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(side="left", padx=(5, 0))
        
        # Status indicator
        self.status_indicator = tk.Label(
            header_frame,
            text="●",
            font=("Segoe UI", 12),
            bg=COLORS["background"],
            fg=COLORS["success"]
        )
        self.status_indicator.pack(side="right", padx=(0, 5))
        
        self.status_label = tk.Label(
            header_frame,
            text="ACTIVE",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["success"]
        )
        self.status_label.pack(side="right")
        
        # Stats Cards Row
        stats_frame = tk.Frame(main_frame, bg=COLORS["background"])
        stats_frame.pack(fill="x", pady=(0, 15))
        
        # Active Time Card
        self.active_card = self.create_stat_card(stats_frame, "Active Time", "0s", COLORS["primary"])
        self.active_card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Idle Time Card  
        self.idle_card = self.create_stat_card(stats_frame, "Idle Time", "0s", COLORS["warning"])
        self.idle_card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        # Suspicious Card
        self.suspicious_card = self.create_stat_card(stats_frame, "Suspicious", "0", COLORS["danger"])
        self.suspicious_card.pack(side="left", fill="x", expand=True)
        
        # Current Application
        app_frame = tk.Frame(
            main_frame,
            bg=COLORS["card"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        app_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            app_frame,
            text="Current Application",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["card"],
            fg=COLORS["text_primary"],
            anchor="w"
        ).pack(fill="x", padx=12, pady=(10, 5))
        
        self.app_label = tk.Label(
            app_frame,
            text="No active application",
            font=("Segoe UI", 9),
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
            anchor="w",
            wraplength=350
        )
        self.app_label.pack(fill="x", padx=12, pady=(0, 10))
        
        # Connection Info
        info_frame = tk.Frame(main_frame, bg=COLORS["background"])
        info_frame.pack(fill="x", pady=(0, 15))
        
        # Backend status
        backend_frame = tk.Frame(info_frame, bg=COLORS["background"])
        backend_frame.pack(fill="x", pady=2)
        
        tk.Label(
            backend_frame,
            text="Backend:",
            font=("Segoe UI", 9),
            bg=COLORS["background"],
            fg=COLORS["text_secondary"]
        ).pack(side="left")
        
        self.backend_status = tk.Label(
            backend_frame,
            text="Connected",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["background"],
            fg=COLORS["success"]
        )
        self.backend_status.pack(side="left", padx=(5, 0))
        
        # Last sync
        sync_frame = tk.Frame(info_frame, bg=COLORS["background"])
        sync_frame.pack(fill="x", pady=2)
        
        tk.Label(
            sync_frame,
            text="Last Sync:",
            font=("Segoe UI", 9),
            bg=COLORS["background"],
            fg=COLORS["text_secondary"]
        ).pack(side="left")
        
        self.sync_label = tk.Label(
            sync_frame,
            text="Never",
            font=("Segoe UI", 9),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        )
        self.sync_label.pack(side="left", padx=(5, 0))
        
        # Employee ID
        emp_frame = tk.Frame(info_frame, bg=COLORS["background"])
        emp_frame.pack(fill="x", pady=2)
        
        tk.Label(
            emp_frame,
            text="Employee:",
            font=("Segoe UI", 9),
            bg=COLORS["background"],
            fg=COLORS["text_secondary"]
        ).pack(side="left")
        
        tk.Label(
            emp_frame,
            text=self.agent.employee_id,
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(side="left", padx=(5, 0))
        
        # Footer with stop button
        footer_frame = tk.Frame(main_frame, bg=COLORS["background"])
        footer_frame.pack(fill="x", pady=(10, 0))
        
        # Version info
        tk.Label(
            footer_frame,
            text="v2.0",
            font=("Segoe UI", 8),
            bg=COLORS["background"],
            fg=COLORS["text_light"]
        ).pack(side="left")
        
        # Stop button
        self.stop_btn = tk.Button(
            footer_frame,
            text="Stop Agent",
            command=self.on_stop_click,
            font=("Segoe UI", 10),
            bg=COLORS["danger"],
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=6
        )
        self.stop_btn.pack(side="right")

    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(
            parent,
            bg=COLORS["card"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=10,
            pady=8
        )
        
        # Title
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8),
            bg=COLORS["card"],
            fg=COLORS["text_secondary"]
        ).pack(anchor="w")
        
        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["card"],
            fg=color
        )
        value_label.pack(anchor="w", pady=(2, 0))
        
        return {"frame": card, "value_label": value_label}

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    def update_ui(self):
        with self.agent.lock:
            # Agent status
            if self.agent.running:
                self.status_label.config(text="ACTIVE", fg=COLORS["success"])
                self.status_indicator.config(fg=COLORS["success"])
            else:
                self.status_label.config(text="STOPPED", fg=COLORS["danger"])
                self.status_indicator.config(fg=COLORS["danger"])
            
            # Update stats cards
            active_total = self.agent.total_active_seconds
            idle_total = self.agent.total_idle_seconds
            
            self.active_card["value_label"].config(text=self.format_time(active_total))
            self.idle_card["value_label"].config(text=self.format_time(idle_total))
            self.suspicious_card["value_label"].config(text=str(self.agent.session_suspicious_count))
            
            # Update application info
            exe = self.agent.current_app_exe
            title = self.agent.current_app_title
            if exe or title:
                app_text = f"{exe or 'Unknown'} | {title or 'No title'}"
                self.app_label.config(text=app_text)
            else:
                self.app_label.config(text="No active application")
            
            # Update connection info
            backend_status = self.agent.backend_status
            backend_color = COLORS["success"] if "Connected" in backend_status else COLORS["danger"]
            self.backend_status.config(text=backend_status, fg=backend_color)
            
            self.sync_label.config(text=self.agent.last_send_time_str)
        
        # Schedule next update
        self.root.after(1000, self.update_ui)

    def on_close_attempt(self):
        # Allow closing with window [X] but show confirmation
        if tk.messagebox.askokcancel("Quit", "Do you want to stop the Nagster agent?"):
            self.on_stop_click()

    def on_stop_click(self):
        try:
            print("[Nagster] Sending final activity log...")
            self.agent.send_to_backend()
        except Exception as e:
            print("[Nagster] Final send failed:", repr(e))
        
        self.agent.stop()
        self.root.after(500, self.root.destroy)

    def run(self):
        self.root.mainloop()

# Simple Login Popup
def prompt_employee_id_popup(config: dict):
    backend_base = config.get("backend_base_url", DEFAULT_BASE_URL)
    result = {"employee_id": None, "remember": False}

    root = tk.Tk()
    root.title("Nagster Login")
    root.geometry("350x200")
    root.resizable(False, False)
    root.configure(bg=COLORS["background"])
    
    # Center window
    root.update_idletasks()
    w, h = 350, 200
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # Header
    header = tk.Frame(root, bg=COLORS["primary"], height=60)
    header.pack(fill="x", pady=(0, 20))
    header.pack_propagate(False)
    
    tk.Label(
        header,
        text="Nagster Login",
        font=("Segoe UI", 14, "bold"),
        bg=COLORS["primary"],
        fg="white"
    ).pack(expand=True)
    
    # Content
    content = tk.Frame(root, bg=COLORS["background"], padx=25)
    content.pack(fill="both", expand=True)
    
    tk.Label(
        content,
        text="Enter Employee ID:",
        font=("Segoe UI", 10),
        bg=COLORS["background"],
        fg=COLORS["text_primary"]
    ).pack(anchor="w", pady=(0, 8))
    
    entry = tk.Entry(
        content,
        font=("Segoe UI", 11),
        relief="flat",
        bd=1,
        highlightthickness=1,
        highlightcolor=COLORS["primary"]
    )
    entry.pack(fill="x", pady=(0, 12), ipady=6)
    entry.focus_set()
    
    remember_var = tk.IntVar(value=1 if config.get("remember_me") else 0)
    chk = tk.Checkbutton(
        content,
        text="Remember me",
        variable=remember_var,
        font=("Segoe UI", 9),
        bg=COLORS["background"],
        fg=COLORS["text_secondary"]
    )
    chk.pack(anchor="w", pady=(0, 15))
    
    def authenticate():
        emp_id = entry.get().strip()
        if not emp_id:
            tk.messagebox.showerror("Error", "Please enter Employee ID")
            return
        
        btn.config(text="Verifying...", state="disabled")
        root.update()
        
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
            tk.messagebox.showerror("Error", "Employee ID not found")
            btn.config(text="Login", state="normal")
    
    btn = tk.Button(
        content,
        text="Login",
        command=authenticate,
        font=("Segoe UI", 10, "bold"),
        bg=COLORS["primary"],
        fg="white",
        relief="flat",
        bd=0,
        padx=25,
        pady=8
    )
    btn.pack()
    
    entry.bind("<Return>", lambda e: authenticate())
    
    def on_close():
        root.destroy()
        raise SystemExit(0)
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    
    emp_id = result["employee_id"]
    if not emp_id:
        raise SystemExit(0)
    
    return emp_id, result["remember"]