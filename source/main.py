from tile_board import TileBoard
from extra_ui import IOBoard, ToolBox
import tkinter as tk
from tkinter import filedialog
from time import time
import json


class LadderLogic:

    def __init__(self,file_data=None):


        self.root=tk.Toplevel()
        self.root.title('LadderLogic')


        if(file_data==None):
            self.board=TileBoard(self.root,self)
        else:
            self.board=TileBoard(self.root,self,tile_size=file_data['settings']["tile_size"])
        self.board.grid(column=0,row=1, sticky="nsew")

        self.io=IOBoard(self.root,self)
        self.io.grid(column=2,row=1, sticky="nsew")

        if(file_data!=None):
            self.board.load_from_file(file_data['TileBoard'])
            self.io.load_from_file(file_data['IOBoard'])

        self.board.start()

        print("config done")
        self.tools=ToolBox(self.root,self)
        self.tools.grid(column=0,row=0, sticky="nsew")

        self.root.grid_rowconfigure(1,weight=0)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=0)
        self.root.grid_columnconfigure(2,weight=0)

        # self.root.createcommand('::tk::mac::ShowPreferences', self.luanch_preferences)

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

        self.root.bind("<Command-n>", lambda x:self.file_new())
        self.root.bind("<Command-o>", lambda x:self.file_open())
        self.root.bind("<Command-s>", lambda x:self.file_save())
        self.root.bind("<Command-Shift-s>", lambda x:self.file_saveas())
        self.root.bind("<Command-w>", lambda x:self.root.destroy())

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
            file_data=json.load(f)

        #Cheak version by file_data["0header"]
        LadderLogic(file_data=file_data)

        # new_window.board.grid_forget()
        # new_window.board=TileBoard(new_window.root,new_window,
        #     tile_size=file_data['settings']["tile_size"])

        # new_window.board.grid(column=0,row=1, sticky="nsew")

        # self.board.load_from_file(file_data['TileBoard'])

        # new_window.io.load_from_file(file_data['IOBoard'])

        # new_window.board.start()


         #test for extra features



    def file_save(self):

        file_data={}
        file_data['0header']={"sys":"osx","POSIX":str(int(time())),"version":"1.0 Alpha"}
        file_data['settings']={"tile_size":self.board.tile_size}
        file_data['TileBoard']=self.board.save_to_file()
        file_data['IOBoard']=self.io.save_to_file()


        with open(self.filename,mode="w+") as f:
            json.dump(file_data,f, sort_keys=True)

    def file_saveas(self):
        self.filename=filedialog.asksaveasfilename(defaultextension='.lil',initialfile='')
        self.filemenu.entryconfigure(2, state=tk.NORMAL)

        self.file_save()



    def luanch_preferences(self,event=None):
        print("luanch_preferences")



if __name__ == "__main__":

    main_root=tk.Tk()
    LadderLogic()
    main_root.withdraw()
    main_root.mainloop()