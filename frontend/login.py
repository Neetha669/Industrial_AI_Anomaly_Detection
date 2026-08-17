import tkinter as tk
from tkinter import messagebox
import sys
import os


# ============================================================
# PROJECT PATH
# ============================================================

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# LOGIN WINDOW
# ============================================================

class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Industrial AI - Login"
        )

        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        self.root.configure(
            bg="#EEF2F7"
        )

        # Center window
        self.center_window()

        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Build UI
        self.create_ui()

        # Enter key
        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ========================================================
    # CENTER WINDOW
    # ========================================================

    def center_window(self):

        self.root.update_idletasks()

        width = 1000
        height = 650

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ========================================================
    # USER INTERFACE
    # ========================================================

    def create_ui(self):

        # ----------------------------------------------------
        # LEFT PANEL
        # ----------------------------------------------------

        left_panel = tk.Frame(
            self.root,
            bg="#10233F",
            width=430,
            height=650
        )

        left_panel.pack(
            side="left",
            fill="y"
        )

        left_panel.pack_propagate(False)

        # Shield icon
        tk.Label(
            left_panel,
            text="🛡",
            font=("Arial", 55),
            bg="#10233F",
            fg="white"
        ).pack(
            pady=(100, 15)
        )

        # Main title
        tk.Label(
            left_panel,
            text="INDUSTRIAL AI",
            font=("Arial", 25, "bold"),
            bg="#10233F",
            fg="white"
        ).pack()

        tk.Label(
            left_panel,
            text="SAFETY MONITORING SYSTEM",
            font=("Arial", 11, "bold"),
            bg="#10233F",
            fg="#93C5FD"
        ).pack(
            pady=(5, 30)
        )

        # Description
        tk.Label(
            left_panel,
            text=(
                "Real-Time AI-Based Industrial\n"
                "Anomaly Detection System"
            ),
            font=("Arial", 13),
            bg="#10233F",
            fg="#E2E8F0",
            justify="center"
        ).pack(
            pady=10
        )

        # Features
        features = (
            "✓ Worker Detection\n"
            "✓ Danger Zone Monitoring\n"
            "✓ Fall Detection\n"
            "✓ Machine Anomaly Detection"
        )

        tk.Label(
            left_panel,
            text=features,
            font=("Arial", 10),
            bg="#10233F",
            fg="#CBD5E1",
            justify="left"
        ).pack(
            pady=35
        )

        tk.Label(
            left_panel,
            text="AI • SAFETY • MONITORING",
            font=("Arial", 8, "bold"),
            bg="#10233F",
            fg="#64748B"
        ).pack(
            side="bottom",
            pady=25
        )

        # ----------------------------------------------------
        # RIGHT PANEL
        # ----------------------------------------------------

        right_panel = tk.Frame(
            self.root,
            bg="#F8FAFC",
            width=570,
            height=650
        )

        right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )

        right_panel.pack_propagate(False)

        # Login container
        login_container = tk.Frame(
            right_panel,
            bg="#FFFFFF",
            bd=1,
            relief="solid"
        )

        login_container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=400,
            height=455
        )

        # ----------------------------------------------------
        # LOGIN TITLE
        # ----------------------------------------------------

        tk.Label(
            login_container,
            text="Welcome Back",
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            pady=(35, 5)
        )

        tk.Label(
            login_container,
            text="Sign in to access the safety dashboard",
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        ).pack(
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        tk.Label(
            login_container,
            text="USERNAME",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=45
        )

        username_frame = tk.Frame(
            login_container,
            bg="#F1F5F9",
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        username_frame.pack(
            fill="x",
            padx=45,
            pady=(7, 18)
        )

        tk.Label(
            username_frame,
            text="👤",
            font=("Arial", 12),
            bg="#F1F5F9",
            fg="#64748B"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            font=("Arial", 11),
            bg="#F1F5F9",
            fg="#172033",
            relief="flat",
            bd=0
        )

        self.username_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        tk.Label(
            login_container,
            text="PASSWORD",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=45
        )

        password_frame = tk.Frame(
            login_container,
            bg="#F1F5F9",
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        password_frame.pack(
            fill="x",
            padx=45,
            pady=(7, 10)
        )

        tk.Label(
            password_frame,
            text="🔒",
            font=("Arial", 12),
            bg="#F1F5F9",
            fg="#64748B"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Arial", 11),
            bg="#F1F5F9",
            fg="#172033",
            show="•",
            relief="flat",
            bd=0
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        # ----------------------------------------------------
        # SHOW PASSWORD
        # ----------------------------------------------------

        self.show_password_var = tk.BooleanVar(
            value=False
        )

        tk.Checkbutton(
            login_container,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=("Arial", 8),
            bg="white",
            fg="#64748B",
            activebackground="white",
            activeforeground="#64748B",
            selectcolor="white"
        ).pack(
            anchor="w",
            padx=43,
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # LOGIN BUTTON
        # ----------------------------------------------------

        self.login_button = tk.Button(
            login_container,
            text="LOGIN",
            font=("Arial", 11, "bold"),
            bg="#1F4FA3",
            fg="white",
            activebackground="#163A7A",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.login
        )

        self.login_button.pack(
            fill="x",
            padx=45,
            ipady=10,
            pady=(5, 15)
        )

        # Hover effects
        self.login_button.bind(
            "<Enter>",
            lambda event:
            self.login_button.configure(
                bg="#163A7A"
            )
        )

        self.login_button.bind(
            "<Leave>",
            lambda event:
            self.login_button.configure(
                bg="#1F4FA3"
            )
        )

        # ----------------------------------------------------
        # DEFAULT LOGIN INFO
        # ----------------------------------------------------

        tk.Label(
            login_container,
            text="Default administrator account",
            font=("Arial", 8),
            bg="white",
            fg="#94A3B8"
        ).pack(
            pady=(3, 2)
        )

        tk.Label(
            login_container,
            text="Username: admin   |   Password: admin123",
            font=("Arial", 8, "bold"),
            bg="white",
            fg="#64748B"
        ).pack()

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        tk.Label(
            right_panel,
            text="Industrial AI Anomaly Detection System • Version 1.0",
            font=("Arial", 8),
            bg="#F8FAFC",
            fg="#94A3B8"
        ).pack(
            side="bottom",
            pady=15
        )

        # Focus username
        self.username_entry.focus()

    # ========================================================
    # SHOW / HIDE PASSWORD
    # ========================================================

    def toggle_password(self):

        if self.show_password_var.get():

            self.password_entry.configure(
                show=""
            )

        else:

            self.password_entry.configure(
                show="•"
            )

    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = self.username_var.get().strip()
        password = self.password_var.get()

        # ----------------------------------------------------
        # LOGIN CREDENTIALS
        # ----------------------------------------------------

        valid_username = "admin"
        valid_password = "admin123"

        # Empty fields
        if not username or not password:

            messagebox.showwarning(
                "Login Required",
                "Please enter both username and password.",
                parent=self.root
            )

            return

        # Correct login
        if (
            username == valid_username
            and password == valid_password
        ):

            self.open_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.",
                parent=self.root
            )

            self.password_var.set("")

            self.password_entry.focus()

    # ========================================================
    # OPEN DASHBOARD
    # ========================================================

    def open_dashboard(self):

        try:

            # Import your Dashboard class
            from frontend.dashboard import Dashboard

        except ImportError:

            messagebox.showerror(
                "Dashboard Error",
                (
                    "Could not load dashboard.py.\n\n"
                    "Make sure dashboard.py is inside:\n"
                    "frontend/"
                ),
                parent=self.root
            )

            return

        # Close login window
        self.root.destroy()

        # Create dashboard window
        dashboard_root = tk.Tk()

        Dashboard(
            dashboard_root
        )

        dashboard_root.mainloop()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = LoginWindow(root)

    root.mainloop()