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

        self.filemenu.add_command(label="New", command=self.file_new)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save As...", command=self.file_saveas)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
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

    def file_save(self):
        print("file_save")

    def file_saveas(self):
        self.filename=filedialog.asksaveasfilename(defaultextension='.lil',initialfile='')

        with open(self.filename,mode="w+") as f:
            pass
            f.write("<>"+'\n')# prevents editors from reading html
            f.write("<header>"+'\n')
            f.write("Uid:filetype"+'\n')
            f.write("Sys:"+'\n')
            f.write("POSIX:"+str(int(time()))+'\n')
            f.write("Version:"+"1.0 Alpha"+'\n')

            f.write("<header/>"+'\n')

            f.write("<TileBoard>"+'\n')
            f.write("X:"+str(len(self.board.tiles))+'\n')
            f.write("Y:"+str(len(self.board.tiles[0]))+'\n')

            for column in self.board.tiles:
                for tile in column:
                    f.write(tile.save_to_file()+"\n")

                f.write("sep"+'\n')

            f.write("<TileBoard/>"+'\n')

            f.write("<IOBoard>"+'\n')
            f.write("<IOBoard/>"+'\n')

            f.write("<Settings>"+'\n')
            f.write("<Settings/>"+'\n')




    def luanch_preferences(self,event=None):
        print("luanch_preferences")



if __name__ == "__main__":

    l=LadderLogic()


    l.root.mainloop()