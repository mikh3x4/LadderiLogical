from tile_board import TileBoard
from extra_ui import IOBoard, ToolBox
import tkinter as tk
from tkinter import filedialog
from time import time

class LadderLogic:

    def __init__(self):

        self.root=tk.Tk()
        self.root.title('LadderLogic')

        self.board=TileBoard(self.root,self)
        self.board.grid(column=0,row=1, sticky="nsew")

        self.io=IOBoard(self.root,self)
        self.io.grid(column=2,row=1, sticky="nsew")

        print("config done")
        self.tools=ToolBox(self.root,self)
        self.tools.grid(column=0,row=0, sticky="nsew")

        self.root.grid_rowconfigure(1,weight=0)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=0)
        self.root.grid_columnconfigure(2,weight=0)

        self.root.createcommand('::tk::mac::ShowPreferences', self.luanch_preferences)

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="New", command=self.file_new, accelerator="Command+N")
        self.filemenu.add_command(label="Open", command=self.file_open, accelerator="Command+O")
        self.filemenu.add_command(label="Save", command=self.file_save, accelerator="Command+S")

        self.filemenu.entryconfigure(2, state=tk.DISABLED)
        self.filemenu.add_command(label="Save As...", command=self.file_saveas, accelerator="Shift-Command+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit, accelerator="Command+Q")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.root.config(menu=self.menubar)

        self.filename=""

    def file_new(self):
        #Generate warnings etc?
        #NEED EXTENSIVE TESTING
        LadderLogic()

        print("file_new")

    def file_open(self):
        print("file_open")
        file_to_open=filedialog.askopenfilename(defaultextension='.lil',initialfile='')
        with open(file_to_open,mode="r") as f:
            new_window=LadderLogic()


    def file_save(self):
        with open(self.filename,mode="w+") as f:
            f.write("<>"+'\n')# prevents editors from reading html
            f.write("<header>"+'\n')
            f.write("Uid:filetype"+'\n')
            f.write("Sys:"+'\n')
            f.write("POSIX:"+str(int(time()))+'\n')
            f.write("Version:"+"1.0 Alpha"+'\n')

            f.write("<header/>"+'\n')

            f.write("<Settings>"+'\n')
            f.write("<Settings/>"+'\n')

            f.write("<TileBoard>"+'\n')
            f.write("X:"+str(len(self.board.tiles))+'\n')
            f.write("Y:"+str(len(self.board.tiles[0]))+'\n')

            for column in self.board.tiles:
                for tile in column:
                    f.write(tile.save_to_file()+"\n")

                f.write("sep"+'\n')

            f.write("<TileBoard/>"+'\n')

            f.write("<IOBoard>"+'\n')
            f.write(self.io.save_to_file()+'\n')

            f.write("<IOBoard/>"+'\n')

    def file_saveas(self):
        self.filename=filedialog.asksaveasfilename(defaultextension='.lil',initialfile='')
        self.filemenu.entryconfigure(2, state=tk.NORMAL)

        self.file_save()



    def luanch_preferences(self,event=None):
        print("luanch_preferences")



if __name__ == "__main__":

    l=LadderLogic()


    l.root.mainloop()