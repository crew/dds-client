#!/usr/local/bin/python
"""DEPENDENCIES:
 Packages: python-tk, python-imaging, python-imaging-tk
"""
import PIL.Image
import Tkinter as tk
import ImageTk

def closeWindow(event):
	global root
	root.quit()

root=tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set() # <-- move focus to this widget
root.bind("<Key>", closeWindow)
	
i = ImageTk.PhotoImage(PIL.Image.open("test.jpg"))
label = tk.Label(root, image=i)
label.photo = i
label.pack()
root.mainloop()
