import cv2
import mediapipe as mp


class PoseDetector:

    def __init__(self):

        # ============================================
        # POSE
        # ============================================

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.mp_draw = mp.solutions.drawing_utils

        # ============================================
        # HANDS
        # ============================================

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.hand_draw = mp.solutions.drawing_utils

    # =================================================
    # DETECT POSE + HANDS
    # =================================================

    def detect_pose(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ============================================
        # BODY POSE
        # ============================================

        pose_results = self.pose.process(rgb)

        pose_landmarks = []

        if pose_results.pose_landmarks:

            h, w, _ = frame.shape

            # Draw body skeleton
            self.mp_draw.draw_landmarks(
                frame,
                pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

            # Store 33 body landmarks
            for lm in pose_results.pose_landmarks.landmark:

                x = int(lm.x * w)
                y = int(lm.y * h)

                pose_landmarks.append(
                    (x, y)
                )

                # Draw body point
                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 255),
                    -1
                )

        # ============================================
        # HAND DETECTION
        # ============================================

        hand_results = self.hands.process(rgb)

        hand_landmarks = []

        if hand_results.multi_hand_landmarks:

            h, w, _ = frame.shape

            for hand in hand_results.multi_hand_landmarks:

                current_hand = []

                # Draw hand skeleton
                self.hand_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

                # Store 21 hand landmarks
                for lm in hand.landmark:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    current_hand.append(
                        (x, y)
                    )

                    # Draw hand point
                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (255, 255, 0),
                        -1
                    )

                hand_landmarks.append(
                    current_hand
                )

        # ============================================
        # RETURN RESULTS
        # ============================================

        return (
            frame,
            pose_landmarks,
            hand_landmarks
        )

    # =================================================
    # RELEASE
    # =================================================

    def release(self):

        self.pose.close()
        self.hands.close()


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    detector = PoseDetector()

    while True:

        success, frame = cap.read()

        if not success:
            break

        (
            frame,
            pose_landmarks,
            hand_landmarks
        ) = detector.detect_pose(frame)

        # Count hands
        number_of_hands = len(hand_landmarks)

        # Count body points
        number_of_body_points = len(
            pose_landmarks
        )

        cv2.putText(
            frame,
            f"Body Keypoints : {number_of_body_points}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Hands Detected : {number_of_hands}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.imshow(
            "Pose + Hand Detection",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    detector.release()

    cap.release()

    cv2.destroyAllWindows()