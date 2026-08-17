import tkinter as tk


class Settings:

    def __init__(self, parent):

        self.parent = parent

        # Default settings
        self.danger_zone_enabled = True
        self.fall_detection_enabled = True
        self.temperature_enabled = True
        self.vibration_enabled = True

        self.temperature_threshold = 50
        self.vibration_threshold = 5

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
        # MAIN CONTAINER
        # ==================================================

        container = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        container.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # MONITORING SETTINGS
        # ==================================================

        monitoring = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid"
        )

        monitoring.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            monitoring,
            text="MONITORING SETTINGS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        tk.Label(
            monitoring,
            text="Enable or disable individual safety monitoring modules.",
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # Monitoring switches

        self.create_switch(
            monitoring,
            "Danger Zone Detection",
            "Detect workers entering restricted areas.",
            "danger_zone"
        )

        self.create_switch(
            monitoring,
            "Fall Detection",
            "Detect abnormal horizontal body posture.",
            "fall"
        )

        self.create_switch(
            monitoring,
            "Temperature Monitoring",
            "Monitor temperature sensor anomalies.",
            "temperature"
        )

        self.create_switch(
            monitoring,
            "Vibration Monitoring",
            "Monitor abnormal machine vibration.",
            "vibration"
        )

        # ==================================================
        # THRESHOLD SETTINGS
        # ==================================================

        threshold_frame = tk.Frame(
            monitoring,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        threshold_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        tk.Label(
            threshold_frame,
            text="ANOMALY THRESHOLDS",
            font=("Arial", 11, "bold"),
            bg="#F8FAFC",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # Temperature

        temp_row = tk.Frame(
            threshold_frame,
            bg="#F8FAFC"
        )

        temp_row.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            temp_row,
            text="Temperature threshold (°C)",
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            side="left"
        )

        self.temperature_entry = tk.Entry(
            temp_row,
            width=10,
            font=("Arial", 9),
            relief="solid",
            bd=1
        )

        self.temperature_entry.pack(
            side="right"
        )

        self.temperature_entry.insert(
            0,
            str(self.temperature_threshold)
        )

        # Vibration

        vibration_row = tk.Frame(
            threshold_frame,
            bg="#F8FAFC"
        )

        vibration_row.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        tk.Label(
            vibration_row,
            text="Vibration threshold (mm/s)",
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            side="left"
        )

        self.vibration_entry = tk.Entry(
            vibration_row,
            width=10,
            font=("Arial", 9),
            relief="solid",
            bd=1
        )

        self.vibration_entry.pack(
            side="right"
        )

        self.vibration_entry.insert(
            0,
            str(self.vibration_threshold)
        )

        # Save button

        tk.Button(
            monitoring,
            text="SAVE SETTINGS",
            font=("Arial", 9, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9,
            command=self.save_settings
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        # ==================================================
        # SYSTEM INFORMATION
        # ==================================================

        system = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid",
            width=350
        )

        system.pack(
            side="right",
            fill="y"
        )

        system.pack_propagate(False)

        tk.Label(
            system,
            text="SYSTEM CONFIGURATION",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        self.info_box(
            system,
            "WORKER DETECTION",
            "YOLOv8n",
            "#2563EB"
        )

        self.info_box(
            system,
            "POSE DETECTION",
            "MediaPipe Pose",
            "#16A34A"
        )

        self.info_box(
            system,
            "ANOMALY DETECTION",
            "Isolation Forest",
            "#F59E0B"
        )

        self.info_box(
            system,
            "DECISION ENGINE",
            "Rule-Based Logic",
            "#DC2626"
        )

        # ==================================================
        # STATUS
        # ==================================================

        tk.Frame(
            system,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            system,
            text="CONFIGURATION STATUS",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25
        )

        self.status_label = tk.Label(
            system,
            text="DEFAULT CONFIGURATION",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#16A34A"
        )

        self.status_label.pack(
            anchor="w",
            padx=25,
            pady=10
        )

        # ==================================================
        # FOOTER
        # ==================================================

        tk.Label(
            self.page,
            text=(
                "Settings control the monitoring behaviour "
                "of the Industrial AI Safety System."
            ),
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            pady=8
        )

    # ==================================================
    # SWITCH
    # ==================================================

    def create_switch(
        self,
        parent,
        title,
        description,
        module
    ):

        row = tk.Frame(
            parent,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=5
        )

        text_frame = tk.Frame(
            row,
            bg="#F8FAFC"
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=10
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 10, "bold"),
            bg="#F8FAFC",
            fg="#172033"
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
            anchor="w",
            pady=(3, 0)
        )

        variable = tk.BooleanVar(
            value=True
        )

        check = tk.Checkbutton(
            row,
            variable=variable,
            onvalue=True,
            offvalue=False,
            bg="#F8FAFC",
            activebackground="#F8FAFC",
            cursor="hand2"
        )

        check.pack(
            side="right",
            padx=15
        )

        if module == "danger_zone":
            self.danger_zone_var = variable

        elif module == "fall":
            self.fall_var = variable

        elif module == "temperature":
            self.temperature_var = variable

        elif module == "vibration":
            self.vibration_var = variable

    # ==================================================
    # INFORMATION BOX
    # ==================================================

    def info_box(
        self,
        parent,
        title,
        value,
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
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        tk.Label(
            box,
            text=value,
            font=("Arial", 11, "bold"),
            bg="#F8FAFC",
            fg=color
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

    # ==================================================
    # SAVE SETTINGS
    # ==================================================

    def save_settings(self):

        self.danger_zone_enabled = (
            self.danger_zone_var.get()
        )

        self.fall_detection_enabled = (
            self.fall_var.get()
        )

        self.temperature_enabled = (
            self.temperature_var.get()
        )

        self.vibration_enabled = (
            self.vibration_var.get()
        )

        try:

            self.temperature_threshold = float(
                self.temperature_entry.get()
            )

            self.vibration_threshold = float(
                self.vibration_entry.get()
            )

            self.status_label.config(
                text="SETTINGS SAVED",
                fg="#16A34A"
            )

        except ValueError:

            self.status_label.config(
                text="INVALID THRESHOLD VALUE",
                fg="#DC2626"
            )

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()