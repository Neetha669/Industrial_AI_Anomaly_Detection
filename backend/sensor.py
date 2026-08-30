# ============================================================
# SENSOR MODULE
# Software Simulation - NO HARDWARE REQUIRED
# ============================================================

import random
import time


class SimulatedSensors:

    def __init__(self):

        # Normal starting values
        self.temperature = 32.0
        self.vibration = 2.0

        # Thresholds
        self.temperature_warning = 38.0
        self.temperature_danger = 42.0

        self.vibration_warning = 5.0
        self.vibration_danger = 8.0

        # Simulation mode
        self.simulation_enabled = True

        # Used to occasionally generate abnormal values
        self.counter = 0

    # ========================================================
    # TEMPERATURE
    # ========================================================

    def read_temperature(self):

        if not self.simulation_enabled:
            return self.temperature

        self.counter += 1

        # Mostly normal temperature
        self.temperature += random.uniform(-0.4, 0.4)

        # Keep normal range
        self.temperature = max(
            28.0,
            min(self.temperature, 45.0)
        )

        # Every 150 readings generate high temperature
        if self.counter % 150 == 0:
            self.temperature = random.uniform(40.0, 44.0)

        return round(self.temperature, 2)

    # ========================================================
    # VIBRATION
    # ========================================================

    def read_vibration(self):

        if not self.simulation_enabled:
            return self.vibration

        # Normal vibration
        self.vibration += random.uniform(-0.3, 0.3)

        self.vibration = max(
            0.5,
            min(self.vibration, 10.0)
        )

        # Occasionally generate high vibration
        if self.counter % 200 == 0:
            self.vibration = random.uniform(6.0, 9.0)

        return round(self.vibration, 2)

    # ========================================================
    # READ BOTH
    # ========================================================

    def read_all(self):

        temperature = self.read_temperature()
        vibration = self.read_vibration()

        temperature_status = self.get_temperature_status(
            temperature
        )

        vibration_status = self.get_vibration_status(
            vibration
        )

        return {
            "temperature": temperature,
            "temperature_status": temperature_status,

            "vibration": vibration,
            "vibration_status": vibration_status,

            "temperature_anomaly":
                temperature_status != "NORMAL",

            "vibration_anomaly":
                vibration_status != "NORMAL",

            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    # ========================================================
    # TEMPERATURE STATUS
    # ========================================================

    def get_temperature_status(self, temperature):

        if temperature >= self.temperature_danger:
            return "DANGER"

        elif temperature >= self.temperature_warning:
            return "WARNING"

        return "NORMAL"

    # ========================================================
    # VIBRATION STATUS
    # ========================================================

    def get_vibration_status(self, vibration):

        if vibration >= self.vibration_danger:
            return "DANGER"

        elif vibration >= self.vibration_warning:
            return "WARNING"

        return "NORMAL"


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sensors = SimulatedSensors()

    while True:

        data = sensors.read_all()

        print("--------------------------------")
        print(
            f"Temperature : "
            f"{data['temperature']} °C "
            f"({data['temperature_status']})"
        )

        print(
            f"Vibration   : "
            f"{data['vibration']} mm/s "
            f"({data['vibration_status']})"
        )

        time.sleep(1)