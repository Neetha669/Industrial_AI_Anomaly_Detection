import tkinter as tk


class WorkerStatus:

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

        # Worker detected
        self.create_card(
            summary,
            "WORKER DETECTED",
            "0",
            "#2563EB"
        )

        # Worker status
        self.create_card(
            summary,
            "WORKER STATUS",
            "SAFE",
            "#16A34A"
        )

        # Danger zone
        self.create_card(
            summary,
            "DANGER ZONE",
            "SAFE",
            "#16A34A"
        )

        # Fall
        self.create_card(
            summary,
            "FALL STATUS",
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
        # WORKER DETECTION PANEL
        # ==================================================

        detection_frame = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid"
        )

        detection_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            detection_frame,
            text="WORKER DETECTION",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        # Worker icon
        tk.Label(
            detection_frame,
            text="👤",
            font=("Segoe UI Emoji", 60),
            bg="white",
            fg="#2563EB"
        ).pack(
            pady=10
        )

        self.worker_detected_label = tk.Label(
            detection_frame,
            text="NO WORKER DETECTED",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#64748B"
        )

        self.worker_detected_label.pack(
            pady=10
        )

        tk.Label(
            detection_frame,
            text="YOLOv8 Worker Detection",
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack()

        tk.Label(
            detection_frame,
            text="Detects the complete worker body\n"
                 "and visible body parts using AI vision.",
            font=("Arial", 9),
            bg="white",
            fg="#94A3B8",
            justify="center"
        ).pack(
            pady=15
        )

        # ==================================================
        # SAFETY ANALYSIS
        # ==================================================

        safety_frame = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid",
            width=340
        )

        safety_frame.pack(
            side="right",
            fill="y"
        )

        safety_frame.pack_propagate(False)

        tk.Label(
            safety_frame,
            text="SAFETY ANALYSIS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 20)
        )

        # Status rows

        self.status_row(
            safety_frame,
            "Worker",
            "SAFE",
            "#16A34A"
        )

        self.status_row(
            safety_frame,
            "Danger Zone",
            "SAFE",
            "#16A34A"
        )

        self.status_row(
            safety_frame,
            "Fall Detection",
            "NOT DETECTED",
            "#64748B"
        )

        self.status_row(
            safety_frame,
            "Pose Detection",
            "READY",
            "#2563EB"
        )

        self.status_row(
            safety_frame,
            "AI Detection",
            "ACTIVE",
            "#16A34A"
        )

        # --------------------------------------------------
        # DETECTION METHODS
        # --------------------------------------------------

        tk.Frame(
            safety_frame,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            safety_frame,
            text="DETECTION METHODS",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=20
        )

        methods = (
            "• YOLOv8 person detection\n"
            "• Bounding box analysis\n"
            "• MediaPipe pose detection\n"
            "• 33 body keypoints\n"
            "• Danger zone analysis\n"
            "• Fall detection"
        )

        tk.Label(
            safety_frame,
            text=methods,
            font=("Arial", 9),
            bg="white",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=12
        )

        # ==================================================
        # NOTE
        # ==================================================

        tk.Label(
            self.page,
            text=(
                "Worker safety status is updated from the "
                "real-time AI detection modules."
            ),
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            pady=8
        )

    # ==================================================
    # CARD
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
    # STATUS ROW
    # ==================================================

    def status_row(
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
            padx=20,
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
    # UPDATE WORKER STATUS
    # ==================================================

    def update_status(
        self,
        worker_detected=False,
        danger=False,
        fall=False
    ):

        if worker_detected:

            self.worker_detected_label.config(
                text="WORKER DETECTED",
                fg="#16A34A"
            )

        else:

            self.worker_detected_label.config(
                text="NO WORKER DETECTED",
                fg="#64748B"
            )

        # Worker status

        # You can connect these to the actual
        # YOLO + danger zone + fall detection later.

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()