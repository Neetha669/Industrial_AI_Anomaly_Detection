import os
import cv2
from datetime import datetime


class MonitorState:

    def __init__(self):

        self.system_status = "ONLINE"
        self.worker_status = "NOT DETECTED"
        self.machine_status = "NORMAL"

        self.danger_status = "SAFE"
        self.fall_status = "NOT DETECTED"

        self.active_alerts = 0

        self.latest_incident = {
            "status": "NO INCIDENT",
            "type": "No incident recorded",
            "time": "--",
            "location": "--",
            "priority": "--"
        }

        self.recent_alerts = []

        self.latest_image = None

        os.makedirs("data", exist_ok=True)

    # ==================================================
    # UPDATE INCIDENT
    # ==================================================

    def add_incident(
        self,
        incident_type,
        location="Zone A",
        priority="HIGH",
        frame=None
    ):

        now = datetime.now()

        self.latest_incident = {
            "status": "ACTIVE",
            "type": incident_type,
            "time": now.strftime("%I:%M:%S %p"),
            "location": location,
            "priority": priority
        }

        self.active_alerts += 1

        # ----------------------------------------------
        # SAVE LATEST INCIDENT IMAGE
        # ----------------------------------------------

        if frame is not None:

            image_path = os.path.join(
                "data",
                "latest_incident.jpg"
            )

            cv2.imwrite(
                image_path,
                frame
            )

            self.latest_image = image_path

        # ----------------------------------------------
        # RECENT ALERT
        # ----------------------------------------------

        self.recent_alerts.insert(
            0,
            {
                "time": now.strftime("%I:%M:%S %p"),
                "type": incident_type,
                "location": location,
                "priority": priority,
                "status": "ACTIVE"
            }
        )

        # Keep only latest 5
        self.recent_alerts = self.recent_alerts[:5]

    # ==================================================
    # RESET ALERT
    # ==================================================

    def clear_alerts(self):

        self.active_alerts = 0

        self.latest_incident = {
            "status": "NO INCIDENT",
            "type": "No incident recorded",
            "time": "--",
            "location": "--",
            "priority": "--"
        }


# Global monitoring state
monitor_state = MonitorState()