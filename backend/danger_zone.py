# backend/danger_zone.py

import cv2


# ============================================================
# VIDEO 2 - INDUSTRIAL DANGER ZONE
# ============================================================
#
# Rectangle placed on the RIGHT-SIDE FLOOR AREA.
#
# Normalized coordinates:
# x1, y1 = top-left
# x2, y2 = bottom-right
#
# 0.0 -> left/top
# 1.0 -> right/bottom
# ============================================================

DANGER_ZONE = {
    "x1": 0.62,
    "y1": 0.64,

    "x2": 0.79,
    "y2": 0.86
}


# ============================================================
# GET DANGER ZONE PIXEL COORDINATES
# ============================================================

def get_danger_zone(frame):

    if frame is None:
        return 0, 0, 0, 0

    height, width = frame.shape[:2]

    x1 = int(width * DANGER_ZONE["x1"])
    y1 = int(height * DANGER_ZONE["y1"])

    x2 = int(width * DANGER_ZONE["x2"])
    y2 = int(height * DANGER_ZONE["y2"])

    return x1, y1, x2, y2


# ============================================================
# CHECK POINT INSIDE RECTANGULAR DANGER ZONE
# ============================================================

def point_inside_danger_zone(
    x,
    y,
    frame
):

    if frame is None:
        return False

    x1, y1, x2, y2 = get_danger_zone(frame)

    return (
        x1 <= x <= x2
        and
        y1 <= y <= y2
    )


# ============================================================
# CHECK PERSON INSIDE DANGER ZONE
# ============================================================
#
# We check the bottom-center / foot point.
#
# This is important because the danger zone represents
# the FLOOR area.
# ============================================================

def check_person_in_danger_zone(
    x1,
    y1,
    x2,
    y2,
    frame
):

    if frame is None:
        return False

    # Bottom-center / foot point
    foot_x = int((x1 + x2) / 2)
    foot_y = int(y2)

    return point_inside_danger_zone(
        foot_x,
        foot_y,
        frame
    )


# ============================================================
# VIDEO 2 COMPATIBILITY FUNCTION
# ============================================================
#
# Your Live Monitoring code is currently trying to import:
#
# check_video2_person_in_danger_zone
#
# So we provide that function here.
#
# It uses the SAME danger-zone logic above.
# ============================================================

def check_video2_person_in_danger_zone(
    x1,
    y1,
    x2,
    y2,
    frame
):

    return check_person_in_danger_zone(
        x1,
        y1,
        x2,
        y2,
        frame
    )


# ============================================================
# DRAW DANGER ZONE
# ============================================================
#
# Rectangle is shown ONLY when violation=True.
# ============================================================

def draw_danger_zone(
    frame,
    violation=False
):

    if frame is None:
        return frame

    # Do not show zone when there is no violation
    if not violation:
        return frame

    x1, y1, x2, y2 = get_danger_zone(frame)

    # --------------------------------------------------------
    # TRANSPARENT RED RECTANGLE
    # --------------------------------------------------------

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x1, y1),
        (x2, y2),
        (0, 0, 255),
        -1
    )

    frame[:] = cv2.addWeighted(
        overlay,
        0.18,
        frame,
        0.82,
        0
    )

    # --------------------------------------------------------
    # RED BORDER
    # --------------------------------------------------------

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 0, 255),
        4
    )

    # --------------------------------------------------------
    # LABEL
    # --------------------------------------------------------

    cv2.putText(
        frame,
        "DANGER ZONE",
        (
            x1 + 8,
            max(30, y1 - 10)
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    return frame