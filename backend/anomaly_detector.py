import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )

        self.training_data = []

        self.is_trained = False

        # Number of normal frames used for learning
        self.training_frames = 100

        self.frame_count = 0

        print(
            "Anomaly Detector initialized."
        )

    # ========================================================
    # EXTRACT FEATURES
    # ========================================================

    def extract_features(
        self,
        landmarks
    ):

        if landmarks is None:
            return None

        try:

            nose = landmarks[0]

            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]

            left_elbow = landmarks[13]
            right_elbow = landmarks[14]

            left_wrist = landmarks[15]
            right_wrist = landmarks[16]

            left_hip = landmarks[23]
            right_hip = landmarks[24]

            left_knee = landmarks[25]
            right_knee = landmarks[26]

            left_ankle = landmarks[27]
            right_ankle = landmarks[28]

            features = [

                nose.x,
                nose.y,

                left_shoulder.x,
                left_shoulder.y,

                right_shoulder.x,
                right_shoulder.y,

                left_elbow.x,
                left_elbow.y,

                right_elbow.x,
                right_elbow.y,

                left_wrist.x,
                left_wrist.y,

                right_wrist.x,
                right_wrist.y,

                left_hip.x,
                left_hip.y,

                right_hip.x,
                right_hip.y,

                left_knee.x,
                left_knee.y,

                right_knee.x,
                right_knee.y,

                left_ankle.x,
                left_ankle.y,

                right_ankle.x,
                right_ankle.y
            ]

            return np.array(
                features,
                dtype=np.float32
            )

        except Exception as e:

            print(
                "Feature extraction error:",
                e
            )

            return None

    # ========================================================
    # TRAIN
    # ========================================================

    def train_step(
        self,
        features
    ):

        if features is None:
            return False

        if self.is_trained:
            return True

        self.training_data.append(
            features
        )

        self.frame_count += 1

        if (
            self.frame_count
            >=
            self.training_frames
        ):

            if len(
                self.training_data
            ) >= 20:

                X = np.array(
                    self.training_data
                )

                self.model.fit(
                    X
                )

                self.is_trained = True

                print(
                    "Isolation Forest trained successfully."
                )

                return True

        return False

    # ========================================================
    # DETECT
    # ========================================================

    def detect(
        self,
        features
    ):

        if features is None:

            return {
                "anomaly": False,
                "status": "NO POSE"
            }

        # ----------------------------------------------------
        # LEARNING
        # ----------------------------------------------------

        if not self.is_trained:

            self.train_step(
                features
            )

            return {
                "anomaly": False,
                "status": "LEARNING"
            }

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        try:

            prediction = self.model.predict(
                features.reshape(
                    1,
                    -1
                )
            )

            if prediction[0] == -1:

                return {
                    "anomaly": True,
                    "status": "ANOMALY"
                }

            return {
                "anomaly": False,
                "status": "NORMAL"
            }

        except Exception as e:

            print(
                "Anomaly prediction error:",
                e
            )

            return {
                "anomaly": False,
                "status": "ERROR"
            }

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.training_data = []

        self.frame_count = 0

        self.is_trained = False

        print(
            "Anomaly detector reset."
        )