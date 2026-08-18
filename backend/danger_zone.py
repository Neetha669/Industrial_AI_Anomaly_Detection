import cv2


# ============================================================
# PREDEFINED FLOOR DANGER ZONE
# ============================================================

DANGER_ZONE = {
    "x1": 0.42,
    "y1": 0.60,
    "x2": 0.72,
    "y2": 0.92
}


# ============================================================
# GET PIXEL COORDINATES
# ============================================================

def get_danger_zone(frame):

    height, width = frame.shape[:2]

    x1 = int(width * DANGER_ZONE["x1"])
    y1 = int(height * DANGER_ZONE["y1"])

    x2 = int(width * DANGER_ZONE["x2"])
    y2 = int(height * DANGER_ZONE["y2"])

    return x1, y1, x2, y2


# ============================================================
# POINT INSIDE DANGER ZONE
# ============================================================

def point_inside_danger_zone(x, y, frame):

    x1, y1, x2, y2 = get_danger_zone(frame)

    return (
        x1 <= x <= x2
        and
        y1 <= y <= y2
    )


# ============================================================
# CHECK PERSON
# ============================================================

def check_person_in_danger_zone(
    x1,
    y1,
    x2,
    y2,
    frame
):

    foot_x = int((x1 + x2) / 2)
    foot_y = int(y2)

    return point_inside_danger_zone(
        foot_x,
        foot_y,
        frame
    )


# ============================================================
# DRAW DANGER ZONE
# ============================================================

def draw_danger_zone(
    frame,
    violation=False
):

    # Do NOT show zone when nobody is inside
    if not violation:
        return frame

    x1, y1, x2, y2 = get_danger_zone(frame)

    # --------------------------------------------------------
    # TRANSPARENT RED AREA
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
        0.15,
        frame,
        0.85,
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
            x1 + 10,
            max(30, y1 - 10)
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        3
    )

    return frame