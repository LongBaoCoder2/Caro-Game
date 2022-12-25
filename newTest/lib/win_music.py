from playsound import playsound
import threading

class WinMusic:
    def play(file3):
        threading.Thread(target=playsound, args=(file3,), daemon=True).start()