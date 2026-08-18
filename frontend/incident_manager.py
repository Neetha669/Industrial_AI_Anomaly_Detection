import json
import os
from datetime import datetime


CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    CURRENT_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


class IncidentManager:

    def __init__(self):

        self.status_file = os.path.join(
            DATA_DIR,
            "latest_status.json"
        )

        self.incident_file = os.path.join(
            DATA_DIR,
            "incident_logs.json"
        )

        self.logs = []

        self.previous_status = {
            "worker": False,
            "danger": False,
            "hand_danger": False,
            "body_danger": False,
            "fall": False,
            "anomaly": False
        }

        self.load_logs()

    # ==================================================
    # LOAD INCIDENT LOGS
    # ==================================================

    def load_logs(self):

        if not os.path.exists(self.incident_file):

            self.logs = []

            return

        try:

            with open(
                self.incident_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):

                    self.logs = data

                else:

                    self.logs = []

        except Exception:

            self.logs = []

    # ==================================================
    # SAVE INCIDENT LOGS
    # ==================================================

    def save_logs(self):

        try:

            with open(
                self.incident_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.logs,
                    file,
                    indent=4
                )

        except Exception as error:

            print(
                "Unable to save incident logs:",
                error
            )

    # ==================================================
    # READ LATEST STATUS
    # ==================================================

    def read_status(self):

        if not os.path.exists(self.status_file):

            return None

        try:

            with open(
                self.status_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception as error:

            print(
                "Unable to read latest status:",
                error
            )

            return None

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

            "date": now.strftime(
                "%d-%m-%Y"
            ),

            "time": now.strftime(
                "%H:%M:%S"
            ),

            "type": incident_type,

            "description": description,

            "source": source,

            "status": status
        }

        # Newest incident first
        self.logs.insert(
            0,
            incident
        )

        self.save_logs()

        print(
            "INCIDENT:",
            incident_type,
            "-",
            description
        )

        return incident

    # ==================================================
    # PROCESS LATEST STATUS
    # ==================================================

    def process_status(self, status_data=None):

        if status_data is None:

            status_data = self.read_status()

        if not status_data:

            return []

        new_incidents = []

        # --------------------------------------------------
        # FALL DETECTION
        # --------------------------------------------------

        fall = status_data.get(
            "fall",
            False
        )

        if fall and not self.previous_status["fall"]:

            incident = self.add_incident(

                "FALL",

                "Worker fall detected by AI pose analysis.",

                "AI Fall Detection",

                "OPEN"
            )

            new_incidents.append(
                incident
            )

        # --------------------------------------------------
        # DANGER ZONE
        # --------------------------------------------------

        danger = status_data.get(
            "danger",
            False
        )

        if danger and not self.previous_status["danger"]:

            incident = self.add_incident(

                "DANGER ZONE",

                "Worker detected inside restricted danger zone.",

                "AI Danger Zone Detection",

                "OPEN"
            )

            new_incidents.append(
                incident
            )

        # --------------------------------------------------
        # HAND DANGER
        # --------------------------------------------------

        hand_danger = status_data.get(
            "hand_danger",
            False
        )

        if hand_danger and not self.previous_status["hand_danger"]:

            incident = self.add_incident(

                "DANGER ZONE",

                "Hand detected inside dangerous area.",

                "AI Hand Danger Detection",

                "OPEN"
            )

            new_incidents.append(
                incident
            )

        # --------------------------------------------------
        # BODY DANGER
        # --------------------------------------------------

        body_danger = status_data.get(
            "body_danger",
            False
        )

        if body_danger and not self.previous_status["body_danger"]:

            incident = self.add_incident(

                "DANGER ZONE",

                "Worker body detected in dangerous area.",

                "AI Body Danger Detection",

                "OPEN"
            )

            new_incidents.append(
                incident
            )

        # --------------------------------------------------
        # SENSOR / ANOMALY
        # --------------------------------------------------

        anomaly = status_data.get(
            "anomaly",
            False
        )

        if anomaly and not self.previous_status["anomaly"]:

            anomaly_status = status_data.get(
                "anomaly_status",
                "Abnormal sensor condition detected"
            )

            # Determine whether it is temperature
            # or vibration based on the status text.

            anomaly_text = str(
                anomaly_status
            ).upper()

            if "TEMPERATURE" in anomaly_text:

                incident_type = "TEMPERATURE"

                description = (
                    "Abnormal temperature detected "
                    "by Isolation Forest."
                )

            elif "VIBRATION" in anomaly_text:

                incident_type = "VIBRATION"

                description = (
                    "Abnormal vibration detected "
                    "by Isolation Forest."
                )

            else:

                incident_type = "VIBRATION"

                description = (
                    "Abnormal sensor condition detected "
                    "by AI anomaly detection."
                )

            incident = self.add_incident(

                incident_type,

                description,

                "Isolation Forest",

                "OPEN"
            )

            new_incidents.append(
                incident
            )

        # ==================================================
        # UPDATE PREVIOUS STATUS
        # ==================================================

        self.previous_status = {

            "worker": status_data.get(
                "worker",
                False
            ),

            "danger": danger,

            "hand_danger": hand_danger,

            "body_danger": body_danger,

            "fall": fall,

            "anomaly": anomaly
        }

        return new_incidents

    # ==================================================
    # GET ALL LOGS
    # ==================================================

    def get_logs(self):

        self.load_logs()

        return self.logs.copy()

    # ==================================================
    # GET STATISTICS
    # ==================================================

    def get_statistics(self):

        logs = self.get_logs()

        total = len(logs)

        critical = 0
        falls = 0
        danger = 0
        sensor = 0

        for log in logs:

            incident_type = log.get(
                "type",
                ""
            )

            if incident_type == "FALL":

                falls += 1

                critical += 1

            elif incident_type == "DANGER ZONE":

                danger += 1

                critical += 1

            elif incident_type in [
                "TEMPERATURE",
                "VIBRATION"
            ]:

                sensor += 1

        return {

            "total": total,

            "critical": critical,

            "falls": falls,

            "danger": danger,

            "sensor": sensor
        }

    # ==================================================
    # CLEAR ALL LOGS
    # ==================================================

    def clear_logs(self):

        self.logs = []

        self.save_logs()

    # ==================================================
    # CHECK STATUS AND CREATE INCIDENTS
    # ==================================================

    def check_for_incidents(self):

        return self.process_status()
