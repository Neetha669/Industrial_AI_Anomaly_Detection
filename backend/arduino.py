import serial
import time


class ArduinoReader:

    def __init__(self, port="COM3", baudrate=9600):
        """
        Change COM3 to your Arduino COM Port.
        Example:
        COM3
        COM4
        COM5
        """

        self.serial = serial.Serial(port, baudrate, timeout=1)

        time.sleep(2)

    def read_sensor(self):

        if self.serial.in_waiting:

            line = self.serial.readline().decode().strip()

            if line == "ERROR":
                return None

            try:

                temperature, vibration = line.split(",")

                return {
                    "temperature": float(temperature),
                    "vibration": int(vibration)
                }

            except:
                return None

        return None

    def close(self):
        self.serial.close()


if __name__ == "__main__":

    arduino = ArduinoReader(port="COM3")   # Change COM Port

    while True:

        data = arduino.read_sensor()

        if data:

            print("-------------------")
            print("Temperature :", data["temperature"])
            print("Vibration   :", data["vibration"])