from tkinter.tix import MAIN
from detection import Detection
from main import main
from windowcapture import WindowCapture
import state
import gamestate

if __name__ == "__main__":
    stage_num = None
    wincap = WindowCapture()
    detection = Detection()
    tactician = state.Tactician()
    gamecontext = gamestate.GameContext()

    
    while True:


        """
        update screenshot
        search for object
        """