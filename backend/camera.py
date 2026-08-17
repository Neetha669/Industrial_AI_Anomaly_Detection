import cv2


class Camera:

    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("Unable to open webcam.")

    def get_frame(self):

        success, frame = self.cap.read()

        if not success:
            return None

        return frame

    def release(self):

        if self.cap.isOpened():
            self.cap.release()


if __name__ == "__main__":

    camera = Camera()

    while True:

        frame = camera.get_frame()

        if frame is None:
            break

        cv2.imshow("Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()