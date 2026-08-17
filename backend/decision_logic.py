class DecisionLogic:

    def get_status(
        self,
        danger=False,
        fall=False,
        temp_anomaly=False,
        vibration_anomaly=False
    ):
        """
        Combines all safety conditions and returns
        the final system status.
        """

        # 1. Highest priority:
        # Worker is in danger zone AND has fallen
        if danger and fall:
            return "CRITICAL EMERGENCY"

        # 2. Multiple abnormal conditions
        if danger and temp_anomaly:
            return "HIGH RISK"

        if danger and vibration_anomaly:
            return "HIGH RISK"

        if fall and temp_anomaly:
            return "HIGH RISK"

        if fall and vibration_anomaly:
            return "HIGH RISK"

        # 3. Individual safety conditions
        if danger:
            return "DANGER"

        if fall:
            return "FALL DETECTED"

        if temp_anomaly:
            return "TEMPERATURE ALERT"

        if vibration_anomaly:
            return "MACHINE VIBRATION ALERT"

        # 4. No abnormal condition
        return "SAFE"


# ---------------------------------
# Test the Decision Logic
# ---------------------------------

if __name__ == "__main__":

    logic = DecisionLogic()

    print("1.", logic.get_status())

    print(
        "2.",
        logic.get_status(danger=True)
    )

    print(
        "3.",
        logic.get_status(fall=True)
    )

    print(
        "4.",
        logic.get_status(temp_anomaly=True)
    )

    print(
        "5.",
        logic.get_status(vibration_anomaly=True)
    )

    print(
        "6.",
        logic.get_status(
            danger=True,
            fall=True
        )
    )

    print(
        "7.",
        logic.get_status(
            danger=True,
            temp_anomaly=True
        )
    )