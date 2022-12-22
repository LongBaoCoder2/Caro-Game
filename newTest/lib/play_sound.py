from playsound import playsound
import threading

class PlaySound:
    def play(file):
        threading.Thread(target=playsound, args=(file,), daemon=True).start()
