import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Import your backend function
from backend.yolo_detector import get_frame


class CameraFrame:

    def __init__(self, parent):

        self.parent = parent

        self.label = tk.Label(parent)
        self.label.pack()

        self.update_frame()

    def update_frame(self):

        frame = get_frame()

        if frame is not None:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = Image.fromarray(frame)

            image = image.resize((700, 500))

            photo = ImageTk.PhotoImage(image)

            self.label.configure(image=photo)

            self.label.image = photo

        self.parent.after(20, self.update_frame)