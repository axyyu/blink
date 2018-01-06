"""
Blink GUI Setup

"""

from dependencies import *
from gui_objects import intersection_panel
from gui_objects import region_frame

class Blink_Frame(wx.Frame): 
    def __init__(self, network, *args, **kw):  
        super(Blink_Frame, self).__init__(*args, **kw) 
        self.width, self.height = wx.GetDisplaySize()
        self.network = network
        self.InitUI()
     
    def InitUI(self): 
        self.SetSize((self.width,self.height-30)) 
        self.SetTitle('Blink')
        self.Centre()
        self.setup_network()
        self.Show(True)

    def setup_network(self):
        pass