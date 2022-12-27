from playsound import playsound
import threading
stop_thread =threading.Event()

class PlaySound:
    def play(file):
        threading.Thread(target=playsound, args=(file,), daemon=True).start()