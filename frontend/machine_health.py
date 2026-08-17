import tkinter as tk


class MachineHealth:

    def __init__(self, parent):

        self.parent = parent

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
        # TOP SUMMARY CARDS
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
            "MACHINE STATUS",
            "HEALTHY",
            "#16A34A"
        )

        self.create_card(
            summary,
            "TEMPERATURE",
            "NORMAL",
            "#16A34A"
        )

        self.create_card(
            summary,
            "VIBRATION",
            "NORMAL",
            "#16A34A"
        )

        self.create_card(
            summary,
            "ANOMALY",
            "NOT DETECTED",
            "#64748B"
        )

        # ==================================================
        # MAIN AREA
        # ==================================================

        main_area = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        main_area.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # MACHINE OVERVIEW
        # ==================================================

        overview = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid"
        )

        overview.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            overview,
            text="MACHINE OVERVIEW",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        # Machine icon

        tk.Label(
            overview,
            text="⚙",
            font=("Segoe UI Symbol", 65),
            bg="white",
            fg="#2563EB"
        ).pack(
            pady=5
        )

        tk.Label(
            overview,
            text="MACHINE 01",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            pady=5
        )

        tk.Label(
            overview,
            text="Industrial Machine Monitoring",
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack(
            pady=(0, 20)
        )

        # Machine information

        self.info_row(
            overview,
            "Machine Status",
            "RUNNING",
            "#16A34A"
        )

        self.info_row(
            overview,
            "Health Condition",
            "HEALTHY",
            "#16A34A"
        )

        self.info_row(
            overview,
            "Anomaly Status",
            "NORMAL",
            "#16A34A"
        )

        self.info_row(
            overview,
            "Monitoring",
            "ACTIVE",
            "#2563EB"
        )

        # ==================================================
        # SENSOR / AI ANALYSIS
        # ==================================================

        analysis = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid",
            width=380
        )

        analysis.pack(
            side="right",
            fill="y"
        )

        analysis.pack_propagate(False)

        tk.Label(
            analysis,
            text="HEALTH ANALYSIS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        # Temperature

        self.sensor_box(
            analysis,
            "TEMPERATURE",
            "32.6 °C",
            "NORMAL",
            "#16A34A"
        )

        # Vibration

        self.sensor_box(
            analysis,
            "VIBRATION",
            "2.3 mm/s",
            "NORMAL",
            "#16A34A"
        )

        # Isolation Forest

        self.sensor_box(
            analysis,
            "ISOLATION FOREST",
            "ACTIVE",
            "MONITORING",
            "#2563EB"
        )

        # ==================================================
        # ALGORITHM INFORMATION
        # ==================================================

        tk.Frame(
            analysis,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            analysis,
            text="ANOMALY DETECTION",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25
        )

        algorithm_text = (
            "Isolation Forest\n\n"
            "• Temperature monitoring\n"
            "• Vibration monitoring\n"
            "• Unlabelled sensor data\n"
            "• Normal / anomaly classification\n"
            "• Real-time machine health analysis"
        )

        tk.Label(
            analysis,
            text=algorithm_text,
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
                "Machine health is determined using sensor "
                "data and anomaly detection algorithms."
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

        tk.Label(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            bg="white",
            fg=color
        ).pack(
            anchor="w",
            padx=15
        )

    # ==================================================
    # INFORMATION ROW
    # ==================================================

    def info_row(
        self,
        parent,
        label,
        value,
        color
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=30,
            pady=8
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            font=("Arial", 9, "bold"),
            bg="white",
            fg=color
        ).pack(
            side="right"
        )

    # ==================================================
    # SENSOR BOX
    # ==================================================

    def sensor_box(
        self,
        parent,
        sensor,
        value,
        status,
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
            text=sensor,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 3)
        )

        tk.Label(
            box,
            text=value,
            font=("Arial", 16, "bold"),
            bg="#F8FAFC",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=15
        )

        tk.Label(
            box,
            text=status,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg=color
        ).pack(
            anchor="w",
            padx=15,
            pady=(2, 12)
        )

    # ==================================================
    # UPDATE MACHINE HEALTH
    # ==================================================

    def update_status(
        self,
        temperature=32.6,
        vibration=2.3,
        anomaly=False
    ):

        # This method will later receive the
        # real Isolation Forest prediction.

        pass

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()