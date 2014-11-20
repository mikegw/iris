import time
from Tkinter import *
import cwiid

class Application(Frame):
    def __init__(self, master):
        """Initialize the frame."""
        Frame.__init__(self, master)
        self.pos = '0'
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """Create label"""
        self.lbl = Label(self.frame, text = 'ready')
        self.con = Button(self.frame)
        self.con['text'] = "click here to connect"
        self.con['command'] = self.connect()
        self.up = Button(self.frame, text = 'click to update')
        self.up['command'] = self.update_pos()
    
    def connect(self):
        self.wm = cwiid.Wiimote()
        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_IR
        self.update_pos()
    
    def update_pos(self):
        if self.wm.state['ir_src'] == [None, None, None, None]:
            self.lbl['text'] = 'None'
        else:
            self.lbl['text'] = str(self.wm.state['ir_src'][0]['pos'][0])+ ', ' + str(self.wm.state['ir_src'][0]['pos'][1])

print(1)
root = Tk()
print(2)
root.title("Position finder")
print(3)
app = Application(master = root)
print(4)
app.mainloop()
print(5)
root.destroy()
