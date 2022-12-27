from playsound import playsound
from _thread import *

class WinMusic:
    def play(file):
        start_new_thread(playsound, (file, ))
        

    
    

    