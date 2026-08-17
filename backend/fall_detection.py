import math


class FallDetector:

    def __init__(self):
        pass

    def detect_fall(self, landmarks):
        """
        Detect fall using MediaPipe Pose landmarks.

        Returns:
            True  -> Fall detected
            False -> Normal
        """

        if len(landmarks) < 33:
            return False

        # Important body points
        nose = landmarks[0]

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        left_ankle = landmarks[27]
        right_ankle = landmarks[28]

        # Shoulder center
        shoulder_x = (left_shoulder[0] + right_shoulder[0]) // 2
        shoulder_y = (left_shoulder[1] + right_shoulder[1]) // 2

        # Hip center
        hip_x = (left_hip[0] + right_hip[0]) // 2
        hip_y = (left_hip[1] + right_hip[1]) // 2

        # Ankle center
        ankle_x = (left_ankle[0] + right_ankle[0]) // 2
        ankle_y = (left_ankle[1] + right_ankle[1]) // 2

        # Body height
        body_height = abs(ankle_y - shoulder_y)

        # Body width
        body_width = abs(ankle_x - shoulder_x)

        # Simple fall condition
        if body_width > body_height:
            return True

        return False