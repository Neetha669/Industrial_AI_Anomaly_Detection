# ============================================================
# SOFTWARE ALERT / BUZZER
# NO HARDWARE REQUIRED
# ============================================================

import threading
import time

try:
    import winsound

    WINDOWS_SOUND = True

except ImportError:

    WINDOWS_SOUND = False


class AlertSound:

    def __init__(self):

        self.alert_active = False
        self.last_alert_time = 0

        # Prevent continuous sound
        self.cooldown = 3

    # ========================================================
    # BEEP
    # ========================================================

    def beep(self):

        try:

            if WINDOWS_SOUND:

                winsound.Beep(
                    1000,
                    300
                )

            else:

                print("\a")

        except Exception as e:

            print(
                "Sound error:",
                e
            )

    # ========================================================
    # DANGER ALERT
    # ========================================================

    def danger_alert(self):

        current_time = time.time()

        # Prevent sound every frame
        if (
            current_time - self.last_alert_time
            < self.cooldown
        ):
            return

        self.last_alert_time = current_time

        # Run sound separately
        thread = threading.Thread(
            target=self._danger_sound,
            daemon=True
        )

        thread.start()

    # ========================================================
    # SOUND PATTERN
    # ========================================================

    def _danger_sound(self):

        self.alert_active = True

        print("================================")
        print("🚨 SAFETY ALERT")
        print("================================")

        for _ in range(3):

            self.beep()

            time.sleep(0.2)

        self.alert_active = False

    # ========================================================
    # WARNING ALERT
    # ========================================================

    def warning_alert(self):

        current_time = time.time()

        if (
            current_time - self.last_alert_time
            < self.cooldown
        ):
            return

        self.last_alert_time = current_time

        thread = threading.Thread(
            target=self._warning_sound,
            daemon=True
        )

        thread.start()

    def _warning_sound(self):

        self.alert_active = True

        if WINDOWS_SOUND:

            try:

                winsound.Beep(
                    700,
                    200
                )

            except Exception:
                print("\a")

        else:

            print("\a")

        self.alert_active = False


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    alert = AlertSound()

    print("Testing software buzzer...")

    alert.danger_alert()

    time.sleep(5)

    alert.warning_alert()