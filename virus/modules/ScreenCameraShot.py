import cv2

class CameraShot:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def capture(self):
        success, frame = self.camera.read()
        if success:
            cv2.imshow("Captured Screenshot", frame)
            cv2.waitKey(0)
            cv2.imwrite("camera_shot.jpg", frame)
            cv2.destroyAllWindows()
            print("📸 Screenshot saved as camera_shot.jpg")
        else:
            print("❌ Screenshot could not be grabbed.")

    def run(self):
        self.capture()


if __name__ == "__main__":
    CameraShot().run()