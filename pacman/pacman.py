import sys
import os

def get_base_path():
    if getattr(sys, 'frozen', False): # executable
        return sys._MEIPASS
    else:
        return os.path.dirname(__file__)
base_path = get_base_path()
sys.path.append(os.path.join(base_path, 'classes'))

import Game_Controller

if __name__ == '__main__':
    print('Hello, World!')