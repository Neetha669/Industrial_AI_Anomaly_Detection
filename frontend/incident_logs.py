import tkinter as tk
from datetime import datetime


class IncidentLogs:

    def __init__(self, parent):

        self.parent = parent
        self.logs = []

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

        # ==================================================
        # LOG TABLE
        # ==================================================

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

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

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

        # ==================================================
        # TABLE
        # ==================================================

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

        # Canvas for scrolling

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

        # Table headings

        self.create_table_header()

        # Empty message

        self.empty_label = tk.Label(
            self.table,
            text="No incidents recorded",
            font=("Arial", 10),
            bg="#F8FAFC",
            fg="#94A3B8"
        )

        self.empty_label.pack(
            pady=60
        )

        # ==================================================
        # FOOTER
        # ==================================================

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
    # TABLE HEADER
    # ==================================================

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

    # ==================================================
    # ADD INCIDENT
    # ==================================================

    def add_incident(
        self,
        incident_type,
        description,
        source="System",
        status="OPEN"
    ):

        now = datetime.now()

        incident = {
            "date": now.strftime("%d-%m-%Y"),
            "time": now.strftime("%H:%M:%S"),
            "type": incident_type,
            "description": description,
            "source": source,
            "status": status
        }

        self.logs.insert(
            0,
            incident
        )

        self.refresh_logs()

    # ==================================================
    # REFRESH LOGS
    # ==================================================

    def refresh_logs(self):

        for widget in self.table.winfo_children():

            widget.destroy()

        self.create_table_header()

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

        for incident in self.logs:

            self.create_log_row(
                incident
            )

        self.update_summary()

    # ==================================================
    # CREATE LOG ROW
    # ==================================================

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

        if incident["type"] == "FALL":

            color = "#DC2626"

        elif incident["type"] == "DANGER ZONE":

            color = "#EA580C"

        elif incident["type"] in [
            "TEMPERATURE",
            "VIBRATION"
        ]:

            color = "#F59E0B"

        else:

            color = "#2563EB"

        values = [
            incident["date"],
            incident["time"],
            incident["type"],
            incident["description"],
            incident["source"],
            incident["status"]
        ]

        widths = [
            14,
            10,
            20,
            40,
            25,
            15
        ]

        for index, value in enumerate(values):

            fg = color if index == 2 else "#475569"

            tk.Label(
                row,
                text=value,
                font=(
                    "Arial",
                    8,
                    "bold" if index == 2 else "normal"
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

    # ==================================================
    # UPDATE SUMMARY
    # ==================================================

    def update_summary(self):

        total = len(self.logs)

        fall = sum(
            1 for log in self.logs
            if log["type"] == "FALL"
        )

        danger = sum(
            1 for log in self.logs
            if log["type"] == "DANGER ZONE"
        )

        sensor = sum(
            1 for log in self.logs
            if log["type"] in [
                "TEMPERATURE",
                "VIBRATION"
            ]
        )

        self.total_card.config(
            text=str(total)
        )

        self.fall_card.config(
            text=str(fall)
        )

        self.danger_card.config(
            text=str(danger)
        )

        self.sensor_card.config(
            text=str(sensor)
        )

    # ==================================================
    # CLEAR LOGS
    # ==================================================

    def clear_logs(self):

        self.logs.clear()

        self.refresh_logs()

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()