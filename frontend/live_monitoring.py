import tkinter as tk
import cv2
import os
import sys
import json

from PIL import Image, ImageTk
from datetime import datetime

# ============================================================
# PROJECT ROOT
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
# IMPORT DETECTORS
# ============================================================

from backend.yolo_detector import YOLODetector
from backend.anomaly_detector import AnomalyDetector


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

# ============================================================
# VIDEO DIRECTORY
# ============================================================

VIDEO_DIR = os.path.join(
    DATA_DIR,
    "videos"
)

os.makedirs(
    VIDEO_DIR,
    exist_ok=True
)

# ============================================================
# INDUSTRIAL DEMO VIDEO
# ============================================================

VIDEO_FILE = os.path.join(
    VIDEO_DIR,
    "industrial_demo.mp4"
)

# ============================================================
# STATUS FILE
# ============================================================

STATUS_FILE = os.path.join(
    DATA_DIR,
    "latest_status.json"
)

# ============================================================
# LATEST IMAGES
# ============================================================

LATEST_IMAGE = os.path.join(
    DATA_DIR,
    "latest_monitoring.jpg"
)

LATEST_ANOMALY_IMAGE = os.path.join(
    DATA_DIR,
    "latest_anomaly.jpg"
)

LATEST_DANGER_IMAGE = os.path.join(
    DATA_DIR,
    "latest_danger.jpg"
)


# ============================================================
# LIVE MONITORING
# ============================================================

class LiveMonitoring:

    def __init__(self, parent):

        self.parent = parent

        # ----------------------------------------------------
        # CAMERA / VIDEO
        # ----------------------------------------------------

        self.camera = None

        self.using_video = False

        self.running = False

        self.photo = None

        # ----------------------------------------------------
        # DETECTORS
        # ----------------------------------------------------

        self.detector = None

        self.anomaly_detector = None

        # ----------------------------------------------------
        # ANOMALY CONTROL
        # ----------------------------------------------------

        self.previous_anomaly = False

        self.previous_danger = False

        self.anomaly_image_saved = False

        self.danger_image_saved = False

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.create_ui()


    # ========================================================
    # UI
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
        # CAMERA AREA
        # ====================================================

        camera_frame = tk.Frame(
            self.page,
            bg="#172033"
        )

        camera_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            camera_frame,
            text="LIVE INDUSTRIAL MONITORING",
            font=("Arial", 14, "bold"),
            bg="#172033",
            fg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.camera_label = tk.Label(
            camera_frame,
            text="Camera is not running",
            font=("Arial", 16, "bold"),
            bg="#08101F",
            fg="#94A3B8"
        )

        self.camera_label.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        # ====================================================
        # STATUS PANEL
        # ====================================================

        status_frame = tk.Frame(
            self.page,
            bg="white",
            bd=1,
            relief="solid",
            width=330
        )

        status_frame.pack(
            side="right",
            fill="y"
        )

        status_frame.pack_propagate(False)

        tk.Label(
            status_frame,
            text="SAFETY STATUS",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 30)
        )

        # ====================================================
        # STATUS ROWS
        # ====================================================

        self.system_status = self.status_row(
            status_frame,
            "SYSTEM",
            "OFFLINE"
        )

        self.worker_status = self.status_row(
            status_frame,
            "WORKER",
            "NOT DETECTED"
        )

        self.danger_status = self.status_row(
            status_frame,
            "DANGER ZONE",
            "SAFE"
        )

        self.fall_status = self.status_row(
            status_frame,
            "FALL",
            "NOT DETECTED"
        )

        self.anomaly_status = self.status_row(
            status_frame,
            "ANOMALY",
            "NOT DETECTED"
        )

        self.risk_status = self.status_row(
            status_frame,
            "RISK LEVEL",
            "LOW"
        )

        # ====================================================
        # CURRENT EVENT
        # ====================================================

        tk.Frame(
            status_frame,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            status_frame,
            text="CURRENT EVENT",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25
        )

        self.event_label = tk.Label(
            status_frame,
            text="System waiting...",
            font=("Arial", 10),
            bg="white",
            fg="#64748B",
            justify="left",
            wraplength=270
        )

        self.event_label.pack(
            anchor="w",
            padx=25,
            pady=10
        )

        # ====================================================
        # AI DETECTION
        # ====================================================

        tk.Label(
            status_frame,
            text="AI DETECTION",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(10, 0)
        )

        ai_text = (
            "YOLOv8 Worker Detection\n"
            "Bounding Box Detection\n"
            "Danger Zone Analysis\n"
            "MediaPipe Pose Detection\n"
            "MediaPipe Hand Detection\n"
            "Fall Detection\n"
            "Isolation Forest Anomaly Detection"
        )

        tk.Label(
            status_frame,
            text=ai_text,
            font=("Arial", 9),
            bg="white",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=12
        )

        # ====================================================
        # START BUTTON
        # ====================================================

        self.start_button = tk.Button(
            status_frame,
            text="▶  START MONITORING",
            font=("Arial", 11, "bold"),
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.start_monitoring
        )

        self.start_button.pack(
            fill="x",
            padx=25,
            pady=(10, 8)
        )

        # ====================================================
        # STOP BUTTON
        # ====================================================

        self.stop_button = tk.Button(
            status_frame,
            text="■  STOP MONITORING",
            font=("Arial", 11, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.stop_monitoring
        )

        self.stop_button.pack(
            fill="x",
            padx=25
        )


    # ========================================================
    # STATUS ROW
    # ========================================================

    def status_row(
        self,
        parent,
        label,
        value
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=7
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack(
            side="left"
        )

        value_label = tk.Label(
            row,
            text=value,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748B"
        )

        value_label.pack(
            side="right"
        )

        return value_label


    # ========================================================
    # START MONITORING
    # ========================================================

    def start_monitoring(self):

        if self.running:
            return

        # ====================================================
        # RESET STATES
        # ====================================================

        self.previous_anomaly = False
        self.previous_danger = False

        self.anomaly_image_saved = False
        self.danger_image_saved = False

        # ====================================================
        # LOAD YOLO DETECTOR
        # ====================================================

        try:

            self.detector = YOLODetector()

        except Exception as e:

            self.camera_label.config(
                text=f"YOLO detector error:\n{e}"
            )

            return

        # ====================================================
        # LOAD ANOMALY DETECTOR
        # ====================================================

        try:

            self.anomaly_detector = AnomalyDetector()

        except Exception as e:

            self.camera_label.config(
                text=f"Anomaly detector error:\n{e}"
            )

            self.detector = None

            return

        # ====================================================
        # SELECT VIDEO OR CAMERA
        # ====================================================

        if os.path.exists(VIDEO_FILE):

            print(
                "Industrial demo video found."
            )

            print(
                f"Using video: {VIDEO_FILE}"
            )

            self.camera = cv2.VideoCapture(
                VIDEO_FILE
            )

            self.using_video = True

        else:

            print(
                "Industrial demo video not found."
            )

            print(
                "Opening webcam..."
            )

            self.camera = cv2.VideoCapture(
                0
            )

            self.using_video = False

        # ====================================================
        # CHECK SOURCE
        # ====================================================

        if not self.camera.isOpened():

            self.system_status.config(
                text="OFFLINE",
                fg="#DC2626"
            )

            self.camera_label.config(
                text="Video / camera could not be opened"
            )

            self.detector = None
            self.anomaly_detector = None

            return

        # ====================================================
        # CAMERA SETTINGS
        # ====================================================

        if not self.using_video:

            self.camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                1280
            )

            self.camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                720
            )

        # ====================================================
        # START
        # ====================================================

        self.running = True

        self.system_status.config(
            text="ONLINE",
            fg="#16A34A"
        )

        self.start_button.config(
            state="disabled"
        )

        if self.using_video:

            self.event_label.config(
                text="Industrial demo video running..."
            )

        else:

            self.event_label.config(
                text="Live camera monitoring..."
            )

        self.update_camera()


    # ========================================================
    # UPDATE CAMERA / VIDEO
    # ========================================================

    def update_camera(self):

        if not self.running:
            return

        if self.camera is None:
            return

        # ====================================================
        # READ FRAME
        # ====================================================

        success, frame = self.camera.read()

        # ====================================================
        # VIDEO ENDED
        # ====================================================

        if not success:

            if self.using_video:

                # Restart video from beginning
                self.camera.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    0
                )

                success, frame = (
                    self.camera.read()
                )

                if not success:

                    self.camera_label.config(
                        text="Industrial video ended"
                    )

                    self.stop_monitoring()

                    return

            else:

                self.camera_label.config(
                    text="Camera frame unavailable"
                )

                self.parent.after(
                    100,
                    self.update_camera
                )

                return

        # ====================================================
        # PROCESS YOLO + MEDIAPIPE
        # ====================================================

        try:

            processed_frame, result = (
                self.detector.process_frame(
                    frame
                )
            )

        except Exception as e:

            self.camera_label.config(
                text=f"Detection error:\n{e}"
            )

            self.parent.after(
                100,
                self.update_camera
            )

            return

        # ====================================================
        # GET YOLO RESULTS
        # ====================================================

        worker = result.get(
            "worker",
            False
        )

        danger = result.get(
            "danger",
            False
        )

        fall = result.get(
            "fall",
            False
        )

        hand_danger = result.get(
            "hand_danger",
            False
        )

        body_danger = result.get(
            "body_danger",
            False
        )

        status = result.get(
            "status",
            "NO WORKER"
        )

        # ====================================================
        # GET POSE LANDMARKS
        # ====================================================

        pose_landmarks = result.get(
            "pose_landmarks",
            None
        )

        # ====================================================
        # ANOMALY DETECTION
        # ====================================================

        anomaly_result = {
            "anomaly": False,
            "status": "NO POSE"
        }

        if (
            self.anomaly_detector is not None
            and
            pose_landmarks is not None
        ):

            try:

                features = (
                    self.anomaly_detector.extract_features(
                        pose_landmarks
                    )
                )

                anomaly_result = (
                    self.anomaly_detector.detect(
                        features
                    )
                )

            except Exception as e:

                print(
                    f"Anomaly detection error: {e}"
                )

                anomaly_result = {
                    "anomaly": False,
                    "status": "ERROR"
                }

        # ====================================================
        # ANOMALY RESULT
        # ====================================================

        anomaly = anomaly_result.get(
            "anomaly",
            False
        )

        anomaly_state = anomaly_result.get(
            "status",
            "NO POSE"
        )

        # ====================================================
        # WORKER STATUS
        # ====================================================

        if worker:

            self.worker_status.config(
                text="DETECTED",
                fg="#16A34A"
            )

        else:

            self.worker_status.config(
                text="NOT DETECTED",
                fg="#64748B"
            )

        # ====================================================
        # DANGER STATUS
        # ====================================================

        if danger:

            if hand_danger:

                danger_text = "HAND DANGER"

            elif body_danger:

                danger_text = "BODY DANGER"

            else:

                danger_text = "DANGER"

            self.danger_status.config(
                text=danger_text,
                fg="#DC2626"
            )

        else:

            self.danger_status.config(
                text="SAFE",
                fg="#16A34A"
            )

        # ====================================================
        # FALL STATUS
        # ====================================================

        if fall:

            self.fall_status.config(
                text="DETECTED",
                fg="#DC2626"
            )

        else:

            self.fall_status.config(
                text="NOT DETECTED",
                fg="#64748B"
            )

        # ====================================================
        # ANOMALY STATUS
        # ====================================================

        if anomaly:

            self.anomaly_status.config(
                text="DETECTED",
                fg="#DC2626"
            )

        elif anomaly_state == "LEARNING":

            self.anomaly_status.config(
                text="LEARNING",
                fg="#D97706"
            )

        elif anomaly_state == "NORMAL":

            self.anomaly_status.config(
                text="NORMAL",
                fg="#16A34A"
            )

        elif anomaly_state == "ERROR":

            self.anomaly_status.config(
                text="ERROR",
                fg="#DC2626"
            )

        else:

            self.anomaly_status.config(
                text="NOT DETECTED",
                fg="#64748B"
            )

        # ====================================================
        # RISK LEVEL
        # ====================================================

        if anomaly or fall:

            risk_level = "HIGH"

            risk_color = "#DC2626"

        elif danger:

            risk_level = "MEDIUM"

            risk_color = "#D97706"

        else:

            risk_level = "LOW"

            risk_color = "#16A34A"

        self.risk_status.config(
            text=risk_level,
            fg=risk_color
        )

        # ====================================================
        # CURRENT EVENT
        # ====================================================

        if anomaly:

            alert_message = (
                "Industrial anomaly detected"
            )

        elif fall:

            alert_message = (
                "Worker fall detected"
            )

        elif hand_danger:

            alert_message = (
                "Worker hand entered danger zone"
            )

        elif body_danger:

            alert_message = (
                "Worker entered danger zone"
            )

        elif worker:

            alert_message = (
                "Worker detected - activity normal"
            )

        else:

            alert_message = (
                "No worker detected"
            )

        self.event_label.config(
            text=alert_message
        )

        # ====================================================
        # DRAW ANOMALY STATUS ON VIDEO
        # ====================================================

        if anomaly:

            cv2.putText(
                processed_frame,
                "INDUSTRIAL ANOMALY DETECTED",
                (25, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.70,
                (0, 0, 255),
                3
            )

        elif anomaly_state == "LEARNING":

            cv2.putText(
                processed_frame,
                "ANOMALY MODEL: LEARNING",
                (25, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 255),
                2
            )

        elif anomaly_state == "NORMAL":

            cv2.putText(
                processed_frame,
                "INDUSTRIAL ACTIVITY: NORMAL",
                (25, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 180, 0),
                2
            )

        # ====================================================
        # DISPLAY RISK LEVEL
        # ====================================================

        cv2.putText(
            processed_frame,
            f"RISK LEVEL: {risk_level}",
            (25, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.70,
            (
                (0, 0, 255)
                if risk_level == "HIGH"
                else
                (0, 165, 255)
                if risk_level == "MEDIUM"
                else
                (0, 180, 0)
            ),
            2
        )

        # ====================================================
        # SAVE LATEST MONITORING IMAGE
        # ====================================================

        try:

            cv2.imwrite(
                LATEST_IMAGE,
                processed_frame
            )

        except Exception as e:

            print(
                f"Latest image error: {e}"
            )

        # ====================================================
        # SAVE ANOMALY IMAGE
        #
        # Only save when anomaly changes from
        # False -> True.
        #
        # This prevents saving hundreds of images.
        # ====================================================

        if anomaly and not self.previous_anomaly:

            try:

                cv2.imwrite(
                    LATEST_ANOMALY_IMAGE,
                    processed_frame
                )

                self.anomaly_image_saved = True

                print(
                    "Latest anomaly image saved:"
                )

                print(
                    LATEST_ANOMALY_IMAGE
                )

            except Exception as e:

                print(
                    f"Anomaly image error: {e}"
                )

        self.previous_anomaly = anomaly

        # ====================================================
        # SAVE DANGER IMAGE
        #
        # Only save when danger changes from
        # False -> True.
        # ====================================================

        if danger and not self.previous_danger:

            try:

                cv2.imwrite(
                    LATEST_DANGER_IMAGE,
                    processed_frame
                )

                self.danger_image_saved = True

                print(
                    "Latest danger image saved:"
                )

                print(
                    LATEST_DANGER_IMAGE
                )

            except Exception as e:

                print(
                    f"Danger image error: {e}"
                )

        self.previous_danger = danger

        # ====================================================
        # SAVE STATUS JSON
        # ====================================================

        latest_data = {

            "system": "ONLINE",

            "worker": bool(worker),

            "danger": bool(danger),

            "hand_danger": bool(
                hand_danger
            ),

            "body_danger": bool(
                body_danger
            ),

            "fall": bool(fall),

            "anomaly": bool(anomaly),

            "anomaly_status": anomaly_state,

            "risk_level": risk_level,

            "status": status,

            "message": alert_message,

            "latest_anomaly_image": (
                LATEST_ANOMALY_IMAGE
                if self.anomaly_image_saved
                else ""
            ),

            "latest_danger_image": (
                LATEST_DANGER_IMAGE
                if self.danger_image_saved
                else ""
            ),

            "time": datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )
        }

        try:

            with open(
                STATUS_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    latest_data,
                    file,
                    indent=4
                )

        except Exception as e:

            print(
                f"Status file error: {e}"
            )

        # ====================================================
        # DISPLAY FRAME
        # ====================================================

        rgb = cv2.cvtColor(
            processed_frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(
            rgb
        )

        # ====================================================
        # RESIZE
        # ====================================================

        display_width = 760
        display_height = 500

        image.thumbnail(
            (
                display_width,
                display_height
            ),
            Image.Resampling.LANCZOS
        )

        self.photo = ImageTk.PhotoImage(
            image
        )

        self.camera_label.config(
            image=self.photo,
            text=""
        )

        self.camera_label.image = self.photo

        # ====================================================
        # CONTINUE
        # ====================================================

        self.parent.after(
            30,
            self.update_camera
        )


    # ========================================================
    # STOP MONITORING
    # ========================================================

    def stop_monitoring(self):

        self.running = False

        # ====================================================
        # CAMERA / VIDEO
        # ====================================================

        if self.camera is not None:

            self.camera.release()

            self.camera = None

        # ====================================================
        # YOLO DETECTOR
        # ====================================================

        if self.detector is not None:

            try:

                self.detector.release()

            except Exception:

                pass

            self.detector = None

        # ====================================================
        # ANOMALY DETECTOR
        # ====================================================

        if self.anomaly_detector is not None:

            try:

                self.anomaly_detector.reset()

            except Exception:

                pass

            self.anomaly_detector = None

        # ====================================================
        # UI
        # ====================================================

        self.camera_label.config(
            image="",
            text="Camera is not running"
        )

        self.camera_label.image = None

        self.system_status.config(
            text="OFFLINE",
            fg="#64748B"
        )

        self.worker_status.config(
            text="NOT DETECTED",
            fg="#64748B"
        )

        self.danger_status.config(
            text="SAFE",
            fg="#16A34A"
        )

        self.fall_status.config(
            text="NOT DETECTED",
            fg="#64748B"
        )

        self.anomaly_status.config(
            text="NOT DETECTED",
            fg="#64748B"
        )

        self.risk_status.config(
            text="LOW",
            fg="#16A34A"
        )

        self.event_label.config(
            text="System waiting..."
        )

        self.start_button.config(
            state="normal"
        )


    # ========================================================
    # CLEANUP
    # ========================================================

    def destroy(self):

        self.stop_monitoring()

        if self.page.winfo_exists():

            self.page.destroy()