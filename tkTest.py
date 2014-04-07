#!/usr/local/bin/python
"""DEPENDENCIES:
 Packages: python-tk, python-imaging, python-imaging-tk
"""
import PIL.Image
import Tkinter as tk
import ImageTk


# -> TKWindow
# creates a new TKWindow, Does not display the window
def getWindow():
	root = tk.Tk()
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.overrideredirect(1)
	root.geometry("%dx%d+0+0" % (w, h))
	root.focus_set()
	#Should close the window with a key press, currently not working
	root.bind("<Key>", lambda e: e.widget.quit())
	return root
	
# TKwindow PhotoImage(TK) -> Void
# Adds the given PhotoImage to the given window
def addImageToWindow(window, img):
	label = tk.Label(window, image=img)
	label.photo = img
	label.pack()

# String -> PhotoImage(TK)
#retrieves the from the given path, creates a PhotoImage
def getPhotoImg(path):
	return ImageTk.PhotoImage(PIL.Image.open(path))

# TKWindo String -> Void
# adds the image at the given path to the window
def getImgAddToWindow(window, path):
	addImageToWindow(window, getPhotoImg(path))


# String -> TKWindow	
#Creates a window and adds the image at the given path to it
def makeImageSlide(pathToImage):
	w = getWindow()
	getImgAddToWindow(w, pathToImage)
	return w

# TKWindow -> Void	
#Opens and rns the given window
def popWindow(window):
	window.mainloop()

if __name__ == "__main__":
	popWindow(makeImageSlide("testslide1.jpg"))

