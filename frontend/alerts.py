import tkinter as tk
from datetime import datetime


class Alerts:

    def __init__(self, parent):

        self.parent = parent

        self.alerts = []

        self.create_ui()

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

        # --------------------------------------------------
        # ALERT LIST AREA
        # --------------------------------------------------

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

        # Categories

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
                "Alerts are generated by the integrated "
                "AI and sensor monitoring modules."
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
    # ADD ALERT
    # ==================================================

    def add_alert(
        self,
        alert_type,
        message,
        source="System"
    ):

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

        self.refresh_alerts()

    # ==================================================
    # REFRESH ALERTS
    # ==================================================

    def refresh_alerts(self):

        # Remove existing widgets

        for widget in self.alert_list.winfo_children():

            widget.destroy()

        # No alerts

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

        # Display alerts

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

        # Color indicator

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

        tk.Label(
            content,
            text=alert["message"],
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#172033",
            anchor="w"
        ).pack(
            fill="x",
            pady=(5, 2)
        )

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

        total = len(self.alerts)

        critical = sum(
            1 for a in self.alerts
            if a["type"] == "CRITICAL"
        )

        warning = sum(
            1 for a in self.alerts
            if a["type"] in ["WARNING", "HIGH RISK"]
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

        self.refresh_alerts()

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()