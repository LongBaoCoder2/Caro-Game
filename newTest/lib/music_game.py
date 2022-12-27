from playsound import playsound
from threading import Thread
class MusicGame:

    def play(file2):
        t=Thread(target=playsound, args=(file2,), daemon=True)
        t.start()
        
      
       
