import os
import cv2
import mediapipe as mp
from ultralytics import YOLO


class YOLODetector:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, model_path=None):

        # ------------------------------------------------------
        # PROJECT ROOT
        # ------------------------------------------------------

        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        project_root = os.path.dirname(
            current_dir
        )

        # ------------------------------------------------------
        # YOLO MODEL PATH
        # ------------------------------------------------------

        if model_path is None:

            model_path = os.path.join(
                project_root,
                "models",
                "yolov8n.pt"
            )

        print("Loading YOLO model...")

        self.model = YOLO(model_path)

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
            model_complexity=1,
            min_detection_confidence=0.4,
            min_tracking_confidence=0.4
        )

        # ======================================================
        # DRAWING
        # ======================================================

        self.mp_draw = mp.solutions.drawing_utils

        # ======================================================
        # STATUS VARIABLES
        # ======================================================

        self.worker_detected = False

        self.danger_detected = False

        self.fall_detected = False

        self.hand_in_danger = False

        self.body_in_danger = False

    # ==========================================================
    # POINT INSIDE PREDEFINED DANGER ZONE
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
    # CALCULATE IOU
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
            intersection_width
            *
            intersection_height
        )

        area1 = (
            box1["x2"] - box1["x1"]
        ) * (
            box1["y2"] - box1["y1"]
        )

        area2 = (
            box2["x2"] - box2["x1"]
        ) * (
            box2["y2"] - box2["y1"]
        )

        union_area = (
            area1
            +
            area2
            -
            intersection_area
        )

        if union_area <= 0:

            return 0.0

        return (
            intersection_area
            /
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

        # ------------------------------------------------------
        # Sort by confidence
        # ------------------------------------------------------

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

                # ------------------------------------------------
                # High overlap means duplicate
                # ------------------------------------------------

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

        # ======================================================
        # INVALID FRAME
        # ======================================================

        if frame is None:

            return frame, {

                "worker": False,

                "danger": False,

                "fall": False,

                "hand_danger": False,

                "body_danger": False,

                "status": "OFFLINE"
            }

        # ======================================================
        # RESET STATUS
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
        # PREDEFINED DANGER ZONE
        #
        # IMPORTANT:
        #
        # This is intentionally NOT drawn on every frame.
        #
        # The coordinates are configured according to the
        # fixed camera/video view.
        #
        # CHANGE THESE VALUES AFTER CHECKING YOUR VIDEO.
        # ======================================================

        zone_x1 = int(
            width * 0.35
        )

        zone_y1 = int(
            height * 0.35
        )

        zone_x2 = int(
            width * 0.75
        )

        zone_y2 = int(
            height * 0.90
        )

        danger_zone = (
            zone_x1,
            zone_y1,
            zone_x2,
            zone_y2
        )

        # ======================================================
        # YOLO PERSON DETECTION
        # ======================================================

        results = self.model.predict(

            source=frame,

            conf=0.40,

            iou=0.45,

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
                # COCO class 0 = person
                # ------------------------------------------------

                if class_id != 0:

                    continue

                if confidence < 0.40:

                    continue

                bx1, by1, bx2, by2 = map(
                    int,
                    box.xyxy[0]
                )

                # ------------------------------------------------
                # Clamp coordinates
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

                persons.append({

                    "x1": bx1,

                    "y1": by1,

                    "x2": bx2,

                    "y2": by2,

                    "confidence": confidence
                })

        # ======================================================
        # REMOVE DUPLICATE BOXES
        # ======================================================

        persons = self.remove_duplicate_boxes(
            persons
        )

        # ======================================================
        # WORKER DETECTED
        # ======================================================

        if len(persons) > 0:

            self.worker_detected = True

        # ======================================================
        # PROCESS EACH WORKER
        # ======================================================

        for person in persons:

            bx1 = person["x1"]

            by1 = person["y1"]

            bx2 = person["x2"]

            by2 = person["y2"]

            confidence = person["confidence"]

            # --------------------------------------------------
            # PERSON CENTER
            # --------------------------------------------------

            center_x = int(
                (bx1 + bx2) / 2
            )

            center_y = int(
                (by1 + by2) / 2
            )

            # --------------------------------------------------
            # BODY BOTTOM POINT
            #
            # Usually better for checking whether a worker
            # has entered a floor-level restricted area.
            # --------------------------------------------------

            bottom_x = center_x

            bottom_y = by2

            # --------------------------------------------------
            # CHECK BODY
            # --------------------------------------------------

            body_inside = (

                self.point_inside_zone(
                    center_x,
                    center_y,
                    danger_zone
                )

                or

                self.point_inside_zone(
                    bottom_x,
                    bottom_y,
                    danger_zone
                )
            )

            # --------------------------------------------------
            # DANGER
            # --------------------------------------------------

            if body_inside:

                self.body_in_danger = True

                self.danger_detected = True

            # --------------------------------------------------
            # PERSON COLOR
            # --------------------------------------------------

            if body_inside:

                box_color = (
                    0,
                    0,
                    255
                )

                label = (
                    f"PERSON - DANGER "
                    f"{confidence:.2f}"
                )

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

            # --------------------------------------------------
            # DRAW PERSON BOX
            # --------------------------------------------------

            cv2.rectangle(

                frame,

                (bx1, by1),

                (bx2, by2),

                box_color,

                3
            )

            # --------------------------------------------------
            # PERSON LABEL
            # --------------------------------------------------

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
        # MEDIAPIPE RGB
        # ======================================================

        rgb = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2RGB
        )

        # ======================================================
        # POSE DETECTION
        # ======================================================

        pose_result = self.pose.process(
            rgb
        )

        # ======================================================
        # BODY POSE
        # ======================================================

        if pose_result.pose_landmarks:

            self.mp_draw.draw_landmarks(

                frame,

                pose_result.pose_landmarks,

                self.mp_pose.POSE_CONNECTIONS
            )

            landmarks = (
                pose_result
                .pose_landmarks
                .landmark
            )

            # --------------------------------------------------
            # CHECK BODY LANDMARKS
            # --------------------------------------------------

            important_landmarks = [

                self.mp_pose.PoseLandmark.NOSE,

                self.mp_pose.PoseLandmark.LEFT_SHOULDER,

                self.mp_pose.PoseLandmark.RIGHT_SHOULDER,

                self.mp_pose.PoseLandmark.LEFT_ELBOW,

                self.mp_pose.PoseLandmark.RIGHT_ELBOW,

                self.mp_pose.PoseLandmark.LEFT_WRIST,

                self.mp_pose.PoseLandmark.RIGHT_WRIST,

                self.mp_pose.PoseLandmark.LEFT_HIP,

                self.mp_pose.PoseLandmark.RIGHT_HIP,

                self.mp_pose.PoseLandmark.LEFT_KNEE,

                self.mp_pose.PoseLandmark.RIGHT_KNEE,

                self.mp_pose.PoseLandmark.LEFT_ANKLE,

                self.mp_pose.PoseLandmark.RIGHT_ANKLE
            ]

            for landmark_id in important_landmarks:

                landmark = landmarks[
                    landmark_id
                ]

                if landmark.visibility < 0.4:

                    continue

                lx = int(
                    landmark.x * width
                )

                ly = int(
                    landmark.y * height
                )

                if self.point_inside_zone(

                    lx,

                    ly,

                    danger_zone
                ):

                    self.body_in_danger = True

                    self.danger_detected = True

        # ======================================================
        # MEDIAPIPE HANDS
        # ======================================================

        hand_result = self.hands.process(
            rgb
        )

        if hand_result.multi_hand_landmarks:

            for hand_landmarks in (
                hand_result.multi_hand_landmarks
            ):

                # ------------------------------------------------
                # DRAW HAND
                # ------------------------------------------------

                self.mp_draw.draw_landmarks(

                    frame,

                    hand_landmarks,

                    self.mp_hands.HAND_CONNECTIONS
                )

                # ------------------------------------------------
                # CHECK HAND LANDMARKS
                # ------------------------------------------------

                for landmark in (
                    hand_landmarks.landmark
                ):

                    hx = int(
                        landmark.x * width
                    )

                    hy = int(
                        landmark.y * height
                    )

                    # ------------------------------------------------
                    # Small hand point
                    # ------------------------------------------------

                    cv2.circle(

                        frame,

                        (hx, hy),

                        3,

                        (255, 255, 0),

                        -1
                    )

                    # ------------------------------------------------
                    # HAND IN DANGER ZONE
                    # ------------------------------------------------

                    if self.point_inside_zone(

                        hx,

                        hy,

                        danger_zone
                    ):

                        self.hand_in_danger = True

                        self.danger_detected = True

        # ======================================================
        # FALL DETECTION
        # ======================================================

        if pose_result.pose_landmarks:

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
        # SHOW DANGER ZONE ONLY WHEN VIOLATION OCCURS
        # ======================================================

        if self.danger_detected:

            # --------------------------------------------------
            # Red danger-zone rectangle
            # --------------------------------------------------

            cv2.rectangle(

                frame,

                (
                    zone_x1,
                    zone_y1
                ),

                (
                    zone_x2,
                    zone_y2
                ),

                (0, 0, 255),

                3
            )

            # --------------------------------------------------
            # Danger-zone label
            # --------------------------------------------------

            cv2.putText(

                frame,

                "PREDEFINED DANGER ZONE",

                (
                    zone_x1 + 10,
                    max(
                        30,
                        zone_y1 - 10
                    )
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.65,

                (0, 0, 255),

                2
            )

        # ======================================================
        # ALERT MESSAGE
        # ======================================================

        if self.fall_detected:

            alert_text = (
                "FALL DETECTED"
            )

        elif self.hand_in_danger:

            alert_text = (
                "HAND IN DANGER ZONE"
            )

        elif self.body_in_danger:

            alert_text = (
                "WORKER IN DANGER ZONE"
            )

        else:

            alert_text = ""

        # ======================================================
        # DISPLAY ALERT
        # ======================================================

        if alert_text != "":

            cv2.putText(

                frame,

                alert_text,

                (25, 85),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 0, 255),

                3
            )

        # ======================================================
        # FINAL STATUS
        #
        # IMPORTANT:
        #
        # Danger-zone violation is NOT called anomaly here.
        # Anomaly detection is handled separately by
        # anomaly_detector.py.
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

            status = (
                "SAFE"
            )

            status_color = (
                0,
                180,
                0
            )

        else:

            status = (
                "NO WORKER"
            )

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

            (25, 45),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.9,

            status_color,

            3
        )

        # ======================================================
        # RETURN RESULT
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
                status
        }

    # ==========================================================
    # RELEASE
    # ==========================================================

    def release(self):

        if self.pose is not None:

            self.pose.close()

        if self.hands is not None:

            self.hands.close()