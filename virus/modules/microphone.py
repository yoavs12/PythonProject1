import pyaudio
import wave
import time
import os
import threading


class MicrophoneRecorder:
    def __init__(self, output_filename="recorded_audio.wav"):
        self.output_filename = output_filename
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.frames = []
        self.p = None
        self.stream = None
        self.is_recording = False
        self.recording_thread = None

    def _record(self):
        """
        פונקציה פנימית שמבצעת את ההקלטה בפועל
        """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        self.is_recording = True
        counter = 0

        print("מתחיל הקלטה... ההקלטה תימשך עד סיום התוכנית")

        while self.is_recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)

                # הצגת התקדמות כל 5 שניות
                counter += 1
                if counter % int(self.rate / self.chunk * 5) == 0:
                    seconds = counter / (self.rate / self.chunk)
                    print(f"מקליט... ({seconds:.0f} שניות)")
            except:
                break

    def start(self):
        """
        מתחיל את ההקלטה בתהליך נפרד
        """
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.daemon = True  # התהליך יסתיים כשהתוכנית הראשית תסתיים
        self.recording_thread.start()

    def stop(self):
        """
        מפסיק את ההקלטה ושומר את הקובץ
        """
        if not self.is_recording:
            return

        self.is_recording = False

        if self.recording_thread:
            self.recording_thread.join(timeout=1)

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.p:
            self.p.terminate()

        # יצירת תיקייה אם לא קיימת
        os.makedirs(os.path.dirname(self.output_filename) if os.path.dirname(self.output_filename) else '.',
                    exist_ok=True)

        # שמירת הקובץ
        if self.frames:
            wf = wave.open(self.output_filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            print(f"הקובץ נשמר בהצלחה: {self.output_filename}")
        else:
            print("אין נתונים להקלטה")

    def run(self):
        """
        מתחיל הקלטה ומגדיר פעולות ניקוי כשהתוכנית מסתיימת
        """
        try:
            # רישום פעולת ניקוי שתרוץ בסיום התוכנית
            import atexit
            atexit.register(self.stop)

            # התחלת ההקלטה
            self.start()

            print("ההקלטה פעילה ברקע ותישמר אוטומטית בסיום התוכנית")
            print("למעבר לתפריט הראשי, הקש Enter")
            input()  # חכה עד שהמשתמש ילחץ Enter

        except KeyboardInterrupt:
            # נלחץ Ctrl+C
            self.stop()


# אם הקובץ מורץ ישירות, יפעיל את ההקלטה
if __name__ == "__main__":
    recorder = MicrophoneRecorder("audio_recording.wav")
    recorder.run()