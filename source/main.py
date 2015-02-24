from tile_board import TileBoard
from extra_ui import IOBoard, ToolBox
import tkinter as tk

class LadderLogic:

    def __init__(self):

        self.root=tk.Tk()
        self.root.title('LadderLogic')

        self.io=IOBoard(self.root,self)
        self.io.grid(column=2,row=1, sticky="nsew")

        self.board=TileBoard(self.root,self)
        self.board.grid(column=0,row=1, sticky="nsew")

        self.tools=ToolBox(self.root,self)
        self.tools.grid(column=0,row=0, sticky="nsew")

        self.root.grid_rowconfigure(1,weight=0)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=0)
        self.root.grid_columnconfigure(2,weight=0)


if __name__ == "__main__":

    l=LadderLogic()


    l.root.mainloop()