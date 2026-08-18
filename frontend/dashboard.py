import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os
import sys
import json
import subprocess


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

STATUS_FILE = os.path.join(
    DATA_DIR,
    "latest_status.json"
)

LATEST_IMAGE = os.path.join(
    DATA_DIR,
    "latest_monitoring.jpg"
)


# ============================================================
# DASHBOARD
# ============================================================

class Dashboard:

    def __init__(self, root):

        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================

        self.root.title(
            "Industrial AI-Based Anomaly Detection System"
        )

        self.root.geometry("1250x750")
        self.root.minsize(1100, 650)

        self.root.configure(
            bg="#EEF2F7"
        )

        # ====================================================
        # SYSTEM VALUES
        # ====================================================

        self.worker_status = "SAFE"
        self.machine_status = "NORMAL"
        self.alert_count = 0
        self.latest_alert = "No active alerts"

        self.latest_photo = None

        # ====================================================
        # CREATE UI
        # ====================================================

        self.create_sidebar()
        self.create_main_window()

        self.update_clock()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg="#10233F",
            width=240
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        tk.Label(
            self.sidebar,
            text="INDUSTRIAL AI",
            font=("Arial", 18, "bold"),
            bg="#10233F",
            fg="white"
        ).pack(
            pady=(28, 2)
        )

        tk.Label(
            self.sidebar,
            text="SAFETY MONITORING SYSTEM",
            font=("Arial", 8, "bold"),
            bg="#10233F",
            fg="#93C5FD"
        ).pack(
            pady=(0, 25)
        )

        tk.Frame(
            self.sidebar,
            bg="#29476D",
            height=1
        ).pack(
            fill="x",
            padx=20
        )

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        self.create_nav_button(
            "🏠",
            "HOME",
            self.show_home,
            True
        )

        self.create_nav_button(
            "📹",
            "LIVE MONITORING",
            self.show_live_monitoring
        )

        self.create_nav_button(
            "👤",
            "WORKER STATUS",
            self.show_worker_status
        )

        self.create_nav_button(
            "⚙",
            "MACHINE HEALTH",
            self.show_machine_health
        )

        self.create_nav_button(
            "🌡",
            "TEMPERATURE",
            self.show_temperature
        )

        self.create_nav_button(
            "〽",
            "VIBRATION",
            self.show_vibration
        )

        self.create_nav_button(
            "🚨",
            "ALERTS",
            self.show_alerts
        )

        self.create_nav_button(
            "📋",
            "INCIDENT LOGS",
            self.show_incident_logs
        )

        self.create_nav_button(
            "📊",
            "REPORTS",
            self.show_reports
        )

        self.create_nav_button(
            "🔧",
            "SETTINGS",
            self.show_settings
        )

        self.create_nav_button(
            "ⓘ",
            "ABOUT",
            self.show_about
        )

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        logout_frame = tk.Frame(
            self.sidebar,
            bg="#10233F"
        )

        logout_frame.pack(
            side="bottom",
            fill="x",
            pady=15
        )

        tk.Button(
            logout_frame,
            text="  🚪   LOGOUT",
            font=("Segoe UI Emoji", 10, "bold"),
            anchor="w",
            bg="#10233F",
            fg="#FCA5A5",
            activebackground="#7F1D1D",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.logout
        ).pack(
            fill="x",
            padx=15,
            pady=2
        )

    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def create_nav_button(
        self,
        icon,
        text,
        command,
        active=False
    ):

        background = (
            "#1F4FA3"
            if active
            else "#10233F"
        )

        button = tk.Button(
            self.sidebar,
            text=f"  {icon}   {text}",
            font=("Segoe UI Emoji", 10, "bold"),
            anchor="w",
            height=2,
            bg=background,
            fg="white",
            activebackground="#1F4FA3",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="x",
            padx=10,
            pady=2
        )

    # ========================================================
    # MAIN WINDOW
    # ========================================================

    def create_main_window(self):

        self.main = tk.Frame(
            self.root,
            bg="#EEF2F7"
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_header()

        self.content = tk.Frame(
            self.main,
            bg="#EEF2F7"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.show_home()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.main,
            bg="white",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        self.page_title = tk.Label(
            header,
            text="HOME",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#172033"
        )

        self.page_title.pack(
            side="left",
            padx=25
        )

        right = tk.Frame(
            header,
            bg="white"
        )

        right.pack(
            side="right",
            padx=25
        )

        tk.Label(
            right,
            text="ADMIN",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#1F4FA3"
        ).pack(
            side="left",
            padx=20
        )

        self.clock_label = tk.Label(
            right,
            text="",
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        )

        self.clock_label.pack(
            side="left"
        )

    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ========================================================
    # BACK BUTTON
    # ========================================================

    def create_back_button(self):

        tk.Button(
            self.content,
            text="←  BACK TO HOME",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#1F4FA3",
            activebackground="#E8F0FE",
            activeforeground="#1F4FA3",
            relief="solid",
            bd=1,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.show_home
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

    # ========================================================
    # HOME
    # ========================================================

    def show_home(self):

        self.page_title.config(
            text="HOME"
        )

        self.clear_content()

        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            self.content,
            text="System Overview",
            font=("Arial", 20, "bold"),
            bg="#EEF2F7",
            fg="#172033"
        ).pack(
            anchor="w"
        )

        tk.Label(
            self.content,
            text=(
                "Real-time industrial safety monitoring "
                "and anomaly detection overview"
            ),
            font=("Arial", 9),
            bg="#EEF2F7",
            fg="#64748B"
        ).pack(
            anchor="w",
            pady=(4, 15)
        )

        # ====================================================
        # READ LATEST DATA
        # ====================================================

        self.read_latest_data()

        # ====================================================
        # STATUS CARDS
        # ====================================================

        cards = tk.Frame(
            self.content,
            bg="#EEF2F7"
        )

        cards.pack(
            fill="x"
        )

        self.system_card = self.status_card(
            cards,
            "SYSTEM STATUS",
            "ONLINE",
            "#16A34A"
        )

        self.worker_card = self.status_card(
            cards,
            "WORKER STATUS",
            self.worker_status,
            "#16A34A"
        )

        self.machine_card = self.status_card(
            cards,
            "MACHINE STATUS",
            self.machine_status,
            "#2563EB"
        )

        self.alert_card = self.status_card(
            cards,
            "ACTIVE ALERTS",
            str(self.alert_count),
            "#64748B"
        )

        # ====================================================
        # LOWER AREA
        # ====================================================

        lower = tk.Frame(
            self.content,
            bg="#EEF2F7"
        )

        lower.pack(
            fill="both",
            expand=True,
            pady=15
        )

        # ====================================================
        # LATEST IMAGE
        # ====================================================

        image_box = tk.Frame(
            lower,
            bg="white",
            bd=1,
            relief="solid"
        )

        image_box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            image_box,
            text="LATEST MONITORING CAPTURE",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        self.latest_image_label = tk.Label(
            image_box,
            text="No monitoring image available",
            font=("Arial", 11, "bold"),
            bg="#F1F5F9",
            fg="#64748B"
        )

        self.latest_image_label.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        # ====================================================
        # ALERT BOX
        # ====================================================

        alert_box = tk.Frame(
            lower,
            bg="white",
            bd=1,
            relief="solid",
            width=300
        )

        alert_box.pack(
            side="right",
            fill="y"
        )

        alert_box.pack_propagate(False)

        tk.Label(
            alert_box,
            text="LATEST ALERT",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 15)
        )

        self.latest_alert_label = tk.Label(
            alert_box,
            text=self.latest_alert,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#64748B",
            wraplength=250,
            justify="left"
        )

        self.latest_alert_label.pack(
            anchor="w",
            padx=18
        )

        tk.Label(
            alert_box,
            text="LAST UPDATED",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#94A3B8"
        ).pack(
            anchor="w",
            padx=18,
            pady=(30, 5)
        )

        self.latest_time_label = tk.Label(
            alert_box,
            text="--",
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        )

        self.latest_time_label.pack(
            anchor="w",
            padx=18
        )

        # ====================================================
        # OVERALL STATUS
        # ====================================================

        self.overall_status_label = tk.Label(
            alert_box,
            text=f"STATUS : {self.worker_status}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#16A34A"
        )

        self.overall_status_label.pack(
            pady=35
        )

        # ====================================================
        # FOOTER
        # ====================================================

        tk.Label(
            self.content,
            text="Industrial AI-Based Anomaly Detection System",
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            side="bottom",
            pady=3
        )

        # ====================================================
        # REFRESH HOME DATA
        # ====================================================

        self.refresh_home()

    # ========================================================
    # READ LATEST DATA
    # ========================================================

    def read_latest_data(self):

        # Default values
        self.worker_status = "NO WORKER"
        self.machine_status = "NORMAL"
        self.alert_count = 0
        self.latest_alert = "No active alerts"
        self.latest_time = "--"

        # ----------------------------------------------------
        # STATUS JSON
        # ----------------------------------------------------

        if os.path.exists(STATUS_FILE):

            try:

                with open(
                    STATUS_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                worker = data.get(
                    "worker",
                    False
                )

                danger = data.get(
                    "danger",
                    False
                )

                fall = data.get(
                    "fall",
                    False
                )

                status = data.get(
                    "status",
                    "NO WORKER"
                )

                message = data.get(
                    "message",
                    "No active alerts"
                )

                self.latest_time = data.get(
                    "time",
                    "--"
                )

                # ------------------------------------------------
                # WORKER
                # ------------------------------------------------

                if worker:
                    self.worker_status = "DETECTED"
                else:
                    self.worker_status = "NOT DETECTED"

                # ------------------------------------------------
                # ALERT
                # ------------------------------------------------

                if fall:

                    self.latest_alert = "⚠ FALL DETECTED"
                    self.alert_count = 1

                elif danger:

                    self.latest_alert = "⚠ WORKER IN DANGER ZONE"
                    self.alert_count = 1

                elif worker:

                    self.latest_alert = "✓ WORKER DETECTED - SAFE"
                    self.alert_count = 0

                else:

                    self.latest_alert = message
                    self.alert_count = 0

                self.latest_status = status

            except Exception as e:

                self.latest_alert = (
                    "Unable to read monitoring status"
                )

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        return

    # ========================================================
    # LOAD LATEST IMAGE
    # ========================================================

    def load_latest_image(self):

        if not hasattr(
            self,
            "latest_image_label"
        ):
            return

        if not os.path.exists(
            LATEST_IMAGE
        ):

            self.latest_image_label.config(
                image="",
                text="No monitoring image available"
            )

            self.latest_image_label.image = None

            return

        try:

            image = Image.open(
                LATEST_IMAGE
            )

            # Get available size
            width = self.latest_image_label.winfo_width()
            height = self.latest_image_label.winfo_height()

            if width < 100:
                width = 600

            if height < 100:
                height = 350

            image.thumbnail(
                (
                    width - 10,
                    height - 10
                ),
                Image.Resampling.LANCZOS
            )

            self.latest_photo = ImageTk.PhotoImage(
                image
            )

            self.latest_image_label.config(
                image=self.latest_photo,
                text=""
            )

            self.latest_image_label.image = (
                self.latest_photo
            )

        except Exception:
            self.latest_image_label.config(
                image="",
                text="Unable to load latest image"
            )

    # ========================================================
    # REFRESH HOME
    # ========================================================

    def refresh_home(self):

        # Only refresh if HOME is currently displayed
        if self.page_title.cget(
            "text"
        ) != "HOME":
            return

        self.read_latest_data()

        # ----------------------------------------------------
        # UPDATE CARDS
        # ----------------------------------------------------

        if hasattr(
            self,
            "worker_card"
        ):

            if self.worker_status == "DETECTED":

                self.worker_card.config(
                    text="DETECTED",
                    fg="#16A34A"
                )

            else:

                self.worker_card.config(
                    text="NOT DETECTED",
                    fg="#64748B"
                )

        if hasattr(
            self,
            "alert_card"
        ):

            self.alert_card.config(
                text=str(
                    self.alert_count
                ),
                fg=(
                    "#DC2626"
                    if self.alert_count > 0
                    else "#64748B"
                )
            )

        # ----------------------------------------------------
        # ALERT MESSAGE
        # ----------------------------------------------------

        if hasattr(
            self,
            "latest_alert_label"
        ):

            if self.alert_count > 0:

                self.latest_alert_label.config(
                    text=self.latest_alert,
                    fg="#DC2626"
                )

            else:

                self.latest_alert_label.config(
                    text=self.latest_alert,
                    fg="#16A34A"
                )

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        if hasattr(
            self,
            "latest_time_label"
        ):

            self.latest_time_label.config(
                text=self.latest_time
            )

        # ----------------------------------------------------
        # OVERALL STATUS
        # ----------------------------------------------------

        if hasattr(
            self,
            "overall_status_label"
        ):

            if self.alert_count > 0:

                status_text = "STATUS : DANGER"
                status_color = "#DC2626"

            elif self.worker_status == "DETECTED":

                status_text = "STATUS : SAFE"
                status_color = "#16A34A"

            else:

                status_text = "STATUS : NO WORKER"
                status_color = "#F59E0B"

            self.overall_status_label.config(
                text=status_text,
                fg=status_color
            )

        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------


        self.load_latest_image()

        # ----------------------------------------------------
        # CONTINUE REFRESHING
        # ----------------------------------------------------

        self.root.after(
            1000,
            self.refresh_home
        )

    # ========================================================
    # STATUS CARD
    # ========================================================

    def status_card(
        self,
        parent,
        title,
        value,
        color
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            height=90
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 8, "bold"),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(14, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            bg="white",
            fg=color
        )

        value_label.pack(
            anchor="w",
            padx=15
        )

        return value_label

    # ========================================================
    # LIVE MONITORING
    # ========================================================

    def show_live_monitoring(self):

        self.page_title.config(
            text="LIVE MONITORING"
        )

        self.clear_content()

        self.create_back_button()

        try:

            # Because dashboard.py and live_monitoring.py
            # are both inside frontend/

            from live_monitoring import LiveMonitoring

            self.live_monitoring_page = LiveMonitoring(
                self.content
            )

        except Exception as e:

            self.show_error_page(
                "LIVE MONITORING",
                str(e)
            )

    # ========================================================
    # WORKER STATUS
    # ========================================================

    def show_worker_status(self):

        self.page_title.config(text="WORKER STATUS")
        self.clear_content()
        self.create_back_button()

        try:
            from worker_status import WorkerStatus
            WorkerStatus(self.content)

        except Exception as e:
            self.show_error_page(
                "WORKER STATUS",
                str(e)
            )


    # ========================================================
    # MACHINE HEALTH
    # ========================================================

    def show_machine_health(self):

        self.page_title.config(text="MACHINE HEALTH")
        self.clear_content()
        self.create_back_button()

        try:
            from machine_health import MachineHealth
            MachineHealth(self.content)

        except Exception as e:
            self.show_error_page(
                "MACHINE HEALTH",
                str(e)
            )


    # ========================================================
    # TEMPERATURE
    # ========================================================

    def show_temperature(self):

        self.page_title.config(text="TEMPERATURE")
        self.clear_content()
        self.create_back_button()

        try:
            from temperature import Temperature
            Temperature(self.content)

        except Exception as e:
            self.show_error_page(
                "TEMPERATURE",
                str(e)
            )


    # ========================================================
    # VIBRATION
    # ========================================================

    def show_vibration(self):

        self.page_title.config(text="VIBRATION")
        self.clear_content()
        self.create_back_button()

        try:
            from vibration import Vibration
            Vibration(self.content)

        except Exception as e:
            self.show_error_page(
                "VIBRATION",
                str(e)
            )


    # ========================================================
    # ALERTS
    # ========================================================

    def show_alerts(self):

        self.page_title.config(text="ALERTS")
        self.clear_content()
        self.create_back_button()

        try:
            from alerts import Alerts
            Alerts(self.content)

        except Exception as e:
            self.show_error_page(
                "ALERTS",
                str(e)
            )


    # ========================================================
    # INCIDENT LOGS
    # ========================================================

    def show_incident_logs(self):

        self.page_title.config(text="INCIDENT LOGS")
        self.clear_content()
        self.create_back_button()

        try:
            from incident_logs import IncidentLogs
            IncidentLogs(self.content)

        except Exception as e:
            self.show_error_page(
                "INCIDENT LOGS",
                str(e)
            )


    # ========================================================
    # REPORTS
    # ========================================================

    def show_reports(self):

        self.page_title.config(text="REPORTS")
        self.clear_content()
        self.create_back_button()

        try:
            from reports import Reports
            Reports(self.content)

        except Exception as e:
            self.show_error_page(
                "REPORTS",
                str(e)
            )


    # ========================================================
    # SETTINGS
    # ========================================================

    def show_settings(self):

        self.page_title.config(text="SETTINGS")
        self.clear_content()
        self.create_back_button()

        try:
            from settings import Settings
            Settings(self.content)

        except Exception as e:
            self.show_error_page(
                "SETTINGS",
                str(e)
            )


    # ========================================================
    # ABOUT
    # ========================================================

    def show_about(self):

        self.page_title.config(text="ABOUT")
        self.clear_content()
        self.create_back_button()

        try:
            from about import About
            About(self.content)

        except Exception as e:
            self.show_error_page(
                "ABOUT",
                str(e)
            )

    # ========================================================
    # PLACEHOLDER
    # ========================================================

    def placeholder_page(
        self,
        title,
        description
    ):

        tk.Label(
            self.content,
            text=title,
            font=("Arial", 22, "bold"),
            bg="#EEF2F7",
            fg="#172033"
        ).pack(
            pady=(100, 10)
        )

        tk.Label(
            self.content,
            text=description,
            font=("Arial", 10),
            bg="#EEF2F7",
            fg="#64748B"
        ).pack()

    # ========================================================
    # ERROR PAGE
    # ========================================================

    def show_error_page(
        self,
        title,
        error
    ):

        self.clear_content()

        self.create_back_button()

        tk.Label(
            self.content,
            text=title,
            font=("Arial", 22, "bold"),
            bg="#EEF2F7",
            fg="#172033"
        ).pack(
            pady=(100, 10)
        )

        tk.Label(
            self.content,
            text="Unable to load this module.",
            font=("Arial", 11, "bold"),
            bg="#EEF2F7",
            fg="#DC2626"
        ).pack(
            pady=5
        )

        tk.Label(
            self.content,
            text=str(error),
            font=("Consolas", 9),
            bg="#EEF2F7",
            fg="#64748B",
            wraplength=700
        ).pack(
            pady=10
        )

    # ========================================================
    # CLOCK
    # ========================================================

    def update_clock(self):

        current_time = datetime.now().strftime(
            "%d-%m-%Y   %I:%M:%S %p"
        )

        self.clock_label.config(
            text=current_time
        )

        self.root.after(
            1000,
            self.update_clock
        )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if not answer:
            return

        self.root.destroy()

        login_file = os.path.join(
            CURRENT_DIR,
            "login.py"
        )

        if os.path.exists(login_file):

            subprocess.Popen(
                [
                    sys.executable,
                    login_file
                ]
            )


# ============================================================
# RUN DASHBOARD
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = Dashboard(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        root.destroy
    )

    root.mainloop()