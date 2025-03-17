from PIL import ImageGrab
import datetime

class ScreenshotModule:
    def __init__(self, screenshot_path="./"):
        self.screenshot_path = screenshot_path

    def generate_screenshot_path(self) -> str:
        return f"{self.screenshot_path}{datetime.datetime.now().timestamp()}.png"

    def run(self):
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot.save(self.generate_screenshot_path())
        print("📸 Screenshot saved!")

if __name__ == "__main__":
    ScreenshotModule().run()