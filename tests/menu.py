from tkinter import *


root = Tk()

def hello():
    print("hello!")

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello, accelerator="Command+P")
menubar.add_cascade(label="Edit", menu=editmenu)


submenu = Menu(menubar, tearoff=0)
submenu.add_command(label="sub1", command=hello)
submenu.add_command(label="sub2", command=hello)
editmenu.add_cascade(label="SUBME", menu=submenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

# create a popup menu
menu_dropdown = Menu(root, tearoff=0)
menu_dropdown.add_command(label="Undo", command=hello)
menu_dropdown.add_command(label="Redo", command=hello)
def config_dialog(event=None):
	print('settings')

root.createcommand('::tk::mac::ShowPreferences', config_dialog)
# create a canvas
frame = Frame(root, width=512, height=512)
frame.pack()

def popup(event):
    menu_dropdown.post(event.x_root, event.y_root)

# attach popup to canvas
frame.bind("<Button-3>", popup)

root.mainloop()