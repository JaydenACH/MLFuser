import tkinter as tk
from tkinter import ttk
import json
import pandas as pd
import pyautogui
import threading
from time import sleep
import sys


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('MLfuser')
        #place widgets here

        self.root.mainloop()

if __name__ == "__main__":
    app = App()