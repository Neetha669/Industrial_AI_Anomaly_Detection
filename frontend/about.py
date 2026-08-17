import tkinter as tk


class About:

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
        # MAIN CARD
        # ==================================================

        main = tk.Frame(
            self.page,
            bg="white",
            bd=1,
            relief="solid"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # ==================================================
        # HEADER
        # ==================================================

        tk.Label(
            main,
            text="INDUSTRIAL AI",
            font=("Arial", 26, "bold"),
            bg="white",
            fg="#2563EB"
        ).pack(
            pady=(25, 0)
        )

        tk.Label(
            main,
            text="ANOMALY DETECTION SYSTEM",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            pady=(2, 5)
        )

        tk.Label(
            main,
            text="AI-Based Real-Time Cyber-Physical Threat Detection",
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack(
            pady=(0, 20)
        )

        # ==================================================
        # ABOUT PROJECT
        # ==================================================

        description = tk.Frame(
            main,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        description.pack(
            fill="x",
            padx=35,
            pady=8
        )

        tk.Label(
            description,
            text="ABOUT THE PROJECT",
            font=("Arial", 13, "bold"),
            bg="#F8FAFC",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        # Use a frame with controlled width
        text_frame = tk.Frame(
            description,
            bg="#F8FAFC"
        )

        text_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

        project_text = (
            "The Industrial AI Anomaly Detection System is designed "
            "to improve worker safety in industrial environments.\n\n"

            "The system combines computer vision and sensor-based "
            "monitoring to identify unsafe situations and abnormal "
            "patterns in real time.\n\n"

            "Worker detection, danger-zone monitoring and fall detection "
            "are performed using AI-based vision methods, while "
            "temperature and machine vibration can be monitored using "
            "unsupervised anomaly detection."
        )

        tk.Label(
            text_frame,
            text=project_text,
            font=("Arial", 10),
            bg="#F8FAFC",
            fg="#475569",
            justify="left",
            anchor="w",
            wraplength=750
        ).pack(
            fill="x",
            anchor="w"
        )

        # ==================================================
        # TECHNOLOGY & AI MODULES
        # ==================================================

        tk.Label(
            main,
            text="TECHNOLOGY & AI MODULES",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=35,
            pady=(18, 10)
        )

        tech_frame = tk.Frame(
            main,
            bg="white"
        )

        tech_frame.pack(
            fill="x",
            padx=30
        )

        self.tech_card(
            tech_frame,
            "YOLOv8n",
            "Worker Detection",
            "#2563EB"
        )

        self.tech_card(
            tech_frame,
            "MediaPipe",
            "Pose & Fall Detection",
            "#16A34A"
        )

        self.tech_card(
            tech_frame,
            "Isolation Forest",
            "Sensor Anomaly Detection",
            "#F59E0B"
        )

        self.tech_card(
            tech_frame,
            "Decision Logic",
            "Risk Classification",
            "#DC2626"
        )

        # ==================================================
        # SAFETY CLASSIFICATION
        # ==================================================

        tk.Label(
            main,
            text="SAFETY CLASSIFICATION",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=35,
            pady=(20, 10)
        )

        safety = tk.Frame(
            main,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        safety.pack(
            fill="x",
            padx=35
        )

        self.safety_item(
            safety,
            "SAFE",
            "No abnormal condition detected.",
            "#16A34A"
        )

        self.safety_item(
            safety,
            "DANGER",
            "Worker or machine condition requires attention.",
            "#F59E0B"
        )

        self.safety_item(
            safety,
            "HIGH RISK",
            "Multiple abnormal conditions detected.",
            "#EA580C"
        )

        self.safety_item(
            safety,
            "CRITICAL EMERGENCY",
            "Immediate safety response required.",
            "#DC2626"
        )

        # ==================================================
        # PROJECT PURPOSE
        # ==================================================

        purpose = (
            "The goal is to provide an integrated safety monitoring "
            "platform that combines visual and sensor-based information "
            "for faster detection of industrial hazards."
        )

        tk.Label(
            main,
            text=purpose,
            font=("Arial", 9),
            bg="white",
            fg="#64748B",
            justify="center",
            wraplength=750
        ).pack(
            pady=18
        )

        # ==================================================
        # VERSION
        # ==================================================

        tk.Label(
            main,
            text="Industrial AI Safety System  •  Version 1.0",
            font=("Arial", 8),
            bg="white",
            fg="#94A3B8"
        ).pack(
            pady=(0, 12)
        )

    # ==================================================
    # TECHNOLOGY CARD
    # ==================================================

    def tech_card(
        self,
        parent,
        technology,
        purpose,
        color
    ):

        card = tk.Frame(
            parent,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=technology,
            font=("Arial", 10, "bold"),
            bg="#F8FAFC",
            fg=color
        ).pack(
            pady=(12, 4)
        )

        tk.Label(
            card,
            text=purpose,
            font=("Arial", 8),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            pady=(0, 12)
        )

    # ==================================================
    # SAFETY ITEM
    # ==================================================

    def safety_item(
        self,
        parent,
        title,
        description,
        color
    ):

        row = tk.Frame(
            parent,
            bg="#F8FAFC"
        )

        row.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            row,
            text="●",
            font=("Arial", 13),
            bg="#F8FAFC",
            fg=color
        ).pack(
            side="left",
            padx=(5, 10)
        )

        tk.Label(
            row,
            text=title,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg=color,
            width=22,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=description,
            font=("Arial", 9),
            bg="#F8FAFC",
            fg="#64748B",
            anchor="w"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        self.page.destroy()