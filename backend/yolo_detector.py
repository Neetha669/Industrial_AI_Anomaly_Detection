# backend/yolo_detector.py

import os
import cv2
import mediapipe as mp

from ultralytics import YOLO

from backend.danger_zone import (
    get_danger_zone,
    check_person_in_danger_zone,
    draw_danger_zone
)


class YOLODetector:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(
        self,
        model_path=None,
        enable_danger_zone=False,
        video_mode="video1"
    ):

        self.enable_danger_zone = enable_danger_zone
        self.video_mode = video_mode

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
        # YOLO MODEL
        # ------------------------------------------------------

        if model_path is None:

            model_path = os.path.join(
                project_root,
                "models",
                "yolov8n.pt"
            )

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                "YOLO model not found:\n"
                f"{model_path}"
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
        # PERSON VALIDATION
        # ======================================================

        self.minimum_pose_landmarks = 5

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
    # CHECK REAL PERSON
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

        box_width = bx2 - bx1
        box_height = by2 - by1

        if box_width <= 0 or box_height <= 0:
            return False

        valid_landmarks = 0
        visible_landmarks = []

        # ------------------------------------------------------
        # CHECK POSE LANDMARKS
        # ------------------------------------------------------

        for landmark_id in self.required_pose_landmarks:

            landmark = pose_landmarks[
                landmark_id
            ]

            if landmark.visibility < 0.50:
                continue

            lx = int(
                landmark.x * width
            )

            ly = int(
                landmark.y * height
            )

            visible_landmarks.append(
                (lx, ly)
            )

            if (
                bx1 <= lx <= bx2
                and
                by1 <= ly <= by2
            ):

                valid_landmarks += 1

        # ------------------------------------------------------
        # NOT ENOUGH HUMAN LANDMARKS
        # ------------------------------------------------------

        if len(visible_landmarks) < 5:
            return False

        if valid_landmarks < self.minimum_pose_landmarks:
            return False

        # ------------------------------------------------------
        # CREATE POSE BOX
        # ------------------------------------------------------

        pose_xs = [
            point[0]
            for point in visible_landmarks
        ]

        pose_ys = [
            point[1]
            for point in visible_landmarks
        ]

        pose_x1 = min(pose_xs)
        pose_y1 = min(pose_ys)

        pose_x2 = max(pose_xs)
        pose_y2 = max(pose_ys)

        pose_width = pose_x2 - pose_x1
        pose_height = pose_y2 - pose_y1

        if pose_width <= 0 or pose_height <= 0:
            return False

        # ------------------------------------------------------
        # CENTER CHECK
        # ------------------------------------------------------

        box_center_x = (
            bx1 + bx2
        ) / 2

        box_center_y = (
            by1 + by2
        ) / 2

        pose_center_x = (
            pose_x1 + pose_x2
        ) / 2

        pose_center_y = (
            pose_y1 + pose_y2
        ) / 2

        center_distance_x = abs(
            box_center_x -
            pose_center_x
        )

        center_distance_y = abs(
            box_center_y -
            pose_center_y
        )

        if center_distance_x > box_width * 0.50:
            return False

        if center_distance_y > box_height * 0.50:
            return False

        # ------------------------------------------------------
        # SIZE CHECK
        # ------------------------------------------------------

        if box_width > pose_width * 2.5:
            return False

        if box_height > pose_height * 2.5:
            return False

        return True


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

        if not persons or len(persons) <= 1:
            return persons

        # Highest confidence first

        persons = sorted(
            persons,
            key=lambda person:
                person["confidence"],
            reverse=True
        )

        filtered = []

        for person in persons:

            is_duplicate = False

            for existing in filtered:

                iou = self.calculate_iou(
                    person,
                    existing
                )

                if iou > 0.50:

                    is_duplicate = True
                    break

            if not is_duplicate:

                filtered.append(
                    person
                )

        return filtered


    # ==========================================================
    # FALL DETECTION
    # ==========================================================

    def detect_fall(
        self,
        landmarks
    ):

        if landmarks is None:
            return False

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

        # ------------------------------------------------------
        # VISIBILITY
        # ------------------------------------------------------

        if not (
            left_shoulder.visibility > 0.4
            and
            right_shoulder.visibility > 0.4
            and
            left_hip.visibility > 0.4
            and
            right_hip.visibility > 0.4
        ):

            return False

        # ------------------------------------------------------
        # SHOULDER CENTER
        # ------------------------------------------------------

        shoulder_x = (
            left_shoulder.x +
            right_shoulder.x
        ) / 2

        shoulder_y = (
            left_shoulder.y +
            right_shoulder.y
        ) / 2

        # ------------------------------------------------------
        # HIP CENTER
        # ------------------------------------------------------

        hip_x = (
            left_hip.x +
            right_hip.x
        ) / 2

        hip_y = (
            left_hip.y +
            right_hip.y
        ) / 2

        # ------------------------------------------------------
        # DIFFERENCES
        # ------------------------------------------------------

        vertical_difference = abs(
            hip_y -
            shoulder_y
        )

        horizontal_difference = abs(
            hip_x -
            shoulder_x
        )

        if vertical_difference <= 0:
            return False

        # ------------------------------------------------------
        # FALL CONDITION
        # ------------------------------------------------------

        return (
            horizontal_difference >
            vertical_difference * 1.5
        )


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
        # DO NOT FLIP HERE
        # ======================================================
        #
        # The video frame should be used exactly as supplied.
        #
        # This prevents the danger-zone coordinates from moving
        # to the opposite side.
        #
        # ======================================================

        height, width = frame.shape[:2]

        # ======================================================
        # RGB
        # ======================================================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ======================================================
        # MEDIAPIPE POSE
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

            conf=0.70,

            iou=0.45,

            classes=[0],

            verbose=False
        )

        persons = []

        # ======================================================
        # READ YOLO BOXES
        # ======================================================

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
                # ONLY COCO PERSON CLASS
                # ------------------------------------------------

                if class_id != 0:
                    continue

                if confidence < 0.70:
                    continue

                bx1, by1, bx2, by2 = map(
                    int,
                    box.xyxy[0]
                )

                # ------------------------------------------------
                # CLAMP TO FRAME
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

                    "confidence":
                        confidence
                }

                # ------------------------------------------------
                # PERSON VALIDATION
                # ------------------------------------------------

                if pose_landmarks is not None:

                    if not self.is_real_person(
                        candidate,
                        pose_landmarks,
                        width,
                        height
                    ):

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
        # WORKER DETECTED
        # ======================================================

        if len(persons) > 0:

            self.worker_detected = True

        # ======================================================
        # FALL DETECTION
        #
        # VIDEO 1 ONLY
        # ======================================================

        if (
            self.video_mode == "video1"
            and
            pose_landmarks is not None
        ):

            self.fall_detected = (
                self.detect_fall(
                    pose_landmarks
                )
            )

        # ======================================================
        # VIDEO 2 DANGER ZONE
        #
        # ONLY VIDEO 2
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

            foot_y = int(
                by2
            )

            # --------------------------------------------------
            # DEFAULT
            # --------------------------------------------------

            person_in_danger = False

            # --------------------------------------------------
            # VIDEO 2 ONLY
            # --------------------------------------------------

            if (
                self.video_mode == "video2"
                and
                self.enable_danger_zone
            ):

                person_in_danger = (
                    check_person_in_danger_zone(
                        bx1,
                        by1,
                        bx2,
                        by2,
                        frame
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

            # ==================================================
            # FALL
            # ==================================================

            elif (
                self.video_mode == "video1"
                and
                self.fall_detected
            ):

                box_color = (
                    0,
                    0,
                    255
                )

                label = (
                    "FALL DETECTED"
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

            # ==================================================
            # DRAW PERSON BOX
            # ==================================================

            cv2.rectangle(

                frame,

                (bx1, by1),

                (bx2, by2),

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

            # ==================================================
            # FOOT POINT
            # ==================================================

            cv2.circle(

                frame,

                (
                    foot_x,
                    foot_y
                ),

                6,

                box_color,

                -1
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

        # ======================================================
        # DRAW VIDEO 2 DANGER ZONE
        #
        # ONLY WHEN WORKER ENTERS
        # ======================================================

        if (
            self.video_mode == "video2"
            and
            self.enable_danger_zone
            and
            self.danger_detected
        ):

            frame = draw_danger_zone(

                frame,

                violation=True
            )

        # ======================================================
        # STATUS
        # ======================================================

        if (
            self.video_mode == "video1"
            and
            self.fall_detected
        ):

            status = (
                "FALL DETECTED"
            )

            status_color = (
                0,
                0,
                255
            )

        elif (
            self.video_mode == "video2"
            and
            self.danger_detected
        ):

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
        # STATUS DISPLAY
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
        # ALERT DISPLAY
        # ======================================================

        if (
            self.video_mode == "video1"
            and
            self.fall_detected
        ):

            cv2.putText(

                frame,

                "FALL DETECTED",

                (
                    25,
                    85
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (
                    0,
                    0,
                    255
                ),

                3
            )

        elif (
            self.video_mode == "video2"
            and
            self.body_in_danger
        ):

            cv2.putText(

                frame,

                "WORKER IN DANGER ZONE",

                (
                    25,
                    85
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (
                    0,
                    0,
                    255
                ),

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

            try:

                self.pose.close()

            except Exception:
                pass

            self.pose = None

        if self.hands is not None:

            try:

                self.hands.close()

            except Exception:
                pass

            self.hands = None

        print(
            "YOLO detector released."
        )