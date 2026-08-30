import tkinter as tk
from tkinter import messagebox

import cv2
import os
import sys
import json
import threading
import winsound

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
# BACKEND IMPORTS
# ============================================================

from backend.yolo_detector import YOLODetector


try:
    from backend.anomaly_detector import AnomalyDetector
except ImportError:
    AnomalyDetector = None


try:
    from backend.incident_manager import IncidentManager
except ImportError:
    IncidentManager = None


# ============================================================
# DATA DIRECTORY
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
# VIDEO FILES
# ============================================================

VIDEO_1 = os.path.join(
    VIDEO_DIR,
    "industrial_demo.mp4"
)

VIDEO_2 = os.path.join(
    VIDEO_DIR,
    "industrial_danger.mp4"
)


# ============================================================
# STATUS FILE
# ============================================================

STATUS_FILE = os.path.join(
    DATA_DIR,
    "latest_status.json"
)


# ============================================================
# IMAGE FILES
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
# SIMULATED SENSOR SETTINGS
# ============================================================

TEMPERATURE_THRESHOLD = 70.0

VIBRATION_THRESHOLD = 7.0


# ============================================================
# LIVE MONITORING
# ============================================================

class LiveMonitoring:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        parent,
        alerts_page=None
    ):

        self.parent = parent

        self.alerts_page = alerts_page

        # ----------------------------------------------------
        # CAMERA
        # ----------------------------------------------------

        self.camera = None

        self.using_video = False

        self.running = False

        self.photo = None

        # ----------------------------------------------------
        # SELECTED VIDEO
        # ----------------------------------------------------

        self.selected_video = VIDEO_1

        # ----------------------------------------------------
        # DETECTORS
        # ----------------------------------------------------

        self.detector = None

        self.anomaly_detector = None

        # ----------------------------------------------------
        # INCIDENT MANAGER
        # ----------------------------------------------------

        if IncidentManager:

            try:

                self.incident_manager = IncidentManager()

            except Exception as e:

                print(
                    f"Incident manager initialization error: {e}"
                )

                self.incident_manager = None

        else:

            self.incident_manager = None

        # ----------------------------------------------------
        # PREVIOUS STATES
        # ----------------------------------------------------

        self.previous_anomaly = False

        self.previous_danger = False

        self.previous_fall = False

        self.previous_hand_danger = False

        self.previous_body_danger = False

        self.previous_temperature_danger = False

        self.previous_vibration_danger = False

        # ----------------------------------------------------
        # IMAGE FLAGS
        # ----------------------------------------------------

        self.anomaly_image_saved = False

        self.danger_image_saved = False

        # ----------------------------------------------------
        # SENSOR VALUES
        # ----------------------------------------------------

        self.temperature = 0.0

        self.vibration = 0.0

        # ====================================================
        # CONTINUOUS ALERT SOUND
        # ====================================================

        self.alert_sound_thread = None

        self.alert_sound_stop_event = threading.Event()

        self.alert_sound_lock = threading.Lock()

        # ----------------------------------------------------
        # CREATE UI
        # ----------------------------------------------------

        self.create_ui()


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
            padx=(0, 6)
        )


        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            camera_frame,
            text="LIVE INDUSTRIAL MONITORING",
            font=("Arial", 14, "bold"),
            bg="#172033",
            fg="white"
        ).pack(
            anchor="w",
            padx=15,
            pady=9
        )


        # ====================================================
        # VIDEO SELECTOR
        # ====================================================

        selector_frame = tk.Frame(
            camera_frame,
            bg="#172033"
        )

        selector_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 7)
        )


        tk.Label(
            selector_frame,
            text="SELECT VIDEO:",
            font=("Arial", 9, "bold"),
            bg="#172033",
            fg="white"
        ).pack(
            side="left",
            padx=(5, 10)
        )


        self.video_var = tk.StringVar(
            value="Video 1 - Fall"
        )


        self.video_menu = tk.OptionMenu(
            selector_frame,
            self.video_var,
            "Video 1 - Fall",
            "Video 2 - Danger Zone",
            command=self.change_video
        )

        self.video_menu.config(
            font=("Arial", 9, "bold"),
            bg="#FFFFFF",
            fg="#172033",
            activebackground="#E2E8F0"
        )

        self.video_menu.pack(
            side="left"
        )


        # ====================================================
        # VIDEO DISPLAY
        # ====================================================

        self.camera_label = tk.Label(
            camera_frame,
            text="Camera is not running",
            font=("Arial", 14, "bold"),
            bg="#08101F",
            fg="#94A3B8"
        )

        self.camera_label.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8)
        )


        # ====================================================
        # RIGHT STATUS PANEL
        # ====================================================

        status_frame = tk.Frame(
            self.page,
            bg="white",
            bd=1,
            relief="solid",
            width=265
        )

        status_frame.pack(
            side="right",
            fill="y",
            padx=(6, 0)
        )

        status_frame.pack_propagate(
            False
        )


        # ====================================================
        # STATUS TITLE
        # ====================================================

        tk.Label(
            status_frame,
            text="SAFETY STATUS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=16,
            pady=(13, 12)
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

        self.temperature_status = self.status_row(
            status_frame,
            "TEMPERATURE",
            "-- °C"
        )

        self.vibration_status = self.status_row(
            status_frame,
            "VIBRATION",
            "--"
        )

        self.risk_status = self.status_row(
            status_frame,
            "RISK LEVEL",
            "LOW"
        )


        # ====================================================
        # SEPARATOR
        # ====================================================

        tk.Frame(
            status_frame,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=16,
            pady=9
        )


        # ====================================================
        # CURRENT EVENT
        # ====================================================

        tk.Label(
            status_frame,
            text="CURRENT EVENT",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=16
        )


        self.event_label = tk.Label(
            status_frame,
            text="System waiting...",
            font=("Arial", 8),
            bg="white",
            fg="#64748B",
            justify="left",
            wraplength=220
        )

        self.event_label.pack(
            anchor="w",
            padx=16,
            pady=5
        )


        # ====================================================
        # AI DETECTION
        # ====================================================

        tk.Label(
            status_frame,
            text="AI DETECTION",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=16,
            pady=(3, 0)
        )


        ai_text = (
            "YOLOv8 Person Detection\n"
            "Danger Zone Detection\n"
            "MediaPipe Pose\n"
            "MediaPipe Hands\n"
            "Fall Detection\n"
            "Isolation Forest\n"
            "Temperature Simulation\n"
            "Vibration Simulation"
        )


        tk.Label(
            status_frame,
            text=ai_text,
            font=("Arial", 7),
            bg="white",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=16,
            pady=5
        )


        # ====================================================
        # BUTTON AREA
        # ====================================================

        button_frame = tk.Frame(
            status_frame,
            bg="white"
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=13,
            pady=10
        )


        # ====================================================
        # START BUTTON
        # ====================================================

        self.start_button = tk.Button(
            button_frame,
            text="▶  START MONITORING",
            font=("Arial", 9, "bold"),
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            height=2,
            command=self.start_monitoring
        )

        self.start_button.pack(
            fill="x",
            pady=(0, 5)
        )


        # ====================================================
        # STOP BUTTON
        # ====================================================

        self.stop_button = tk.Button(
            button_frame,
            text="■  STOP MONITORING",
            font=("Arial", 9, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            height=2,
            command=self.stop_monitoring
        )

        self.stop_button.pack(
            fill="x"
        )

        self.stop_button.config(
            state="disabled"
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
            padx=16,
            pady=3
        )


        tk.Label(
            row,
            text=label,
            font=("Arial", 8),
            bg="white",
            fg="#64748B"
        ).pack(
            side="left"
        )


        value_label = tk.Label(
            row,
            text=value,
            font=("Arial", 8, "bold"),
            bg="white",
            fg="#64748B"
        )

        value_label.pack(
            side="right"
        )

        return value_label


    # ========================================================
    # CHANGE VIDEO
    # ========================================================

    def change_video(
        self,
        selected
    ):

        if selected == "Video 1 - Fall":

            self.selected_video = VIDEO_1

        elif selected == "Video 2 - Danger Zone":

            self.selected_video = VIDEO_2

        else:

            return


        print(
            "Selected video:",
            self.selected_video
        )


        if self.running:

            self.stop_monitoring()

            self.parent.after(
                200,
                self.start_monitoring
            )


    # ========================================================
    # CHECK DANGER-ZONE VIDEO
    # ========================================================

    def is_danger_zone_video(self):

        selected_name = os.path.basename(
            self.selected_video
        ).lower()

        danger_name = os.path.basename(
            VIDEO_2
        ).lower()

        return (
            selected_name == danger_name
        )


    # ========================================================
    # CONTINUOUS ALERT SOUND
    # ========================================================

    def play_alert_sound(self):

        with self.alert_sound_lock:

            # Already playing
            if (
                self.alert_sound_thread is not None
                and
                self.alert_sound_thread.is_alive()
            ):

                return


            # Reset stop event
            self.alert_sound_stop_event.clear()


            def beep_loop():

                print(
                    "🔊 CONTINUOUS ALERT SOUND STARTED"
                )

                while not self.alert_sound_stop_event.is_set():

                    try:

                        # First beep
                        winsound.Beep(
                            1000,
                            250
                        )

                        if self.alert_sound_stop_event.is_set():
                            break


                        # Small pause
                        self.alert_sound_stop_event.wait(
                            0.15
                        )


                        # Second beep
                        if not self.alert_sound_stop_event.is_set():

                            winsound.Beep(
                                1200,
                                300
                            )


                        # Pause before repeating
                        self.alert_sound_stop_event.wait(
                            0.35
                        )


                    except Exception as e:

                        print(
                            "Buzzer sound error:",
                            e
                        )

                        break


                print(
                    "🔇 ALERT SOUND STOPPED"
                )


            self.alert_sound_thread = threading.Thread(
                target=beep_loop,
                daemon=True
            )

            self.alert_sound_thread.start()


    # ========================================================
    # STOP ALERT SOUND
    # ========================================================

    def stop_alert_sound(self):

        self.alert_sound_stop_event.set()


    # ========================================================
    # SEND ALERT
    # ========================================================

    def send_alert(
        self,
        alert_type,
        message,
        source
    ):

        if self.alerts_page is None:

            print(
                "WARNING: Alerts page is not connected."
            )

            return


        try:

            self.alerts_page.add_alert(
                alert_type,
                message,
                source
            )


            print(
                "--------------------------------"
            )

            print(
                "ALERT GENERATED"
            )

            print(
                f"TYPE   : {alert_type}"
            )

            print(
                f"MESSAGE: {message}"
            )

            print(
                f"SOURCE : {source}"
            )

            print(
                "--------------------------------"
            )


        except Exception as e:

            print(
                f"Alert connection error: {e}"
            )


    # ========================================================
    # SIMULATED SENSORS
    # ========================================================

    def get_simulated_sensor_values(self):

        temperature = 65.0

        vibration = 5.0

        return temperature, vibration


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

        self.previous_fall = False

        self.previous_hand_danger = False

        self.previous_body_danger = False

        self.previous_temperature_danger = False

        self.previous_vibration_danger = False

        self.anomaly_image_saved = False

        self.danger_image_saved = False


        self.stop_alert_sound()


        # ====================================================
        # CHECK VIDEO
        # ====================================================

        if not os.path.exists(
            self.selected_video
        ):

            messagebox.showerror(
                "Video Not Found",
                (
                    "Selected video was not found:\n\n"
                    f"{self.selected_video}"
                ),
                parent=self.parent
            )

            return


        # ====================================================
        # DETERMINE VIDEO TYPE
        # ====================================================

        danger_zone_enabled = (
            self.is_danger_zone_video()
        )


        print(
            "================================"
        )

        print(
            "STARTING MONITORING"
        )

        print(
            f"VIDEO: {self.selected_video}"
        )

        print(
            f"DANGER ZONE: {danger_zone_enabled}"
        )

        print(
            "================================"
        )


        # ====================================================
        # LOAD YOLO
        # ====================================================

        try:

            self.detector = YOLODetector(
                enable_danger_zone=danger_zone_enabled
            )

        except Exception as e:

            self.detector = None

            messagebox.showerror(
                "YOLO Error",
                str(e),
                parent=self.parent
            )

            return


        # ====================================================
        # LOAD ANOMALY DETECTOR
        # ====================================================

        if AnomalyDetector:

            try:

                self.anomaly_detector = (
                    AnomalyDetector()
                )

            except Exception as e:

                print(
                    f"Anomaly detector error: {e}"
                )

                self.anomaly_detector = None


        # ====================================================
        # OPEN VIDEO
        # ====================================================

        self.camera = cv2.VideoCapture(
            self.selected_video
        )

        self.using_video = True


        if not self.camera.isOpened():

            messagebox.showerror(
                "Video Error",
                (
                    "Unable to open selected video:\n\n"
                    f"{self.selected_video}"
                ),
                parent=self.parent
            )

            self.camera.release()

            self.camera = None

            if self.detector:

                try:

                    self.detector.release()

                except Exception:

                    pass

            self.detector = None

            return


        # ====================================================
        # RESET VIDEO
        # ====================================================

        self.camera.set(
            cv2.CAP_PROP_POS_FRAMES,
            0
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

        self.stop_button.config(
            state="normal"
        )


        if danger_zone_enabled:

            event_text = (
                "Monitoring:\n"
                "Danger-zone monitoring enabled."
            )

        else:

            event_text = (
                "Monitoring:\n"
                "Fall monitoring enabled."
            )


        self.event_label.config(
            text=event_text
        )


        self.update_camera()


    # ========================================================
    # UPDATE CAMERA
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

            print(
                "Video reached end. Restarting..."
            )

            self.camera.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )

            success, frame = self.camera.read()


            if not success:

                self.stop_monitoring()

                return


        # ====================================================
        # YOLO
        # ====================================================

        try:

            processed_frame, result = (
                self.detector.process_frame(
                    frame
                )
            )

        except Exception as e:

            print(
                f"Detection error: {e}"
            )

            self.parent.after(
                100,
                self.update_camera
            )

            return


        # ====================================================
        # RESULTS
        # ====================================================

        worker = bool(
            result.get(
                "worker",
                False
            )
        )


        danger = bool(
            result.get(
                "danger",
                False
            )
        )


        fall = bool(
            result.get(
                "fall",
                False
            )
        )


        hand_danger = bool(
            result.get(
                "hand_danger",
                False
            )
        )


        body_danger = bool(
            result.get(
                "body_danger",
                False
            )
        )


        status = result.get(
            "status",
            "NO WORKER"
        )


        pose_landmarks = result.get(
            "pose_landmarks",
            None
        )


        # ====================================================
        # ANOMALY DETECTION
        # ====================================================

        anomaly = False

        anomaly_state = "NO POSE"


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


                anomaly = bool(
                    anomaly_result.get(
                        "anomaly",
                        False
                    )
                )


                anomaly_state = (
                    anomaly_result.get(
                        "status",
                        "NO POSE"
                    )
                )


            except Exception as e:

                print(
                    "Anomaly detection error:",
                    e
                )

                anomaly = False

                anomaly_state = "ERROR"


        # ====================================================
        # SIMULATED SENSORS
        # ====================================================

        self.temperature, self.vibration = (
            self.get_simulated_sensor_values()
        )


        temperature_danger = (
            self.temperature >= TEMPERATURE_THRESHOLD
        )


        vibration_danger = (
            self.vibration >= VIBRATION_THRESHOLD
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

        if body_danger:

            self.danger_status.config(
                text="BODY DANGER",
                fg="#DC2626"
            )

        elif hand_danger:

            self.danger_status.config(
                text="HAND DANGER",
                fg="#DC2626"
            )

        elif danger:

            self.danger_status.config(
                text="DANGER",
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
        # TEMPERATURE
        # ====================================================

        if temperature_danger:

            self.temperature_status.config(
                text=f"{self.temperature:.1f} °C",
                fg="#DC2626"
            )

        else:

            self.temperature_status.config(
                text=f"{self.temperature:.1f} °C",
                fg="#16A34A"
            )


        # ====================================================
        # VIBRATION
        # ====================================================

        if vibration_danger:

            self.vibration_status.config(
                text=f"{self.vibration:.1f}",
                fg="#DC2626"
            )

        else:

            self.vibration_status.config(
                text=f"{self.vibration:.1f}",
                fg="#16A34A"
            )


        # ====================================================
        # OVERALL HAZARD
        # ====================================================

        hazard_detected = (
            fall
            or
            danger
            or
            hand_danger
            or
            body_danger
            or
            anomaly
            or
            temperature_danger
            or
            vibration_danger
        )


        # ====================================================
        # CONTINUOUS BEEP
        # ====================================================

        if hazard_detected:

            self.play_alert_sound()

        else:

            self.stop_alert_sound()


        # ====================================================
        # RISK LEVEL
        # ====================================================

        if hazard_detected:

            risk_level = "HIGH"

            risk_color = "#DC2626"

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

        if fall:

            alert_message = (
                "🚨 WORKER FALL DETECTED"
            )

        elif body_danger:

            alert_message = (
                "🚨 WORKER ENTERED DANGER ZONE"
            )

        elif hand_danger:

            alert_message = (
                "🚨 WORKER HAND ENTERED DANGER ZONE"
            )

        elif danger:

            alert_message = (
                "🚨 DANGER-ZONE VIOLATION"
            )

        elif temperature_danger:

            alert_message = (
                "🚨 HIGH TEMPERATURE DETECTED"
            )

        elif vibration_danger:

            alert_message = (
                "🚨 HIGH VIBRATION DETECTED"
            )

        elif anomaly:

            alert_message = (
                "🚨 INDUSTRIAL ANOMALY DETECTED"
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
        # FALL ALERT
        # ====================================================

        if (
            fall
            and
            not self.previous_fall
        ):

            self.send_alert(
                "CRITICAL",
                "Worker fall detected",
                "MediaPipe Fall Detection"
            )


        # ====================================================
        # DANGER ALERT
        # ====================================================

        if (
            danger
            and
            not self.previous_danger
        ):

            self.send_alert(
                "HIGH RISK",
                "Worker entered danger zone",
                "YOLOv8 + Danger Zone Detection"
            )


        # ====================================================
        # HAND DANGER ALERT
        # ====================================================

        if (
            hand_danger
            and
            not self.previous_hand_danger
        ):

            self.send_alert(
                "HIGH RISK",
                "Worker hand entered danger zone",
                "MediaPipe Hands + Danger Zone"
            )


        # ====================================================
        # BODY DANGER ALERT
        # ====================================================

        if (
            body_danger
            and
            not self.previous_body_danger
        ):

            self.send_alert(
                "HIGH RISK",
                "Worker entered danger zone",
                "YOLOv8 + Danger Zone Detection"
            )


        # ====================================================
        # TEMPERATURE ALERT
        # ====================================================

        if (
            temperature_danger
            and
            not self.previous_temperature_danger
        ):

            self.send_alert(
                "CRITICAL",
                (
                    f"High temperature detected: "
                    f"{self.temperature:.1f} °C"
                ),
                "Simulated Temperature Sensor"
            )


        # ====================================================
        # VIBRATION ALERT
        # ====================================================

        if (
            vibration_danger
            and
            not self.previous_vibration_danger
        ):

            self.send_alert(
                "CRITICAL",
                (
                    f"High vibration detected: "
                    f"{self.vibration:.1f}"
                ),
                "Simulated Vibration Sensor"
            )


        # ====================================================
        # ANOMALY ALERT
        # ====================================================

        if (
            anomaly
            and
            not self.previous_anomaly
        ):

            self.send_alert(
                "CRITICAL",
                "Industrial anomaly detected",
                "Isolation Forest"
            )


        # ====================================================
        # SAVE DANGER IMAGE
        # ====================================================

        if (
            danger
            and
            not self.previous_danger
        ):

            try:

                cv2.imwrite(
                    LATEST_DANGER_IMAGE,
                    processed_frame
                )

                self.danger_image_saved = True

            except Exception as e:

                print(
                    f"Danger image error: {e}"
                )


        # ====================================================
        # SAVE ANOMALY IMAGE
        # ====================================================

        if (
            anomaly
            and
            not self.previous_anomaly
        ):

            try:

                cv2.imwrite(
                    LATEST_ANOMALY_IMAGE,
                    processed_frame
                )

                self.anomaly_image_saved = True

            except Exception as e:

                print(
                    f"Anomaly image error: {e}"
                )


        # ====================================================
        # PREVIOUS STATES
        # ====================================================

        self.previous_anomaly = anomaly

        self.previous_danger = danger

        self.previous_fall = fall

        self.previous_hand_danger = hand_danger

        self.previous_body_danger = body_danger

        self.previous_temperature_danger = temperature_danger

        self.previous_vibration_danger = vibration_danger


        # ====================================================
        # ANOMALY VIDEO TEXT
        # ====================================================

        if anomaly:

            cv2.putText(
                processed_frame,
                "INDUSTRIAL ANOMALY DETECTED",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 0, 255),
                3
            )

        elif anomaly_state == "LEARNING":

            cv2.putText(
                processed_frame,
                "ANOMALY MODEL: LEARNING",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (0, 255, 255),
                2
            )

        elif anomaly_state == "NORMAL":

            cv2.putText(
                processed_frame,
                "INDUSTRIAL ACTIVITY: NORMAL",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (0, 180, 0),
                2
            )


        # ====================================================
        # SENSOR DISPLAY
        # ====================================================

        temperature_color = (
            (0, 0, 255)
            if temperature_danger
            else
            (0, 180, 0)
        )


        vibration_color = (
            (0, 0, 255)
            if vibration_danger
            else
            (0, 180, 0)
        )


        cv2.putText(
            processed_frame,
            f"TEMPERATURE: {self.temperature:.1f} C",
            (20, 190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            temperature_color,
            2
        )


        cv2.putText(
            processed_frame,
            f"VIBRATION: {self.vibration:.1f}",
            (20, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            vibration_color,
            2
        )


        # ====================================================
        # RISK DISPLAY
        # ====================================================

        risk_display_color = (
            (0, 0, 255)
            if risk_level == "HIGH"
            else
            (0, 180, 0)
        )


        cv2.putText(
            processed_frame,
            f"RISK LEVEL: {risk_level}",
            (20, 255),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            risk_display_color,
            2
        )


        # ====================================================
        # ALERT DISPLAY
        # ====================================================

        if hazard_detected:

            cv2.putText(
                processed_frame,
                "!!! SAFETY ALERT !!!",
                (20, 290),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 0, 255),
                3
            )


        # ====================================================
        # SAVE LATEST IMAGE
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
        # LATEST JSON
        # ====================================================

        latest_data = {

            "system":
                "ONLINE",

            "video":
                os.path.basename(
                    self.selected_video
                ),

            "danger_zone_enabled":
                self.is_danger_zone_video(),

            "worker":
                worker,

            "danger":
                danger,

            "hand_danger":
                hand_danger,

            "body_danger":
                body_danger,

            "fall":
                fall,

            "anomaly":
                anomaly,

            "anomaly_status":
                anomaly_state,

            "temperature":
                self.temperature,

            "temperature_threshold":
                TEMPERATURE_THRESHOLD,

            "temperature_danger":
                temperature_danger,

            "vibration":
                self.vibration,

            "vibration_threshold":
                VIBRATION_THRESHOLD,

            "vibration_danger":
                vibration_danger,

            "hazard_detected":
                hazard_detected,

            "risk_level":
                risk_level,

            "status":
                status,

            "message":
                alert_message,

            "latest_danger_image":
                (
                    LATEST_DANGER_IMAGE
                    if self.danger_image_saved
                    else ""
                ),

            "latest_anomaly_image":
                (
                    LATEST_ANOMALY_IMAGE
                    if self.anomaly_image_saved
                    else ""
                ),

            "time":
                datetime.now().strftime(
                    "%d-%m-%Y %I:%M:%S %p"
                )
        }


        # ====================================================
        # INCIDENT MANAGER
        # ====================================================

        if self.incident_manager:

            try:

                self.incident_manager.process_status(
                    latest_data
                )

            except Exception as e:

                print(
                    f"Incident manager error: {e}"
                )


        # ====================================================
        # SAVE JSON
        # ====================================================

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

        rgb_frame = cv2.cvtColor(
            processed_frame,
            cv2.COLOR_BGR2RGB
        )


        image = Image.fromarray(
            rgb_frame
        )


        # Smaller display so the status panel/buttons
        # remain visible.

        DISPLAY_WIDTH = 640

        DISPLAY_HEIGHT = 390


        image.thumbnail(
            (
                DISPLAY_WIDTH,
                DISPLAY_HEIGHT
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


        self.camera_label.image = (
            self.photo
        )


        # ====================================================
        # NEXT FRAME
        # ====================================================

        if self.running:

            self.parent.after(
                30,
                self.update_camera
            )


    # ========================================================
    # STOP MONITORING
    # ========================================================

    def stop_monitoring(self):

        print(
            "Stopping monitoring..."
        )


        self.running = False


        # ====================================================
        # STOP CONTINUOUS BEEP
        # ====================================================

        self.stop_alert_sound()


        # ====================================================
        # CAMERA
        # ====================================================

        if self.camera is not None:

            try:

                self.camera.release()

            except Exception:

                pass

            self.camera = None


        # ====================================================
        # YOLO
        # ====================================================

        if self.detector is not None:

            try:

                self.detector.release()

            except Exception:

                pass

            self.detector = None


        # ====================================================
        # ANOMALY
        # ====================================================

        if self.anomaly_detector is not None:

            try:

                if hasattr(
                    self.anomaly_detector,
                    "reset"
                ):

                    self.anomaly_detector.reset()

            except Exception as e:

                print(
                    f"Anomaly reset error: {e}"
                )

            self.anomaly_detector = None


        # ====================================================
        # RESET STATES
        # ====================================================

        self.previous_anomaly = False

        self.previous_danger = False

        self.previous_fall = False

        self.previous_hand_danger = False

        self.previous_body_danger = False

        self.previous_temperature_danger = False

        self.previous_vibration_danger = False


        # ====================================================
        # SENSOR VALUES
        # ====================================================

        self.temperature = 0.0

        self.vibration = 0.0


        # ====================================================
        # IMAGE
        # ====================================================

        self.photo = None


        self.camera_label.config(
            image="",
            text="Camera is not running"
        )

        self.camera_label.image = None


        # ====================================================
        # STATUS
        # ====================================================

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


        self.temperature_status.config(
            text="-- °C",
            fg="#64748B"
        )


        self.vibration_status.config(
            text="--",
            fg="#64748B"
        )


        self.risk_status.config(
            text="LOW",
            fg="#16A34A"
        )


        self.event_label.config(
            text="System waiting..."
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        self.start_button.config(
            state="normal"
        )

        self.stop_button.config(
            state="disabled"
        )


        print(
            "Monitoring stopped."
        )


    # ========================================================
    # DESTROY
    # ========================================================

    def destroy(self):

        self.stop_monitoring()

        try:

            if self.page.winfo_exists():

                self.page.destroy()

        except Exception:

            pass