"""
Blink GUI

Run on main thread
"""
from dependencies import *
from gui_objects import *
from blink_simulation import BlinkSimulation

class BlinkGUI():
    def __init__(self, network_file, config_file):
        self.app = wx.App()
        self.window = Blink_Frame(None)
        self.window.setGrid(4,3)
        self.window.InitUI()

        sim = BlinkSimulation()
        sim.configure(config_file)
        sim.create_network(network_file)
        sim.init(self.window)

        # self.window.Show(True)
        self.app.MainLoop()