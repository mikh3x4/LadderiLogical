from tile_board import TileBoard
from extra_ui import IOBoard, ToolBox
from asm_compiler import Compiler, CompilerSettingsWindow
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
from time import time
import json


class LadderLogic:

    version='1.0 Alpha'

    def __init__(self,main_root,windows,file_data=None,file_name=""):
        self.main_root=main_root

        self.window_list=windows
        self.window_list.append(self)
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

            if(len(file_data)!=4): #0header settings TileBoard IOBoard
                print("File contains unimplemented toplevel feature")

        self.board.start()

        print("config done")
        self.tools=ToolBox(self.root,self)
        self.tools.grid(column=0,row=0, sticky="nsew",columnspan=3)

        self.root.grid_rowconfigure(0,weight=0)
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


        self.compilermenu = tk.Menu(self.menubar, tearoff=0)
        self.compilermenu.add_command(label="Options", command=lambda:CompilerSettingsWindow(self.board,self.io))
        self.compilermenu.add_separator()
        self.compilermenu.add_command(label="Generate for MPLab", command=lambda:Compiler(self,typ='MPLab'))
        self.compilermenu.add_command(label="Generate for Debugger", command=lambda:Compiler(self,typ='Debug'))
        self.compilermenu.add_command(label="Generate for Custom", command=lambda:Compiler(self,typ='Plain'))

        self.menubar.add_cascade(label="Compiler", menu=self.compilermenu)

        self.root.config(menu=self.menubar)

        self.root.bind("<Command-n>", lambda x:self.file_new())
        self.root.bind("<Command-o>", lambda x:self.file_open())
        
        self.root.bind("<Command-Shift-s>", lambda x:self.file_saveas())
        self.root.bind("<Command-w>", self.close_window)




        self.filename=file_name

        if(self.filename!=""):
            self.filemenu.entryconfigure(2, state=tk.NORMAL)
            self.root.bind("<Command-s>", lambda x:self.file_save())

        print(self.window_list)

    def close_window(self,event):
        i=self.window_list.index(self)
        self.window_list.pop(i)

        if(len(self.window_list)==0):
            print('quiting')
            self.main_root.quit()
        else:
            self.root.destroy()

    def file_new(self):
        #Generate warnings etc?
        #NEED EXTENSIVE TESTING
        LadderLogic(self.main_root,self.window_list)

        print("file_new")

    def file_open(self):
        print("file_open")
        file_to_open=filedialog.askopenfilename(defaultextension='.lil',initialfile='')

        with open(file_to_open,mode="r") as f:
            file_data=json.load(f)

        LadderLogic(self.main_root,self.window_list,file_data=file_data,file_name=file_to_open)



    def file_save(self,file_to_save=None):

        file_data={}
        file_data['0header']={"sys":"osx","POSIX":str(int(time())),"version":self.version}
        file_data['settings']={"tile_size":self.board.tile_size}
        file_data['TileBoard']=self.board.save_to_file()
        file_data['IOBoard']=self.io.save_to_file()

        if(file_to_save==None):
            file_to_save=self.filename

        with open(file_to_save,mode="w+") as f:
            json.dump(file_data,f, sort_keys=True)

    def file_saveas(self):
        
        file_to_save=filedialog.asksaveasfilename(defaultextension='.lil',initialfile='')

        self.file_save(file_to_save=file_to_save)
        self.filemenu.entryconfigure(2, state=tk.NORMAL)
        self.root.bind("<Command-s>", lambda x:self.file_save())

        self.filename=file_to_save

    def luanch_preferences(self,event=None):
        print("luanch_preferences")



if __name__ == "__main__":

    main_root=tk.Tk()
    main_root.withdraw()
    window_list=[]


    LadderLogic(main_root,window_list)
    
    main_root.mainloop()