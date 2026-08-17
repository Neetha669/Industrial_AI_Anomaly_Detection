import tkinter as tk
from datetime import datetime


class Reports:

    def __init__(self, parent):

        self.parent = parent

        # Demo statistics for now.
        # Later these will come from the actual incident database/logs.
        self.total_incidents = 0
        self.critical_incidents = 0
        self.fall_incidents = 0
        self.danger_incidents = 0
        self.sensor_incidents = 0

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
        # TOP SUMMARY
        # ==================================================

        summary = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        summary.pack(
            fill="x",
            pady=(0, 15)
        )

        self.create_card(
            summary,
            "TOTAL INCIDENTS",
            "0",
            "#2563EB"
        )

        self.create_card(
            summary,
            "CRITICAL EVENTS",
            "0",
            "#DC2626"
        )

        self.create_card(
            summary,
            "FALL EVENTS",
            "0",
            "#EA580C"
        )

        self.create_card(
            summary,
            "SENSOR EVENTS",
            "0",
            "#F59E0B"
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
        # REPORT GENERATOR
        # ==================================================

        report_frame = tk.Frame(
            main,
            bg="white",
            bd=1,
            relief="solid"
        )

        report_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            report_frame,
            text="SAFETY REPORT",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            report_frame,
            text="Generate a summary of system safety events.",
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ==================================================
        # DATE RANGE
        # ==================================================

        date_frame = tk.Frame(
            report_frame,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        date_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        tk.Label(
            date_frame,
            text="REPORT PERIOD",
            font=("Arial", 10, "bold"),
            bg="#F8FAFC",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        dates = tk.Frame(
            date_frame,
            bg="#F8FAFC"
        )

        dates.pack(
            fill="x",
            padx=15,
            pady=(0, 12)
        )

        tk.Label(
            dates,
            text="From:",
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            side="left"
        )

        self.from_date = tk.Entry(
            dates,
            font=("Arial", 9),
            width=15,
            relief="solid",
            bd=1
        )

        self.from_date.pack(
            side="left",
            padx=(5, 20)
        )

        tk.Label(
            dates,
            text="To:",
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            side="left"
        )

        self.to_date = tk.Entry(
            dates,
            font=("Arial", 9),
            width=15,
            relief="solid",
            bd=1
        )

        self.to_date.pack(
            side="left",
            padx=5
        )

        today = datetime.now().strftime("%d-%m-%Y")

        self.from_date.insert(
            0,
            today
        )

        self.to_date.insert(
            0,
            today
        )

        # ==================================================
        # REPORT PREVIEW
        # ==================================================

        tk.Label(
            report_frame,
            text="REPORT PREVIEW",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 8)
        )

        preview_container = tk.Frame(
            report_frame,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        preview_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )

        self.preview = tk.Text(
            preview_container,
            font=("Consolas", 9),
            bg="#F8FAFC",
            fg="#334155",
            relief="flat",
            wrap="word"
        )

        self.preview.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.generate_preview()

        # ==================================================
        # BUTTONS
        # ==================================================

        button_frame = tk.Frame(
            report_frame,
            bg="white"
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        tk.Button(
            button_frame,
            text="GENERATE REPORT",
            font=("Arial", 9, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9,
            command=self.generate_preview
        ).pack(
            side="left"
        )

        tk.Button(
            button_frame,
            text="SAVE REPORT",
            font=("Arial", 9, "bold"),
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9,
            command=self.save_report
        ).pack(
            side="left",
            padx=10
        )

        # ==================================================
        # RIGHT SIDE
        # ==================================================

        right = tk.Frame(
            main,
            bg="white",
            bd=1,
            relief="solid",
            width=330
        )

        right.pack(
            side="right",
            fill="y"
        )

        right.pack_propagate(False)

        tk.Label(
            right,
            text="REPORT INFORMATION",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        self.info_box(
            right,
            "INCIDENT SUMMARY",
            "Total number of safety incidents\n"
            "recorded during the selected period.",
            "#2563EB"
        )

        self.info_box(
            right,
            "CRITICAL EVENTS",
            "High-priority incidents requiring\n"
            "immediate attention.",
            "#DC2626"
        )

        self.info_box(
            right,
            "SENSOR EVENTS",
            "Temperature and vibration anomalies\n"
            "detected by Isolation Forest.",
            "#F59E0B"
        )

        self.info_box(
            right,
            "AI DETECTION",
            "Worker detection, danger-zone\n"
            "monitoring and fall detection.",
            "#16A34A"
        )

        # ==================================================
        # FOOTER
        # ==================================================

        tk.Label(
            self.page,
            text=(
                "Reports are generated from incidents detected "
                "by the integrated monitoring system."
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
    # INFORMATION BOX
    # ==================================================

    def info_box(
        self,
        parent,
        title,
        description,
        color
    ):

        box = tk.Frame(
            parent,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        box.pack(
            fill="x",
            padx=20,
            pady=6
        )

        tk.Label(
            box,
            text=title,
            font=("Arial", 10, "bold"),
            bg="#F8FAFC",
            fg=color
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        tk.Label(
            box,
            text=description,
            font=("Arial", 8),
            bg="#F8FAFC",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

    # ==================================================
    # GENERATE PREVIEW
    # ==================================================

    def generate_preview(self):

        report_date = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        from_date = self.from_date.get()
        to_date = self.to_date.get()

        report = f"""
========================================================
        INDUSTRIAL AI SAFETY MONITORING SYSTEM
                  SAFETY REPORT
========================================================

Report Generated : {report_date}

Report Period
From             : {from_date}
To               : {to_date}

--------------------------------------------------------
INCIDENT SUMMARY
--------------------------------------------------------

Total Incidents        : {self.total_incidents}
Critical Events        : {self.critical_incidents}
Fall Incidents         : {self.fall_incidents}
Danger Zone Incidents  : {self.danger_incidents}
Sensor Alerts          : {self.sensor_incidents}

--------------------------------------------------------
MONITORING MODULES
--------------------------------------------------------

Worker Detection       : YOLOv8n
Pose Detection         : MediaPipe
Fall Detection         : Pose Analysis
Temperature Detection  : Isolation Forest
Vibration Detection    : Isolation Forest
Decision Module        : Rule-Based Logic

--------------------------------------------------------
SYSTEM STATUS
--------------------------------------------------------

Worker Monitoring      : ACTIVE
Danger Zone Monitoring : ACTIVE
Fall Detection         : ACTIVE
Temperature Monitoring : READY
Vibration Monitoring   : READY

--------------------------------------------------------
END OF REPORT
--------------------------------------------------------
"""

        self.preview.delete(
            "1.0",
            tk.END
        )

        self.preview.insert(
            tk.END,
            report
        )

    # ==================================================
    # UPDATE REPORT DATA
    # ==================================================

    def update_statistics(
        self,
        total=0,
        critical=0,
        falls=0,
        danger=0,
        sensor=0
    ):

        self.total_incidents = total
        self.critical_incidents = critical
        self.fall_incidents = falls
        self.danger_incidents = danger
        self.sensor_incidents = sensor

        self.generate_preview()

    # ==================================================
    # SAVE REPORT
    # ==================================================

    def save_report(self):

        filename = (
            "safety_report_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".txt"
        )

        content = self.preview.get(
            "1.0",
            tk.END
        )

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

            self.show_message(
                "Report saved successfully:\n\n"
                + filename
            )

        except Exception as error:

            self.show_message(
                "Unable to save report:\n\n"
                + str(error)
            )

    # ==================================================
    # MESSAGE
    # ==================================================

    def show_message(
        self,
        message
    ):

        popup = tk.Toplevel(
            self.page
        )

        popup.title(
            "Report"
        )

        popup.geometry(
            "400x180"
        )

        popup.configure(
            bg="white"
        )

        tk.Label(
            popup,
            text=message,
            font=("Arial", 10),
            bg="white",
            fg="#172033",
            justify="center"
        ).pack(
            expand=True
        )

        tk.Button(
            popup,
            text="OK",
            command=popup.destroy,
            bg="#2563EB",
            fg="white",
            relief="flat",
            padx=20,
            pady=7
        ).pack(
            pady=15
        )

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()