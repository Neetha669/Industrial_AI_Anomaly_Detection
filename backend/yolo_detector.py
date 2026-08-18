import os
import cv2
import mediapipe as mp
from ultralytics import YOLO


class YOLODetector:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, model_path=None):

        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        project_root = os.path.dirname(
            current_dir
        )

        # ======================================================
        # YOLO MODEL PATH
        # ======================================================

        if model_path is None:

            model_path = os.path.join(
                project_root,
                "models",
                "yolov8n.pt"
            )

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"YOLO model not found:\n{model_path}"
            )

        print("Loading YOLO model...")

        self.model = YOLO(
            model_path
        )

        print("YOLO model loaded.")

        # ======================================================
        # MEDIAPIPE POSE
        # ======================================================

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # ======================================================
        # MEDIAPIPE HANDS
        # ======================================================

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # ======================================================
        # DRAWING
        # ======================================================

        self.mp_draw = (
            mp.solutions.drawing_utils
        )

        # ======================================================
        # STATUS
        # ======================================================

        self.worker_detected = False
        self.danger_detected = False
        self.fall_detected = False
        self.hand_in_danger = False
        self.body_in_danger = False

        # ======================================================
        # DANGER ZONE
        # ======================================================
        #
        # These values are normalized coordinates.
        #
        # x1 = 30% of width
        # y1 = 65% of height
        # x2 = 70% of width
        # y2 = 95% of height
        #
        # You can change these later.
        #
        # ======================================================

        self.danger_zone = {

            "x1": 0.30,
            "y1": 0.65,

            "x2": 0.70,
            "y2": 0.95
        }

        # ======================================================
        # PERSON VALIDATION SETTINGS
        # ======================================================

        # Minimum number of pose landmarks that should
        # appear inside a YOLO person bounding box.

        self.minimum_pose_landmarks = 3

        # Important human body landmarks.
        #
        # These are used to verify that the detected object
        # actually looks like a human body.

        self.required_pose_landmarks = [

            self.mp_pose.PoseLandmark.NOSE,

            self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            self.mp_pose.PoseLandmark.RIGHT_SHOULDER,

            self.mp_pose.PoseLandmark.LEFT_ELBOW,
            self.mp_pose.PoseLandmark.RIGHT_ELBOW,

            self.mp_pose.PoseLandmark.LEFT_HIP,
            self.mp_pose.PoseLandmark.RIGHT_HIP,

            self.mp_pose.PoseLandmark.LEFT_KNEE,
            self.mp_pose.PoseLandmark.RIGHT_KNEE,

            self.mp_pose.PoseLandmark.LEFT_ANKLE,
            self.mp_pose.PoseLandmark.RIGHT_ANKLE
        ]

    # ==========================================================
    # GET DANGER ZONE
    # ==========================================================

    def get_danger_zone(
        self,
        width,
        height
    ):

        x1 = int(
            width *
            self.danger_zone["x1"]
        )

        y1 = int(
            height *
            self.danger_zone["y1"]
        )

        x2 = int(
            width *
            self.danger_zone["x2"]
        )

        y2 = int(
            height *
            self.danger_zone["y2"]
        )

        return (
            x1,
            y1,
            x2,
            y2
        )

    # ==========================================================
    # POINT INSIDE DANGER ZONE
    # ==========================================================

    def point_inside_zone(
        self,
        x,
        y,
        zone
    ):

        x1, y1, x2, y2 = zone

        return (
            x1 <= x <= x2
            and
            y1 <= y <= y2
        )

    # ==========================================================
    # CHECK WHETHER YOLO BOX IS REALLY A PERSON
    # ==========================================================
    #
    # This is the IMPORTANT new function.
    #
    # YOLO sometimes detects machines/robots as PERSON.
    #
    # We use MediaPipe Pose to verify the YOLO detection.
    #
    # If enough human body landmarks are found inside the
    # YOLO bounding box -> accept as person.
    #
    # Otherwise -> reject the YOLO detection.
    #
    # ==========================================================

    def is_real_person(
        self,
        box,
        pose_landmarks,
        width,
        height
    ):

        if pose_landmarks is None:

            return False

        bx1 = box["x1"]
        by1 = box["y1"]
        bx2 = box["x2"]
        by2 = box["y2"]

        valid_landmarks = 0

        # ------------------------------------------------------
        # CHECK HUMAN BODY LANDMARKS
        # ------------------------------------------------------

        for landmark_id in self.required_pose_landmarks:

            landmark = pose_landmarks[
                landmark_id
            ]

            # Ignore landmarks with very low visibility.

            if landmark.visibility < 0.35:
                continue

            lx = int(
                landmark.x * width
            )

            ly = int(
                landmark.y * height
            )

            # --------------------------------------------------
            # CHECK WHETHER LANDMARK IS INSIDE YOLO BOX
            # --------------------------------------------------

            if (
                bx1 <= lx <= bx2
                and
                by1 <= ly <= by2
            ):

                valid_landmarks += 1

        # ------------------------------------------------------
        # HUMAN CONFIRMATION
        # ------------------------------------------------------

        if (
            valid_landmarks
            >=
            self.minimum_pose_landmarks
        ):

            return True

        return False

    # ==========================================================
    # IOU
    # ==========================================================

    def calculate_iou(
        self,
        box1,
        box2
    ):

        x1 = max(
            box1["x1"],
            box2["x1"]
        )

        y1 = max(
            box1["y1"],
            box2["y1"]
        )

        x2 = min(
            box1["x2"],
            box2["x2"]
        )

        y2 = min(
            box1["y2"],
            box2["y2"]
        )

        intersection_width = max(
            0,
            x2 - x1
        )

        intersection_height = max(
            0,
            y2 - y1
        )

        intersection_area = (
            intersection_width *
            intersection_height
        )

        area1 = (
            box1["x2"] -
            box1["x1"]
        ) * (
            box1["y2"] -
            box1["y1"]
        )

        area2 = (
            box2["x2"] -
            box2["x1"]
        ) * (
            box2["y2"] -
            box2["y1"]
        )

        union_area = (
            area1 +
            area2 -
            intersection_area
        )

        if union_area <= 0:

            return 0.0

        return (
            intersection_area /
            union_area
        )

    # ==========================================================
    # REMOVE DUPLICATE PERSON BOXES
    # ==========================================================

    def remove_duplicate_boxes(
        self,
        persons
    ):

        if len(persons) <= 1:

            return persons

        persons = sorted(
            persons,
            key=lambda p: p["confidence"],
            reverse=True
        )

        filtered = []

        for person in persons:

            duplicate = False

            for existing in filtered:

                iou = self.calculate_iou(
                    person,
                    existing
                )

                if iou > 0.50:

                    duplicate = True
                    break

            if not duplicate:

                filtered.append(
                    person
                )

        return filtered

    # ==========================================================
    # PROCESS FRAME
    # ==========================================================

    def process_frame(
        self,
        frame
    ):

        if frame is None:

            return frame, {

                "worker": False,
                "danger": False,
                "fall": False,
                "hand_danger": False,
                "body_danger": False,
                "status": "OFFLINE",
                "pose_landmarks": None
            }

        # ======================================================
        # RESET
        # ======================================================

        self.worker_detected = False
        self.danger_detected = False
        self.fall_detected = False
        self.hand_in_danger = False
        self.body_in_danger = False

        # ======================================================
        # FLIP FRAME
        # ======================================================

        frame = cv2.flip(
            frame,
            1
        )

        height, width = frame.shape[:2]

        # ======================================================
        # DANGER ZONE
        # ======================================================

        danger_zone = self.get_danger_zone(
            width,
            height
        )

        # ======================================================
        # RGB FRAME FOR MEDIAPIPE
        # ======================================================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ======================================================
        # MEDIAPIPE POSE FIRST
        # ======================================================

        pose_result = self.pose.process(
            rgb
        )

        pose_landmarks = None

        if pose_result.pose_landmarks:

            pose_landmarks = (
                pose_result
                .pose_landmarks
                .landmark
            )

        # ======================================================
        # YOLO PERSON DETECTION
        # ======================================================

        results = self.model.predict(

            source=frame,

            # Slightly higher confidence helps reduce
            # false person detections.

            conf=0.60,

            iou=0.45,

            # COCO CLASS 0 = PERSON

            classes=[0],

            verbose=False
        )

        # ======================================================
        # COLLECT PERSONS
        # ======================================================

        persons = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                confidence = float(
                    box.conf[0]
                )

                class_id = int(
                    box.cls[0]
                )

                # ------------------------------------------------
                # ONLY PERSON CLASS
                # ------------------------------------------------

                if class_id != 0:
                    continue

                # ------------------------------------------------
                # CONFIDENCE
                # ------------------------------------------------

                if confidence < 0.60:
                    continue

                bx1, by1, bx2, by2 = map(
                    int,
                    box.xyxy[0]
                )

                # ------------------------------------------------
                # CLAMP COORDINATES
                # ------------------------------------------------

                bx1 = max(
                    0,
                    min(
                        bx1,
                        width - 1
                    )
                )

                by1 = max(
                    0,
                    min(
                        by1,
                        height - 1
                    )
                )

                bx2 = max(
                    0,
                    min(
                        bx2,
                        width - 1
                    )
                )

                by2 = max(
                    0,
                    min(
                        by2,
                        height - 1
                    )
                )

                if bx2 <= bx1:
                    continue

                if by2 <= by1:
                    continue

                candidate = {

                    "x1": bx1,
                    "y1": by1,
                    "x2": bx2,
                    "y2": by2,
                    "confidence": confidence
                }

                # ==================================================
                # HUMAN POSE VALIDATION
                # ==================================================
                #
                # This rejects the robot detection in your image
                # when there are not enough human landmarks.
                #
                # ==================================================

                if not self.is_real_person(
                    candidate,
                    pose_landmarks,
                    width,
                    height
                ):

                    print(
                        "False person detection rejected:",
                        confidence
                    )

                    continue

                persons.append(
                    candidate
                )

        # ======================================================
        # REMOVE DUPLICATES
        # ======================================================

        persons = self.remove_duplicate_boxes(
            persons
        )

        # ======================================================
        # WORKER FOUND
        # ======================================================

        if len(persons) > 0:

            self.worker_detected = True

        # ======================================================
        # PROCESS EACH REAL PERSON
        # ======================================================

        for person in persons:

            bx1 = person["x1"]
            by1 = person["y1"]
            bx2 = person["x2"]
            by2 = person["y2"]

            confidence = person[
                "confidence"
            ]

            # --------------------------------------------------
            # FOOT POINT
            # --------------------------------------------------

            foot_x = int(
                (bx1 + bx2) / 2
            )

            foot_y = by2

            # --------------------------------------------------
            # DANGER ZONE CHECK
            # --------------------------------------------------

            person_in_danger = (
                self.point_inside_zone(
                    foot_x,
                    foot_y,
                    danger_zone
                )
            )

            # ==================================================
            # DANGER
            # ==================================================

            if person_in_danger:

                self.danger_detected = True

                self.body_in_danger = True

                box_color = (
                    0,
                    0,
                    255
                )

                label = (
                    f"PERSON - DANGER "
                    f"{confidence:.2f}"
                )

                # ------------------------------------------------
                # DANGER ZONE BORDER
                # ------------------------------------------------

                x1, y1, x2, y2 = (
                    danger_zone
                )

                cv2.rectangle(

                    frame,

                    (x1, y1),

                    (x2, y2),

                    (0, 0, 255),

                    3
                )

                # ------------------------------------------------
                # DANGER ZONE LABEL
                # ------------------------------------------------

                cv2.putText(

                    frame,

                    "DANGER ZONE",

                    (
                        x1 + 10,
                        max(
                            30,
                            y1 - 10
                        )
                    ),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.65,

                    (0, 0, 255),

                    2
                )

                # ------------------------------------------------
                # FOOT POINT
                # ------------------------------------------------

                cv2.circle(

                    frame,

                    (
                        foot_x,
                        foot_y
                    ),

                    7,

                    (0, 0, 255),

                    -1
                )

            # ==================================================
            # SAFE
            # ==================================================

            else:

                box_color = (
                    0,
                    255,
                    0
                )

                label = (
                    f"PERSON - SAFE "
                    f"{confidence:.2f}"
                )

                cv2.circle(

                    frame,

                    (
                        foot_x,
                        foot_y
                    ),

                    6,

                    (0, 255, 0),

                    -1
                )

            # ==================================================
            # PERSON BOX
            # ==================================================

            cv2.rectangle(

                frame,

                (
                    bx1,
                    by1
                ),

                (
                    bx2,
                    by2
                ),

                box_color,

                3
            )

            # ==================================================
            # PERSON LABEL
            # ==================================================

            cv2.putText(

                frame,

                label,

                (
                    bx1,
                    max(
                        30,
                        by1 - 10
                    )
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.65,

                box_color,

                2
            )

        # ======================================================
        # DRAW POSE
        # ======================================================

        if pose_result.pose_landmarks:

            self.mp_draw.draw_landmarks(

                frame,

                pose_result.pose_landmarks,

                self.mp_pose.POSE_CONNECTIONS
            )

            # ==================================================
            # FALL DETECTION
            # ==================================================

            landmarks = (
                pose_result
                .pose_landmarks
                .landmark
            )

            left_shoulder = landmarks[
                self.mp_pose.PoseLandmark.LEFT_SHOULDER
            ]

            right_shoulder = landmarks[
                self.mp_pose.PoseLandmark.RIGHT_SHOULDER
            ]

            left_hip = landmarks[
                self.mp_pose.PoseLandmark.LEFT_HIP
            ]

            right_hip = landmarks[
                self.mp_pose.PoseLandmark.RIGHT_HIP
            ]

            if (

                left_shoulder.visibility > 0.4

                and

                right_shoulder.visibility > 0.4

                and

                left_hip.visibility > 0.4

                and

                right_hip.visibility > 0.4

            ):

                shoulder_y = (

                    left_shoulder.y
                    +
                    right_shoulder.y

                ) / 2

                hip_y = (

                    left_hip.y
                    +
                    right_hip.y

                ) / 2

                shoulder_x = (

                    left_shoulder.x
                    +
                    right_shoulder.x

                ) / 2

                hip_x = (

                    left_hip.x
                    +
                    right_hip.x

                ) / 2

                vertical_difference = abs(

                    hip_y
                    -
                    shoulder_y
                )

                horizontal_difference = abs(

                    hip_x
                    -
                    shoulder_x
                )

                if (

                    horizontal_difference
                    >
                    vertical_difference * 1.5

                ):

                    self.fall_detected = True

        # ======================================================
        # HAND DETECTION
        # ======================================================

        hand_result = self.hands.process(
            rgb
        )

        if hand_result.multi_hand_landmarks:

            for hand_landmarks in (
                hand_result.multi_hand_landmarks
            ):

                self.mp_draw.draw_landmarks(

                    frame,

                    hand_landmarks,

                    self.mp_hands.HAND_CONNECTIONS
                )

                # ----------------------------------------------
                # CHECK HAND POINTS
                # ----------------------------------------------

                for landmark in (
                    hand_landmarks.landmark
                ):

                    hx = int(
                        landmark.x *
                        width
                    )

                    hy = int(
                        landmark.y *
                        height
                    )

                    if self.point_inside_zone(

                        hx,
                        hy,
                        danger_zone
                    ):

                        self.hand_in_danger = True

                        self.danger_detected = True

        # ======================================================
        # STATUS
        # ======================================================

        if self.fall_detected:

            status = (
                "FALL DETECTED"
            )

            status_color = (
                0,
                0,
                255
            )

        elif self.danger_detected:

            status = (
                "DANGER ZONE VIOLATION"
            )

            status_color = (
                0,
                0,
                255
            )

        elif self.worker_detected:

            status = "SAFE"

            status_color = (
                0,
                180,
                0
            )

        else:

            status = "NO WORKER"

            status_color = (
                0,
                165,
                255
            )

        # ======================================================
        # STATUS TEXT
        # ======================================================

        cv2.putText(

            frame,

            f"STATUS: {status}",

            (
                25,
                45
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.9,

            status_color,

            3
        )

        # ======================================================
        # ALERT TEXT
        # ======================================================

        if self.fall_detected:

            cv2.putText(

                frame,

                "FALL DETECTED",

                (
                    25,
                    85
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 0, 255),

                3
            )

        elif self.hand_in_danger:

            cv2.putText(

                frame,

                "HAND IN DANGER ZONE",

                (
                    25,
                    85
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 0, 255),

                3
            )

        elif self.body_in_danger:

            cv2.putText(

                frame,

                "WORKER IN DANGER ZONE",

                (
                    25,
                    85
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 0, 255),

                3
            )

        # ======================================================
        # RETURN
        # ======================================================

        return frame, {

            "worker":
                self.worker_detected,

            "danger":
                self.danger_detected,

            "fall":
                self.fall_detected,

            "hand_danger":
                self.hand_in_danger,

            "body_danger":
                self.body_in_danger,

            "status":
                status,

            "pose_landmarks":
                pose_landmarks
        }

    # ==========================================================
    # RELEASE
    # ==========================================================

    def release(self):

        if self.pose is not None:

            self.pose.close()

        if self.hands is not None:

            self.hands.close()