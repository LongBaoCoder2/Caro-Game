from playsound import playsound
import threading

class MusicGame:
    def play(file2):
        threading.Thread(target=playsound, args=(file2,), daemon=True).start()