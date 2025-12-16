# agent_ui.py

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
from datetime import datetime
import sys
import os

from agent_core import (
    NagsterAgent,
    load_config_file,
    save_config_file,
    verify_employee_with_backend,
    DEFAULT_BASE_URL,
)

# Professional Dark Theme - React Style
COLORS = {
    # Backgrounds
    "bg_dark": "#0d1117",           # GitHub Dark
    "bg_card": "#161b22",           # Dark Card
    "bg_hover": "#21262d",          # Hover State
    
    # Primary Colors
    "primary": "#58a6ff",           # GitHub Blue
    "primary_dark": "#1f6feb",
    "secondary": "#238636",         # GitHub Green
    "accent": "#8957e5",            # Purple
    
    # Status Colors
    "success": "#3fb950",           # Bright Green
    "warning": "#d29922",           # Amber/Gold
    "danger": "#f85149",            # Red
    "info": "#58a6ff",              # Blue
    
    # Text Colors
    "text_primary": "#f0f6fc",      # White
    "text_secondary": "#8b949e",    # Gray
    "text_muted": "#6e7681",        # Dark Gray
    
    # Borders & Dividers
    "border": "#30363d",
    "border_light": "#3c444d",
    
    # UI Elements
    "shadow": "rgba(0, 0, 0, 0.4)",
    "overlay": "rgba(0, 0, 0, 0.6)"
}

class CompactNagsterUI:
    def __init__(self, agent: NagsterAgent):
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Nagster Agent")
        self.root.geometry("480x400")
        self.root.minsize(480, 400)
        
        # Apply dark theme
        self.root.configure(bg=COLORS["bg_dark"])
        
        # Set custom icon if available
        try:
            self.root.iconbitmap('nagster_icon.ico') if os.path.exists('nagster_icon.ico') else None
        except:
            pass
        
        # Center window
        self.center_window()
        
        # Create custom title bar
        self.create_title_bar()
        
        # Main content
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_attempt)
        
        # Start worker thread
        self.worker_thread = threading.Thread(
            target=self.agent.worker_loop, daemon=True
        )
        self.worker_thread.start()
        
        # Start UI updates
        self.update_ui()

    def create_title_bar(self):
        """Create minimal professional title bar"""
        title_bar = tk.Frame(self.root, bg=COLORS["bg_card"], height=36)
        title_bar.pack(fill="x", padx=0, pady=0)
        title_bar.pack_propagate(False)
        
        # Drag functionality
        def start_move(event):
            self.root.x = event.x
            self.root.y = event.y
            
        def stop_move(event):
            self.root.x = None
            self.root.y = None
            
        def do_move(event):
            deltax = event.x - self.root.x
            deltay = event.y - self.root.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
            
        title_bar.bind("<ButtonPress-1>", start_move)
        title_bar.bind("<ButtonRelease-1>", stop_move)
        title_bar.bind("<B1-Motion>", do_move)
        
        # Logo and Title
        logo_frame = tk.Frame(title_bar, bg=COLORS["bg_card"])
        logo_frame.pack(side="left", padx=15)
        
        # Nagster Text Logo
        tk.Label(
            logo_frame,
            text="NAGSTER",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["primary"]
        ).pack(side="left")
        
        tk.Label(
            logo_frame,
            text="AGENT",
            font=("Segoe UI", 11),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"]
        ).pack(side="left", padx=(2, 0))
        
        # Window Controls
        controls_frame = tk.Frame(title_bar, bg=COLORS["bg_card"])
        controls_frame.pack(side="right")
        
        # Minimize button
        min_btn = tk.Button(
            controls_frame,
            text="–",
            command=self.root.iconify,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            relief="flat",
            bd=0,
            width=3,
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["text_primary"],
            cursor="hand2"
        )
        min_btn.pack(side="left")
        
        # Close button
        close_btn = tk.Button(
            controls_frame,
            text="×",
            command=lambda: sys.exit(0),
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            relief="flat",
            bd=0,
            width=3,
            activebackground=COLORS["danger"],
            activeforeground="white",
            cursor="hand2"
        )
        close_btn.pack(side="left")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=COLORS["bg_dark"], padx=24, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header with status
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
        header_frame.pack(fill="x", pady=(0, 24))
        
        # Status indicator
        status_frame = tk.Frame(header_frame, bg=COLORS["bg_dark"])
        status_frame.pack(side="left")
        
        # Status dot
        status_dot = tk.Frame(
            status_frame,
            width=8,
            height=8,
            bg=COLORS["success"],
            relief="flat",
            bd=0
        )
        status_dot.pack(side="left", padx=(0, 8))
        
        # Status text
        self.status_label = tk.Label(
            status_frame,
            text="ACTIVE MONITORING",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["success"]
        )
        self.status_label.pack(side="left")
        
        # Employee ID badge
        emp_frame = tk.Frame(header_frame, bg=COLORS["bg_dark"])
        emp_frame.pack(side="right")
        
        tk.Label(
            emp_frame,
            text="EMPLOYEE",
            font=("Segoe UI", 8),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"]
        ).pack(anchor="e")
        
        tk.Label(
            emp_frame,
            text=self.agent.employee_id,
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["primary"]
        ).pack(anchor="e")
        
        # Metrics Grid
        metrics_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
        metrics_frame.pack(fill="x", pady=(0, 24))
        
        # Create metric cards
        self.active_card = self.create_metric_card(
            metrics_frame,
            "ACTIVE TIME",
            "0s",
            COLORS["success"],
            "Activity duration when user is actively working"
        )
        self.active_card.pack(side="left", fill="both", expand=True, padx=(0, 12))
        
        self.idle_card = self.create_metric_card(
            metrics_frame,
            "IDLE TIME",
            "0s",
            COLORS["warning"],
            "Duration without keyboard/mouse activity"
        )
        self.idle_card.pack(side="left", fill="both", expand=True, padx=(0, 12))
        
        self.suspicious_card = self.create_metric_card(
            metrics_frame,
            "SUSPICIOUS",
            "0",
            COLORS["danger"],
            "Suspicious activity patterns detected"
        )
        self.suspicious_card.pack(side="left", fill="both", expand=True)
        
        # Application Card
        app_card = tk.Frame(
            main_frame,
            bg=COLORS["bg_card"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=16,
            pady=16
        )
        app_card.pack(fill="x", pady=(0, 24))
        
        # Card header
        card_header = tk.Frame(app_card, bg=COLORS["bg_card"])
        card_header.pack(fill="x", pady=(0, 12))
        
        tk.Label(
            card_header,
            text="CURRENT APPLICATION",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
            anchor="w"
        ).pack(side="left")
        
        # App divider
        tk.Frame(
            app_card,
            height=1,
            bg=COLORS["border"],
            relief="flat"
        ).pack(fill="x", pady=(0, 12))
        
        # Application info
        self.app_label = tk.Label(
            app_card,
            text="No active application detected",
            font=("Segoe UI", 11),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        )
        self.app_label.pack(fill="x")
        
        # Status Bar
        status_bar = tk.Frame(main_frame, bg=COLORS["bg_card"], height=32)
        status_bar.pack(fill="x", side="bottom", pady=(0, 0))
        status_bar.pack_propagate(False)
        
        # Left status
        left_status = tk.Frame(status_bar, bg=COLORS["bg_card"], padx=16)
        left_status.pack(side="left", fill="y")
        
        tk.Label(
            left_status,
            text="SERVER",
            font=("Segoe UI", 8),
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"]
        ).pack(side="left", padx=(0, 4))
        
        self.backend_status = tk.Label(
            left_status,
            text="CONNECTED",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["success"]
        )
        self.backend_status.pack(side="left")
        
        # Right status
        right_status = tk.Frame(status_bar, bg=COLORS["bg_card"], padx=16)
        right_status.pack(side="right", fill="y")
        
        tk.Label(
            right_status,
            text="LAST SYNC",
            font=("Segoe UI", 8),
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"]
        ).pack(side="left", padx=(0, 4))
        
        self.sync_label = tk.Label(
            right_status,
            text="NEVER",
            font=("Segoe UI", 9),
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"]
        )
        self.sync_label.pack(side="left")
        
        # Action Buttons Frame
        actions_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
        actions_frame.pack(fill="x", pady=(20, 0))
        
        # Version info
        tk.Label(
            actions_frame,
            text="v2.0.1",
            font=("Segoe UI", 8),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"]
        ).pack(side="left")
        
        # Stop button
        self.stop_btn = tk.Button(
            actions_frame,
            text="STOP MONITORING",
            command=self.on_stop_click,
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["danger"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=24,
            pady=8,
            cursor="hand2",
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["danger"]
        )
        self.stop_btn.pack(side="right")

    def create_metric_card(self, parent, title, value, color, tooltip=""):
        """Create a professional metric card"""
        card = tk.Frame(
            parent,
            bg=COLORS["bg_card"],
            relief="flat",
            bd=1,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=16,
            pady=16
        )
        
        # Title
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9),
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["bg_card"],
            fg=color,
            anchor="w"
        )
        value_label.pack(fill="x")
        
        # Store reference
        card.value_label = value_label
        
        # Add hover effect
        def on_enter(e):
            card.configure(bg=COLORS["bg_hover"])
            for child in card.winfo_children():
                child.configure(bg=COLORS["bg_hover"])
        
        def on_leave(e):
            card.configure(bg=COLORS["bg_card"])
            for child in card.winfo_children():
                child.configure(bg=COLORS["bg_card"])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card

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
        try:
            with self.agent.lock:
                # Update status
                if self.agent.running:
                    self.status_label.config(text="ACTIVE MONITORING", fg=COLORS["success"])
                else:
                    self.status_label.config(text="MONITORING STOPPED", fg=COLORS["danger"])
                
                # Update metrics
                active_total = self.agent.total_active_seconds
                idle_total = self.agent.total_idle_seconds
                
                self.active_card.value_label.config(text=self.format_time(active_total))
                self.idle_card.value_label.config(text=self.format_time(idle_total))
                self.suspicious_card.value_label.config(text=str(self.agent.session_suspicious_count))
                
                # Update application info
                exe = self.agent.current_app_exe
                title = self.agent.current_app_title
                if exe or title:
                    # Format nicely
                    if exe and title:
                        app_text = f"{exe} - {title}"
                    elif exe:
                        app_text = exe
                    else:
                        app_text = title
                    
                    # Truncate if too long
                    if len(app_text) > 50:
                        app_text = app_text[:47] + "..."
                    
                    self.app_label.config(text=app_text)
                else:
                    self.app_label.config(text="No active application detected")
                
                # Update backend status
                backend_status = self.agent.backend_status
                if any(word in backend_status.upper() for word in ["CONNECTED", "SUCCESS"]):
                    self.backend_status.config(text="CONNECTED", fg=COLORS["success"])
                elif any(word in backend_status.upper() for word in ["FAILED", "ERROR", "DISCONNECTED"]):
                    self.backend_status.config(text="DISCONNECTED", fg=COLORS["danger"])
                else:
                    self.backend_status.config(text=backend_status.upper(), fg=COLORS["warning"])
                
                self.sync_label.config(text=self.agent.last_send_time_str.upper())
        
        except Exception as e:
            print(f"[UI Update Error] {e}")
        
        # Schedule next update
        self.root.after(1000, self.update_ui)

    def on_close_attempt(self):
        # Professional confirmation dialog
        if messagebox.askyesno(
            "Stop Monitoring", 
            "Are you sure you want to stop monitoring?\n\nYour session data will be saved.",
            icon='question',
            default='no'
        ):
            self.on_stop_click()

    def on_stop_click(self):
        try:
            print("[Nagster] Sending final session data...")
            self.agent.send_to_backend()
        except Exception as e:
            print("[Nagster] Final send failed:", repr(e))
        
        self.agent.stop()
        self.root.after(300, self.root.destroy)

    def run(self):
        self.root.mainloop()

# Professional Login Dialog
def prompt_employee_id_popup(config: dict):
    backend_base = config.get("backend_base_url", DEFAULT_BASE_URL)
    result = {"employee_id": None, "remember": False}

    root = tk.Tk()
    root.title("Nagster Authentication")
    root.geometry("420x300")
    root.resizable(False, False)
    root.configure(bg=COLORS["bg_dark"])
    
    # Make it modal
    root.attributes('-topmost', True)
    
    # Center window
    root.update_idletasks()
    w, h = 420, 300
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    
    # Main content
    main_frame = tk.Frame(root, bg=COLORS["bg_dark"], padx=32, pady=32)
    main_frame.pack(fill="both", expand=True)
    
    # Logo/Header
    header_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
    header_frame.pack(fill="x", pady=(0, 24))
    
    tk.Label(
        header_frame,
        text="NAGSTER",
        font=("Segoe UI", 18, "bold"),
        bg=COLORS["bg_dark"],
        fg=COLORS["primary"]
    ).pack(anchor="w")
    
    tk.Label(
        header_frame,
        text="EMPLOYEE AUTHENTICATION",
        font=("Segoe UI", 10),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"]
    ).pack(anchor="w", pady=(4, 0))
    
    # Input section
    input_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
    input_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(
        input_frame,
        text="EMPLOYEE ID",
        font=("Segoe UI", 9),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_muted"]
    ).pack(anchor="w", pady=(0, 8))
    
    entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 12),
        bg=COLORS["bg_card"],
        fg=COLORS["text_primary"],
        relief="flat",
        bd=1,
        highlightthickness=1,
        highlightcolor=COLORS["primary"],
        highlightbackground=COLORS["border"],
        insertbackground=COLORS["primary"]
    )
    entry.pack(fill="x", pady=(0, 16), ipady=10)
    entry.focus_set()
    
    # Remember me
    remember_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
    remember_frame.pack(fill="x", pady=(0, 24))
    
    remember_var = tk.IntVar(value=1 if config.get("remember_me") else 0)
    
    chk = tk.Checkbutton(
        remember_frame,
        text="Remember this device",
        variable=remember_var,
        font=("Segoe UI", 9),
        bg=COLORS["bg_dark"],
        fg=COLORS["text_secondary"],
        selectcolor=COLORS["bg_card"],
        activebackground=COLORS["bg_dark"],
        activeforeground=COLORS["text_secondary"],
        relief="flat"
    )
    chk.pack(anchor="w")
    
    # Login button
    def authenticate():
        emp_id = entry.get().strip()
        if not emp_id:
            messagebox.showerror(
                "Input Required",
                "Please enter your Employee ID",
                parent=root
            )
            return
        
        btn.config(text="AUTHENTICATING...", state="disabled")
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
            messagebox.showerror(
                "Authentication Failed",
                "Invalid Employee ID or server connection failed.\nPlease check your ID and try again.",
                parent=root
            )
            btn.config(text="LOGIN", state="normal")
    
    btn = tk.Button(
        main_frame,
        text="LOGIN",
        command=authenticate,
        font=("Segoe UI", 11, "bold"),
        bg=COLORS["primary"],
        fg="white",
        relief="flat",
        bd=0,
        padx=32,
        pady=12,
        cursor="hand2",
        activebackground=COLORS["primary_dark"],
        activeforeground="white"
    )
    btn.pack()
    
    entry.bind("<Return>", lambda e: authenticate())
    
    # Cancel button (ESC to close)
    def cancel_auth():
        root.destroy()
        sys.exit(0)
    
    root.bind("<Escape>", lambda e: cancel_auth())
    
    root.mainloop()
    
    emp_id = result["employee_id"]
    if not emp_id:
        raise SystemExit(0)
    
    return emp_id, result["remember"]