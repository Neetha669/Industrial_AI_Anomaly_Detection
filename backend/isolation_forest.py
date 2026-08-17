import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os


class IsolationForestDetector:

    def __init__(self):

        self.model = None

        # Model path
        self.model_path = "models/isolation_forest.pkl"

    # -----------------------------
    # Train Model
    # -----------------------------
    def train(self, csv_file):

        data = pd.read_csv(csv_file)

        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )

        self.model.fit(data)

        os.makedirs("models", exist_ok=True)

        joblib.dump(self.model, self.model_path)

        print("Isolation Forest Model Trained Successfully!")

    # -----------------------------
    # Load Saved Model
    # -----------------------------
    def load_model(self):

        self.model = joblib.load(self.model_path)

    # -----------------------------
    # Predict
    # -----------------------------
    def predict(self, temperature, vibration):

        sample = [[temperature, vibration]]

        result = self.model.predict(sample)

        if result[0] == -1:
            return "ANOMALY"

        return "NORMAL"


if __name__ == "__main__":

    detector = IsolationForestDetector()

    detector.train("backend/sensor_data.csv")

    detector.load_model()

    print(detector.predict(30,0))
    print(detector.predict(31,1))
    print(detector.predict(65,1))