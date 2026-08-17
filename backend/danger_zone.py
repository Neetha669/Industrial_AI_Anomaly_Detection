import cv2


# ============================================================
# PREDEFINED DANGER ZONE
# ============================================================

ZONE_X = 150
ZONE_Y = 250

ZONE_WIDTH = 350
ZONE_HEIGHT = 180


# ============================================================
# GET DANGER ZONE
# ============================================================

def get_danger_zone():

    return (
        ZONE_X,
        ZONE_Y,
        ZONE_X + ZONE_WIDTH,
        ZONE_Y + ZONE_HEIGHT
    )


# ============================================================
# POINT INSIDE DANGER ZONE
# ============================================================

def is_inside_danger_zone(x, y):

    x1, y1, x2, y2 = get_danger_zone()

    return (
        x1 <= x <= x2
        and
        y1 <= y <= y2
    )


# ============================================================
# DRAW PREDEFINED DANGER ZONE
# ============================================================

def draw_danger_zone(frame):

    x1, y1, x2, y2 = get_danger_zone()

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        "PREDEFINED DANGER ZONE",
        (x1 + 5, max(30, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255),
        2
    )

    return frame