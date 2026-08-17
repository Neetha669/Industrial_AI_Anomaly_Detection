import tkinter as tk


class Temperature:

    def __init__(self, parent):

        self.parent = parent
        self.temperature = 32.6
        self.status = "NORMAL"

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

        self.value_card = self.create_card(
            summary,
            "CURRENT TEMPERATURE",
            "32.6 °C",
            "#16A34A"
        )

        self.status_card = self.create_card(
            summary,
            "TEMPERATURE STATUS",
            "NORMAL",
            "#16A34A"
        )

        self.threshold_card = self.create_card(
            summary,
            "ANOMALY THRESHOLD",
            "50 °C",
            "#2563EB"
        )

        self.sensor_card = self.create_card(
            summary,
            "SENSOR",
            "NOT CONNECTED",
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
        # TEMPERATURE MONITORING
        # ==================================================

        monitor_frame = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid"
        )

        monitor_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            monitor_frame,
            text="TEMPERATURE MONITORING",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        # Temperature icon

        tk.Label(
            monitor_frame,
            text="🌡",
            font=("Segoe UI Emoji", 70),
            bg="white"
        ).pack(
            pady=5
        )

        self.temperature_label = tk.Label(
            monitor_frame,
            text="32.6 °C",
            font=("Arial", 34, "bold"),
            bg="white",
            fg="#172033"
        )

        self.temperature_label.pack(
            pady=5
        )

        self.status_label = tk.Label(
            monitor_frame,
            text="NORMAL",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#16A34A"
        )

        self.status_label.pack(
            pady=5
        )

        tk.Label(
            monitor_frame,
            text="Real-time temperature monitoring",
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack(
            pady=(0, 20)
        )

        # ==================================================
        # TEMPERATURE INFORMATION
        # ==================================================

        info_frame = tk.Frame(
            monitor_frame,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        info_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.info_row(
            info_frame,
            "Current Value",
            "32.6 °C"
        )

        self.info_row(
            info_frame,
            "Normal Range",
            "20 – 50 °C"
        )

        self.info_row(
            info_frame,
            "Detection Method",
            "Isolation Forest"
        )

        self.info_row(
            info_frame,
            "Data Type",
            "Unlabelled"
        )

        # ==================================================
        # RIGHT PANEL
        # ==================================================

        analysis_frame = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid",
            width=350
        )

        analysis_frame.pack(
            side="right",
            fill="y"
        )

        analysis_frame.pack_propagate(False)

        tk.Label(
            analysis_frame,
            text="TEMPERATURE ANALYSIS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        # ==================================================
        # NORMAL CONDITION
        # ==================================================

        self.analysis_box(
            analysis_frame,
            "NORMAL CONDITION",
            "Temperature is within\n"
            "the expected range.",
            "#16A34A"
        )

        # ==================================================
        # ANOMALY CONDITION
        # ==================================================

        self.anomaly_box = self.analysis_box(
            analysis_frame,
            "ANOMALY DETECTION",
            "Isolation Forest\n"
            "monitoring active.",
            "#2563EB"
        )

        # ==================================================
        # ALGORITHM
        # ==================================================

        tk.Frame(
            analysis_frame,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            analysis_frame,
            text="ALGORITHM",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25
        )

        algorithm_text = (
            "Isolation Forest\n\n"
            "• Unsupervised learning\n"
            "• Uses unlabelled data\n"
            "• Learns normal patterns\n"
            "• Detects unusual temperature\n"
            "• Returns NORMAL / ANOMALY"
        )

        tk.Label(
            analysis_frame,
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
        # SENSOR STATUS
        # ==================================================

        tk.Label(
            analysis_frame,
            text="SENSOR STATUS",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(10, 5)
        )

        self.sensor_status_label = tk.Label(
            analysis_frame,
            text="NOT CONNECTED",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748B"
        )

        self.sensor_status_label.pack(
            anchor="w",
            padx=25
        )

        # ==================================================
        # FOOTER
        # ==================================================

        tk.Label(
            self.page,
            text=(
                "Temperature data will be received from "
                "the Arduino sensor when hardware is connected."
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

    # ==================================================
    # INFORMATION ROW
    # ==================================================

    def info_row(
        self,
        parent,
        label,
        value
    ):

        row = tk.Frame(
            parent,
            bg="#F8FAFC"
        )

        row.pack(
            fill="x",
            padx=15,
            pady=6
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg="#172033"
        ).pack(
            side="right"
        )

    # ==================================================
    # ANALYSIS BOX
    # ==================================================

    def analysis_box(
        self,
        parent,
        title,
        text,
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
            text=text,
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        return box

    # ==================================================
    # UPDATE TEMPERATURE
    # ==================================================

    def update_temperature(
        self,
        temperature,
        anomaly=False,
        sensor_connected=True
    ):

        self.temperature = temperature

        # ------------------------------
        # SENSOR
        # ------------------------------

        if sensor_connected:

            self.sensor_card.config(
                text="CONNECTED",
                fg="#16A34A"
            )

            self.sensor_status_label.config(
                text="CONNECTED",
                fg="#16A34A"
            )

        else:

            self.sensor_card.config(
                text="NOT CONNECTED",
                fg="#64748B"
            )

            self.sensor_status_label.config(
                text="NOT CONNECTED",
                fg="#64748B"
            )

        # ------------------------------
        # TEMPERATURE
        # ------------------------------

        self.temperature_label.config(
            text=f"{temperature:.1f} °C"
        )

        self.value_card.config(
            text=f"{temperature:.1f} °C"
        )

        # ------------------------------
        # ANOMALY
        # ------------------------------

        if anomaly:

            self.status = "ANOMALY"

            self.status_label.config(
                text="TEMPERATURE ANOMALY",
                fg="#DC2626"
            )

            self.status_card.config(
                text="ANOMALY",
                fg="#DC2626"
            )

            self.anomaly_box.config(
                bg="#FEF2F2"
            )

        else:

            self.status = "NORMAL"

            self.status_label.config(
                text="NORMAL",
                fg="#16A34A"
            )

            self.status_card.config(
                text="NORMAL",
                fg="#16A34A"
            )

            self.anomaly_box.config(
                bg="#F8FAFC"
            )

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()