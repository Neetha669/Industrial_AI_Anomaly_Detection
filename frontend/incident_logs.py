import tkinter as tk
import os
import sys


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )


# ============================================================
# IMPORT INCIDENT MANAGER
# ============================================================

try:

    from incident_manager import IncidentManager

except ImportError:

    IncidentManager = None


# ============================================================
# INCIDENT LOGS
# ============================================================

class IncidentLogs:

    def __init__(self, parent):

        self.parent = parent

        # ----------------------------------------------------
        # USE CENTRAL INCIDENT MANAGER
        # ----------------------------------------------------

        if IncidentManager is not None:

            self.manager = IncidentManager()

        else:

            self.manager = None

        self.logs = []

        self.create_ui()

        # Load existing incidents
        self.load_incidents()

        # Keep checking for new incidents
        self.auto_refresh()


    # ========================================================
    # CREATE UI
    # ========================================================

    def create_ui(self):

        self.page = tk.Frame(
            self.parent,
            bg="#EEF2F7"
        )

        self.page.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # SUMMARY CARDS
        # ====================================================

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
            "TOTAL INCIDENTS",
            "0",
            "#2563EB"
        )

        self.fall_card = self.create_card(
            summary,
            "FALL INCIDENTS",
            "0",
            "#DC2626"
        )

        self.danger_card = self.create_card(
            summary,
            "DANGER ZONE",
            "0",
            "#EA580C"
        )

        self.sensor_card = self.create_card(
            summary,
            "SENSOR ALERTS",
            "0",
            "#F59E0B"
        )

        # ====================================================
        # LOG TABLE
        # ====================================================

        log_frame = tk.Frame(
            self.page,
            bg="white",
            bd=1,
            relief="solid"
        )

        log_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            log_frame,
            bg="white"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        tk.Label(
            header,
            text="INCIDENT HISTORY",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            side="left"
        )

        # ----------------------------------------------------
        # REFRESH BUTTON
        # ----------------------------------------------------

        tk.Button(
            header,
            text="REFRESH",
            font=("Arial", 9, "bold"),
            bg="#E8F0FE",
            fg="#2563EB",
            relief="flat",
            cursor="hand2",
            command=self.load_incidents
        ).pack(
            side="right",
            padx=5
        )

        # ----------------------------------------------------
        # CLEAR BUTTON
        # ----------------------------------------------------

        tk.Button(
            header,
            text="CLEAR LOGS",
            font=("Arial", 9, "bold"),
            bg="#F1F5F9",
            fg="#475569",
            relief="flat",
            cursor="hand2",
            command=self.clear_logs
        ).pack(
            side="right"
        )

        # ====================================================
        # TABLE CONTAINER
        # ====================================================

        table_container = tk.Frame(
            log_frame,
            bg="#F8FAFC"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 20)
        )

        # ====================================================
        # CANVAS
        # ====================================================

        self.canvas = tk.Canvas(
            table_container,
            bg="#F8FAFC",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.table = tk.Frame(
            self.canvas,
            bg="#F8FAFC"
        )

        self.table.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.table,
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

        # ====================================================
        # FOOTER
        # ====================================================

        tk.Label(
            self.page,
            text=(
                "Incident logs contain safety events detected "
                "by the AI and sensor monitoring system."
            ),
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            pady=8
        )


    # ========================================================
    # SUMMARY CARD
    # ========================================================

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


    # ========================================================
    # LOAD INCIDENTS FROM INCIDENT MANAGER
    # ========================================================

    def load_incidents(self):

        if self.manager is None:

            self.logs = []

            self.refresh_logs()

            return

        try:

            self.logs = self.manager.get_logs()

        except Exception as error:

            print(
                "Unable to load incidents:",
                error
            )

            self.logs = []

        self.refresh_logs()


    # ========================================================
    # TABLE HEADER
    # ========================================================

    def create_table_header(self):

        header = tk.Frame(
            self.table,
            bg="#E2E8F0"
        )

        header.pack(
            fill="x"
        )

        columns = [
            ("DATE", 14),
            ("TIME", 10),
            ("TYPE", 20),
            ("DESCRIPTION", 40),
            ("SOURCE", 25),
            ("STATUS", 15)
        ]

        for text, width in columns:

            tk.Label(
                header,
                text=text,
                font=("Arial", 8, "bold"),
                bg="#E2E8F0",
                fg="#475569",
                width=width,
                anchor="w"
            ).pack(
                side="left",
                padx=5,
                pady=10
            )


    # ========================================================
    # REFRESH LOGS
    # ========================================================

    def refresh_logs(self):

        # Remove existing table rows

        for widget in self.table.winfo_children():

            widget.destroy()

        # Recreate header

        self.create_table_header()

        # ----------------------------------------------------
        # NO INCIDENTS
        # ----------------------------------------------------

        if not self.logs:

            tk.Label(
                self.table,
                text="No incidents recorded",
                font=("Arial", 10),
                bg="#F8FAFC",
                fg="#94A3B8"
            ).pack(
                pady=60
            )

            self.update_summary()

            return

        # ----------------------------------------------------
        # DISPLAY INCIDENTS
        # ----------------------------------------------------

        for incident in self.logs:

            self.create_log_row(
                incident
            )

        self.update_summary()


    # ========================================================
    # CREATE LOG ROW
    # ========================================================

    def create_log_row(
        self,
        incident
    ):

        row = tk.Frame(
            self.table,
            bg="white",
            bd=1,
            relief="solid"
        )

        row.pack(
            fill="x"
        )

        incident_type = incident.get(
            "type",
            "UNKNOWN"
        )

        # ----------------------------------------------------
        # TYPE COLOR
        # ----------------------------------------------------

        if incident_type == "FALL":

            color = "#DC2626"

        elif incident_type == "DANGER ZONE":

            color = "#EA580C"

        elif incident_type in [
            "TEMPERATURE",
            "VIBRATION"
        ]:

            color = "#F59E0B"

        else:

            color = "#2563EB"

        # ----------------------------------------------------
        # VALUES
        # ----------------------------------------------------

        values = [

            incident.get(
                "date",
                "--"
            ),

            incident.get(
                "time",
                "--"
            ),

            incident_type,

            incident.get(
                "description",
                ""
            ),

            incident.get(
                "source",
                "System"
            ),

            incident.get(
                "status",
                "OPEN"
            )
        ]

        widths = [
            14,
            10,
            20,
            40,
            25,
            15
        ]

        # ----------------------------------------------------
        # CREATE COLUMNS
        # ----------------------------------------------------

        for index, value in enumerate(values):

            fg = (
                color
                if index == 2
                else "#475569"
            )

            tk.Label(
                row,
                text=value,
                font=(
                    "Arial",
                    8,
                    "bold"
                    if index == 2
                    else "normal"
                ),
                bg="white",
                fg=fg,
                width=widths[index],
                anchor="w"
            ).pack(
                side="left",
                padx=5,
                pady=10
            )


    # ========================================================
    # UPDATE SUMMARY
    # ========================================================

    def update_summary(self):

        if self.manager is None:

            total = 0
            falls = 0
            danger = 0
            sensor = 0

        else:

            try:

                statistics = (
                    self.manager.get_statistics()
                )

                total = statistics.get(
                    "total",
                    0
                )

                falls = statistics.get(
                    "falls",
                    0
                )

                danger = statistics.get(
                    "danger",
                    0
                )

                sensor = statistics.get(
                    "sensor",
                    0
                )

            except Exception:

                total = 0
                falls = 0
                danger = 0
                sensor = 0

        # ----------------------------------------------------
        # UPDATE CARDS
        # ----------------------------------------------------

        self.total_card.config(
            text=str(total)
        )

        self.fall_card.config(
            text=str(falls)
        )

        self.danger_card.config(
            text=str(danger)
        )

        self.sensor_card.config(
            text=str(sensor)
        )


    # ========================================================
    # CLEAR LOGS
    # ========================================================

    def clear_logs(self):

        if self.manager is None:

            return

        self.manager.clear_logs()

        self.load_incidents()


    # ========================================================
    # AUTOMATIC REFRESH
    # ========================================================

    def auto_refresh(self):

        try:

            if self.page.winfo_exists():

                # Read latest_status.json
                # and create new incidents if required
                if self.manager is not None:
                    self.manager.check_for_incidents()

                # Load incident_logs.json
                self.load_incidents()

                # Check again after 2 seconds
                self.page.after(
                    2000,
                    self.auto_refresh
                )

        except Exception as error:

            print(
                "Incident auto refresh error:",
                error
            )
    # ========================================================
    # CLEANUP
    # ========================================================

    def destroy(self):

        try:

            self.page.destroy()

        except Exception:

            pass