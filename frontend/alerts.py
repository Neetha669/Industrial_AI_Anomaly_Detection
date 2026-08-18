import tkinter as tk
from datetime import datetime
import os
import json


class Alerts:

    def __init__(self, parent):

        self.parent = parent

        # ==================================================
        # PATH TO latest_status.json
        # ==================================================

        CURRENT_DIR = os.path.dirname(
            os.path.abspath(__file__)
        )

        PROJECT_ROOT = os.path.dirname(
            CURRENT_DIR
        )

        DATA_DIR = os.path.join(
            PROJECT_ROOT,
            "data"
        )

        self.STATUS_FILE = os.path.join(
            DATA_DIR,
            "latest_status.json"
        )

        # ==================================================
        # ALERT STORAGE
        # ==================================================

        self.alerts = []

        # Prevent same alert from being added repeatedly
        self.last_event_key = None

        # Used to stop automatic refresh
        self.after_id = None

        # ==================================================
        # CREATE UI
        # ==================================================

        self.create_ui()

        # Start automatic monitoring
        self.monitor_status()

    # ==================================================
    # CREATE UI
    # ==================================================

    def create_ui(self):

        self.page = tk.Frame(
            self.parent,
            bg="#EEF2F7"
        )

        self.page.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # SUMMARY CARDS
        # ==================================================

        summary = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        summary.pack(
            fill="x",
            pady=(0, 15)
        )

        self.total_card = self.create_card(
            summary,
            "TOTAL ALERTS",
            "0",
            "#2563EB"
        )

        self.critical_card = self.create_card(
            summary,
            "CRITICAL",
            "0",
            "#DC2626"
        )

        self.warning_card = self.create_card(
            summary,
            "WARNING",
            "0",
            "#F59E0B"
        )

        self.status_card = self.create_card(
            summary,
            "SYSTEM STATUS",
            "SAFE",
            "#16A34A"
        )

        # ==================================================
        # MAIN CONTENT
        # ==================================================

        main = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # ALERT LIST
        # ==================================================

        alert_frame = tk.Frame(
            main,
            bg="white",
            bd=1,
            relief="solid"
        )

        alert_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        # Header

        header = tk.Frame(
            alert_frame,
            bg="white"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        tk.Label(
            header,
            text="SAFETY ALERTS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            side="left"
        )

        tk.Button(
            header,
            text="CLEAR ALERTS",
            font=("Arial", 9, "bold"),
            bg="#F1F5F9",
            fg="#475569",
            relief="flat",
            cursor="hand2",
            command=self.clear_alerts
        ).pack(
            side="right"
        )

        # ==================================================
        # ALERT LIST AREA
        # ==================================================

        list_container = tk.Frame(
            alert_frame,
            bg="#F8FAFC"
        )

        list_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        self.canvas = tk.Canvas(
            list_container,
            bg="#F8FAFC",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            list_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.alert_list = tk.Frame(
            self.canvas,
            bg="#F8FAFC"
        )

        self.alert_list.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.alert_list,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Empty message

        self.empty_label = tk.Label(
            self.alert_list,
            text="No safety alerts detected",
            font=("Arial", 11),
            bg="#F8FAFC",
            fg="#94A3B8"
        )

        self.empty_label.pack(
            pady=60
        )

        # ==================================================
        # RIGHT PANEL
        # ==================================================

        right = tk.Frame(
            main,
            bg="white",
            bd=1,
            relief="solid",
            width=350
        )

        right.pack(
            side="right",
            fill="y"
        )

        right.pack_propagate(False)

        tk.Label(
            right,
            text="ALERT CATEGORIES",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        self.category_row(
            right,
            "🔴",
            "CRITICAL EMERGENCY",
            "Immediate action required",
            "#DC2626"
        )

        self.category_row(
            right,
            "🟠",
            "HIGH RISK",
            "Multiple abnormal conditions",
            "#EA580C"
        )

        self.category_row(
            right,
            "🟡",
            "WARNING",
            "Abnormal condition detected",
            "#F59E0B"
        )

        self.category_row(
            right,
            "🔵",
            "INFORMATION",
            "System information",
            "#2563EB"
        )

        # ==================================================
        # DETECTION SOURCES
        # ==================================================

        tk.Frame(
            right,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            right,
            text="DETECTION SOURCES",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25
        )

        sources = (
            "• YOLOv8 Worker Detection\n"
            "• Danger Zone Detection\n"
            "• MediaPipe Pose Detection\n"
            "• Fall Detection\n"
            "• Temperature Anomaly\n"
            "• Vibration Anomaly\n"
            "• Decision Logic"
        )

        tk.Label(
            right,
            text=sources,
            font=("Arial", 9),
            bg="white",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=12
        )

        # ==================================================
        # FOOTER
        # ==================================================

        tk.Label(
            self.page,
            text=(
                "Alerts are generated automatically "
                "from the AI monitoring system."
            ),
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            pady=8
        )

    # ==================================================
    # SUMMARY CARD
    # ==================================================

    def create_card(
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
            height=100
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
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            bg="white",
            fg=color
        )

        label.pack(
            anchor="w",
            padx=15
        )

        return label

    # ==================================================
    # CATEGORY ROW
    # ==================================================

    def category_row(
        self,
        parent,
        icon,
        title,
        description,
        color
    ):

        frame = tk.Frame(
            parent,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            frame,
            text=icon,
            font=("Arial", 15),
            bg="#F8FAFC"
        ).pack(
            side="left",
            padx=12,
            pady=10
        )

        text_frame = tk.Frame(
            frame,
            bg="#F8FAFC"
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg=color
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text=description,
            font=("Arial", 8),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            anchor="w"
        )

    # ==================================================
    # READ latest_status.json
    # ==================================================

    def read_status(self):

        if not os.path.exists(
            self.STATUS_FILE
        ):
            return None

        try:

            with open(
                self.STATUS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception as e:

            print(
                "Alerts JSON error:",
                e
            )

            return None

    # ==================================================
    # AUTOMATIC MONITORING
    # ==================================================

    def monitor_status(self):

        data = self.read_status()

        if data:

            self.process_status(data)

        # Check JSON every 1 second

        try:

            if self.page.winfo_exists():

                self.after_id = self.page.after(
                    1000,
                    self.monitor_status
                )

        except tk.TclError:

            pass

    # ==================================================
    # PROCESS STATUS
    # ==================================================

    def process_status(
        self,
        data
    ):

        worker = data.get(
            "worker",
            False
        )

        danger = data.get(
            "danger",
            False
        )

        hand_danger = data.get(
            "hand_danger",
            False
        )

        body_danger = data.get(
            "body_danger",
            False
        )

        fall = data.get(
            "fall",
            False
        )

        anomaly = data.get(
            "anomaly",
            False
        )

        anomaly_status = data.get(
            "anomaly_status",
            ""
        )

        risk_level = data.get(
            "risk_level",
            "LOW"
        )

        message = data.get(
            "message",
            ""
        )

        timestamp = data.get(
            "time",
            datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )
        )

        # ==================================================
        # DETERMINE CURRENT EVENT
        # ==================================================

        alert_type = None
        alert_message = None
        source = None

        # --------------------------------------------------
        # 1. FALL = CRITICAL
        # --------------------------------------------------

        if fall:

            alert_type = "CRITICAL"

            alert_message = (
                "Worker fall detected"
            )

            source = "Fall Detection"

        # --------------------------------------------------
        # 2. BODY DANGER = CRITICAL
        # --------------------------------------------------

        elif body_danger:

            alert_type = "CRITICAL"

            alert_message = (
                "Worker entered danger zone"
            )

            source = "YOLOv8 + Danger Zone Detection"

        # --------------------------------------------------
        # 3. HAND DANGER = HIGH RISK
        # --------------------------------------------------

        elif hand_danger:

            alert_type = "HIGH RISK"

            alert_message = (
                "Worker hand entered danger zone"
            )

            source = (
                "MediaPipe Pose + Danger Zone"
            )

        # --------------------------------------------------
        # 4. GENERAL DANGER = HIGH RISK
        # --------------------------------------------------

        elif danger:

            alert_type = "HIGH RISK"

            alert_message = (
                "Worker detected inside danger zone"
            )

            source = "YOLOv8 Danger Zone Detection"

        # --------------------------------------------------
        # 5. ANOMALY = WARNING
        # --------------------------------------------------

        elif anomaly:

            alert_type = "WARNING"

            if anomaly_status:

                alert_message = (
                    f"Abnormal condition detected: "
                    f"{anomaly_status}"
                )

            else:

                alert_message = (
                    "Industrial anomaly detected"
                )

            source = "Anomaly Detection"

        # --------------------------------------------------
        # NO ALERT
        # --------------------------------------------------

        else:

            return

        # ==================================================
        # CREATE UNIQUE EVENT KEY
        # ==================================================

        event_key = (
            f"{alert_type}|"
            f"{alert_message}|"
            f"{timestamp}"
        )

        # ==================================================
        # PREVENT DUPLICATE ALERTS
        # ==================================================

        if event_key == self.last_event_key:

            return

        self.last_event_key = event_key

        # ==================================================
        # ADD ALERT
        # ==================================================

        self.add_alert(
            alert_type,
            alert_message,
            source,
            timestamp
        )

        print(
            "ALERT:",
            alert_type,
            alert_message
        )

    # ==================================================
    # ADD ALERT
    # ==================================================

    def add_alert(
        self,
        alert_type,
        message,
        source="System",
        timestamp=None
    ):

        if timestamp is None:

            timestamp = datetime.now().strftime(
                "%H:%M:%S"
            )

        alert = {

            "type": alert_type,

            "message": message,

            "source": source,

            "time": timestamp
        }

        self.alerts.insert(
            0,
            alert
        )

        # Keep last 50 alerts

        self.alerts = self.alerts[:50]

        self.refresh_alerts()

    # ==================================================
    # REFRESH ALERTS
    # ==================================================

    def refresh_alerts(self):

        # Remove existing widgets

        for widget in self.alert_list.winfo_children():

            widget.destroy()

        # ==================================================
        # NO ALERTS
        # ==================================================

        if not self.alerts:

            tk.Label(
                self.alert_list,
                text="No safety alerts detected",
                font=("Arial", 11),
                bg="#F8FAFC",
                fg="#94A3B8"
            ).pack(
                pady=60
            )

            self.update_summary()

            return

        # ==================================================
        # DISPLAY ALERTS
        # ==================================================

        for alert in self.alerts:

            self.create_alert_item(
                alert
            )

        self.update_summary()

    # ==================================================
    # CREATE ALERT ITEM
    # ==================================================

    def create_alert_item(
        self,
        alert
    ):

        alert_type = alert["type"]

        if alert_type == "CRITICAL":

            color = "#DC2626"

        elif alert_type == "HIGH RISK":

            color = "#EA580C"

        elif alert_type == "WARNING":

            color = "#F59E0B"

        else:

            color = "#2563EB"

        item = tk.Frame(
            self.alert_list,
            bg="white",
            bd=1,
            relief="solid"
        )

        item.pack(
            fill="x",
            padx=10,
            pady=5
        )

        # ==================================================
        # COLOR INDICATOR
        # ==================================================

        tk.Frame(
            item,
            bg=color,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        content = tk.Frame(
            item,
            bg="white"
        )

        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=12
        )

        # ==================================================
        # TOP ROW
        # ==================================================

        top = tk.Frame(
            content,
            bg="white"
        )

        top.pack(
            fill="x"
        )

        tk.Label(
            top,
            text=alert_type,
            font=("Arial", 9, "bold"),
            bg="white",
            fg=color
        ).pack(
            side="left"
        )

        tk.Label(
            top,
            text=alert["time"],
            font=("Arial", 8),
            bg="white",
            fg="#94A3B8"
        ).pack(
            side="right"
        )

        # ==================================================
        # MESSAGE
        # ==================================================

        tk.Label(
            content,
            text=alert["message"],
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#172033",
            anchor="w",
            wraplength=600
        ).pack(
            fill="x",
            pady=(5, 2)
        )

        # ==================================================
        # SOURCE
        # ==================================================

        tk.Label(
            content,
            text=f"Source: {alert['source']}",
            font=("Arial", 8),
            bg="white",
            fg="#64748B",
            anchor="w"
        ).pack(
            fill="x"
        )

    # ==================================================
    # UPDATE SUMMARY
    # ==================================================

    def update_summary(self):

        total = len(
            self.alerts
        )

        critical = sum(
            1
            for a in self.alerts
            if a["type"] == "CRITICAL"
        )

        warning = sum(
            1
            for a in self.alerts
            if a["type"] in [
                "WARNING",
                "HIGH RISK"
            ]
        )

        self.total_card.config(
            text=str(total)
        )

        self.critical_card.config(
            text=str(critical)
        )

        self.warning_card.config(
            text=str(warning)
        )

        # ==================================================
        # SYSTEM STATUS
        # ==================================================

        if critical > 0:

            self.status_card.config(
                text="CRITICAL",
                fg="#DC2626"
            )

        elif warning > 0:

            self.status_card.config(
                text="WARNING",
                fg="#F59E0B"
            )

        else:

            self.status_card.config(
                text="SAFE",
                fg="#16A34A"
            )

    # ==================================================
    # CLEAR ALERTS
    # ==================================================

    def clear_alerts(self):

        self.alerts.clear()

        self.last_event_key = None

        self.refresh_alerts()

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        try:

            if self.after_id is not None:

                self.page.after_cancel(
                    self.after_id
                )

        except Exception:

            pass

        try:

            self.page.destroy()

        except Exception:

            pass