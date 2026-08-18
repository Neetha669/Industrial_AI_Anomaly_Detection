import os
import json
from datetime import datetime


class IncidentManager:

    def __init__(self):

        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        project_root = os.path.dirname(
            current_dir
        )

        data_dir = os.path.join(
            project_root,
            "data"
        )

        os.makedirs(
            data_dir,
            exist_ok=True
        )

        self.incident_file = os.path.join(
            data_dir,
            "incident_history.json"
        )

        # Previous states
        self.previous_states = {
            "fall": False,
            "body_danger": False,
            "hand_danger": False,
            "danger": False,
            "anomaly": False
        }

        self.create_file_if_needed()

    # ==================================================
    # CREATE FILE
    # ==================================================

    def create_file_if_needed(self):

        if not os.path.exists(
            self.incident_file
        ):

            try:

                with open(
                    self.incident_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        [],
                        file,
                        indent=4
                    )

            except Exception as e:

                print(
                    "Incident file creation error:",
                    e
                )

    # ==================================================
    # LOAD INCIDENTS
    # ==================================================

    def load_incidents(self):

        try:

            with open(
                self.incident_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except Exception as e:

            print(
                "Incident history error:",
                e
            )

            return []

    # ==================================================
    # SAVE INCIDENT
    # ==================================================

    def save_incident(
        self,
        incident_type,
        description,
        source,
        status="OPEN"
    ):

        incidents = self.load_incidents()

        now = datetime.now()

        incident = {

            "date": now.strftime(
                "%d-%m-%Y"
            ),

            "time": now.strftime(
                "%I:%M:%S %p"
            ),

            "type": incident_type,

            "description": description,

            "source": source,

            "status": status
        }

        # Newest incident first
        incidents.insert(
            0,
            incident
        )

        try:

            with open(
                self.incident_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    incidents,
                    file,
                    indent=4
                )

            print(
                "================================"
            )

            print(
                "INCIDENT SAVED"
            )

            print(
                f"TYPE       : {incident_type}"
            )

            print(
                f"DESCRIPTION: {description}"
            )

            print(
                f"SOURCE     : {source}"
            )

            print(
                f"STATUS     : {status}"
            )

            print(
                f"TIME       : {incident['date']} "
                f"{incident['time']}"
            )

            print(
                "================================"
            )

        except Exception as e:

            print(
                "Incident save error:",
                e
            )

    # ==================================================
    # PROCESS MONITORING STATUS
    # ==================================================

    def process_status(
        self,
        data
    ):

        # ------------------------------------------------
        # GET CURRENT STATES
        # ------------------------------------------------

        fall = bool(
            data.get(
                "fall",
                False
            )
        )

        danger = bool(
            data.get(
                "danger",
                False
            )
        )

        hand_danger = bool(
            data.get(
                "hand_danger",
                False
            )
        )

        body_danger = bool(
            data.get(
                "body_danger",
                False
            )
        )

        anomaly = bool(
            data.get(
                "anomaly",
                False
            )
        )

        # ==================================================
        # FALL
        # ==================================================

        if (
            fall
            and
            not self.previous_states["fall"]
        ):

            self.save_incident(

                "FALL",

                "Worker fall detected",

                "Fall Detection",

                "CRITICAL"
            )

        # ==================================================
        # BODY DANGER
        # ==================================================

        if (
            body_danger
            and
            not self.previous_states["body_danger"]
        ):

            self.save_incident(

                "DANGER ZONE",

                "Worker entered danger zone",

                "YOLOv8 + Danger Zone Detection",

                "CRITICAL"
            )

        # ==================================================
        # HAND DANGER
        # ==================================================

        if (
            hand_danger
            and
            not self.previous_states["hand_danger"]
        ):

            self.save_incident(

                "DANGER ZONE",

                "Worker hand entered danger zone",

                "MediaPipe + Danger Zone Detection",

                "HIGH"
            )

        # ==================================================
        # GENERAL DANGER
        # ==================================================

        if (
            danger
            and
            not hand_danger
            and
            not body_danger
            and
            not self.previous_states["danger"]
        ):

            self.save_incident(

                "DANGER ZONE",

                "Worker detected inside danger zone",

                "YOLOv8 Danger Zone Detection",

                "HIGH"
            )

        # ==================================================
        # ANOMALY
        # ==================================================

        if (
            anomaly
            and
            not self.previous_states["anomaly"]
        ):

            self.save_incident(

                "ANOMALY",

                "Industrial anomaly detected",

                "Isolation Forest Anomaly Detection",

                "WARNING"
            )

        # ==================================================
        # UPDATE PREVIOUS STATES
        # ==================================================

        self.previous_states["fall"] = fall

        self.previous_states["body_danger"] = body_danger

        self.previous_states["hand_danger"] = hand_danger

        self.previous_states["danger"] = danger

        self.previous_states["anomaly"] = anomaly

    # ==================================================
    # RESET STATES
    # ==================================================

    def reset_states(self):

        self.previous_states = {

            "fall": False,

            "body_danger": False,

            "hand_danger": False,

            "danger": False,

            "anomaly": False
        }

        print(
            "Incident manager states reset."
        )

    # ==================================================
    # GET INCIDENTS
    # ==================================================

    def get_incidents(self):

        return self.load_incidents()

    # ==================================================
    # CLEAR INCIDENTS
    # ==================================================

    def clear_incidents(self):

        try:

            with open(
                self.incident_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

            self.reset_states()

            print(
                "Incident history cleared."
            )

        except Exception as e:

            print(
                "Clear incident error:",
                e
            )