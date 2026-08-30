import tkinter as tk
from PIL import Image, ImageTk
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
# WORKER STATUS
# ============================================================

class WorkerStatus:

    def __init__(self, parent):

        self.parent = parent

        # ----------------------------------------------------
        # DATA DIRECTORY
        # ----------------------------------------------------

        self.data_dir = os.path.join(
            PROJECT_ROOT,
            "data"
        )

        # ----------------------------------------------------
        # AUTOMATICALLY CAPTURED WORKER IMAGE
        # ----------------------------------------------------

        self.worker_photo_path = os.path.join(
            self.data_dir,
            "latest_worker.jpg"
        )

        # Keep reference to image
        self.worker_image = None

        # ----------------------------------------------------
        # CREATE UI
        # ----------------------------------------------------

        self.create_ui()

        # ----------------------------------------------------
        # START AUTOMATIC PHOTO MONITORING
        # ----------------------------------------------------

        self.monitor_worker_photo()

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
        # TOP SUMMARY
        # ====================================================

        summary = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        summary.pack(
            fill="x",
            pady=(0, 15)
        )

        self.worker_detected_card = self.create_card(
            summary,
            "WORKER DETECTED",
            "0",
            "#2563EB"
        )

        self.worker_status_card = self.create_card(
            summary,
            "WORKER STATUS",
            "SAFE",
            "#16A34A"
        )

        self.danger_card = self.create_card(
            summary,
            "DANGER ZONE",
            "SAFE",
            "#16A34A"
        )

        self.fall_card = self.create_card(
            summary,
            "FALL STATUS",
            "NOT DETECTED",
            "#64748B"
        )

        # ====================================================
        # MAIN AREA
        # ====================================================

        main_area = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        main_area.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # WORKER DETECTION PANEL
        # ====================================================

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
            pady=(20, 10)
        )

        # ====================================================
        # WORKER PHOTO AREA
        # ====================================================

        photo_container = tk.Frame(
            detection_frame,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        photo_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 10)
        )

        self.worker_photo_label = tk.Label(
            photo_container,
            text="WAITING FOR WORKER DETECTION...",
            font=("Arial", 13, "bold"),
            bg="#F8FAFC",
            fg="#94A3B8",
            justify="center"
        )

        self.worker_photo_label.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # WORKER STATUS TEXT
        # ====================================================

        self.worker_detected_label = tk.Label(
            detection_frame,
            text="WAITING FOR WORKER DETECTION",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#64748B"
        )

        self.worker_detected_label.pack(
            pady=(5, 5)
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
            text=(
                "Automatically captures the latest detected worker "
                "from the AI monitoring video."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#94A3B8",
            justify="center"
        ).pack(
            pady=(5, 15)
        )

        # ====================================================
        # SAFETY ANALYSIS
        # ====================================================

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

        # ----------------------------------------------------
        # STATUS ROWS
        # ----------------------------------------------------

        self.worker_status_row = self.status_row(
            safety_frame,
            "Worker",
            "SAFE",
            "#16A34A"
        )

        self.danger_status_row = self.status_row(
            safety_frame,
            "Danger Zone",
            "SAFE",
            "#16A34A"
        )

        self.fall_status_row = self.status_row(
            safety_frame,
            "Fall Detection",
            "NOT DETECTED",
            "#64748B"
        )

        self.pose_status_row = self.status_row(
            safety_frame,
            "Pose Detection",
            "READY",
            "#2563EB"
        )

        self.ai_status_row = self.status_row(
            safety_frame,
            "AI Detection",
            "ACTIVE",
            "#16A34A"
        )

        # ====================================================
        # DETECTION METHODS
        # ====================================================

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
            "• Worker bounding box\n"
            "• Automatic worker capture\n"
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

        # ====================================================
        # FOOTER
        # ====================================================

        tk.Label(
            self.page,
            text=(
                "Worker safety status is updated automatically "
                "from the real-time AI detection system."
            ),
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            pady=8
        )

    # ========================================================
    # CREATE CARD
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
    # STATUS ROW
    # ========================================================

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

        value_label = tk.Label(
            row,
            text=value,
            font=("Arial", 9, "bold"),
            bg="white",
            fg=color
        )

        value_label.pack(
            side="right"
        )

        return value_label

    # ========================================================
    # AUTOMATICALLY LOAD LATEST WORKER PHOTO
    # ========================================================

    def monitor_worker_photo(self):

        try:

            if not self.page.winfo_exists():

                return

            self.load_worker_photo()

            # Check every 1 second

            self.page.after(
                1000,
                self.monitor_worker_photo
            )

        except tk.TclError:

            pass

    # ========================================================
    # LOAD WORKER PHOTO
    # ========================================================

    def load_worker_photo(self):

        if not os.path.exists(
            self.worker_photo_path
        ):

            self.worker_photo_label.config(
                image="",
                text="WAITING FOR WORKER DETECTION...",
                fg="#94A3B8"
            )

            return

        try:

            # Open image
            image = Image.open(
                self.worker_photo_path
            )

            # Force actual image loading
            image.load()

            # Convert to RGB
            image = image.convert(
                "RGB"
            )

            # Get available display area
            max_width = 760
            max_height = 420

            image.thumbnail(
                (
                    max_width,
                    max_height
                ),
                Image.Resampling.LANCZOS
            )

            # Convert for Tkinter
            self.worker_image = ImageTk.PhotoImage(
                image
            )

            self.worker_photo_label.config(
                image=self.worker_image,
                text=""
            )

            # IMPORTANT:
            # Keep reference alive
            self.worker_photo_label.image = (
                self.worker_image
            )

        except Exception as error:

            print(
                "Worker photo loading error:",
                error
            )

            self.worker_photo_label.config(
                image="",
                text="UNABLE TO LOAD WORKER PHOTO",
                fg="#DC2626"
            )

    # ========================================================
    # UPDATE WORKER STATUS
    # ========================================================

    def update_status(
        self,
        worker_detected=False,
        danger=False,
        fall=False
    ):

        # ----------------------------------------------------
        # WORKER
        # ----------------------------------------------------

        if worker_detected:

            self.worker_detected_card.config(
                text="1"
            )

            self.worker_detected_label.config(
                text="WORKER DETECTED",
                fg="#16A34A"
            )

            self.worker_status_card.config(
                text="SAFE",
                fg="#16A34A"
            )

            self.worker_status_row.config(
                text="SAFE",
                fg="#16A34A"
            )

        else:

            self.worker_detected_card.config(
                text="0"
            )

            self.worker_detected_label.config(
                text="NO WORKER DETECTED",
                fg="#64748B"
            )

            self.worker_status_card.config(
                text="NO WORKER",
                fg="#64748B"
            )

            self.worker_status_row.config(
                text="NO WORKER",
                fg="#64748B"
            )

        # ----------------------------------------------------
        # DANGER
        # ----------------------------------------------------

        if danger:

            self.danger_card.config(
                text="DANGER",
                fg="#DC2626"
            )

            self.danger_status_row.config(
                text="DANGER",
                fg="#DC2626"
            )

        else:

            self.danger_card.config(
                text="SAFE",
                fg="#16A34A"
            )

            self.danger_status_row.config(
                text="SAFE",
                fg="#16A34A"
            )

        # ----------------------------------------------------
        # FALL
        # ----------------------------------------------------

        if fall:

            self.fall_card.config(
                text="DETECTED",
                fg="#DC2626"
            )

            self.fall_status_row.config(
                text="DETECTED",
                fg="#DC2626"
            )

            self.worker_status_card.config(
                text="CRITICAL",
                fg="#DC2626"
            )

            self.worker_status_row.config(
                text="CRITICAL",
                fg="#DC2626"
            )

        else:

            self.fall_card.config(
                text="NOT DETECTED",
                fg="#64748B"
            )

            self.fall_status_row.config(
                text="NOT DETECTED",
                fg="#64748B"
            )

    # ========================================================
    # CLEANUP
    # ========================================================

    def destroy(self):

        try:

            self.page.destroy()

        except Exception:

            pass