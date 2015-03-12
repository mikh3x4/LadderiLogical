import tkinter.ttk as ttk
import tkinter as tk
class IOBoard(ttk.Frame):

    forbiden_chars=["'",'"',"[","]","{","}",","]
    def __init__(self,root,app):
        ttk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.output_list=[]
        self.input_list=[]


        ttk.Label(master=self,text="Outputs").grid(column=1,row=0)
        ttk.Label(master=self,text="Inputs").grid(column=2,row=0)

        v2cmd = (self.root.register(self.validate_2),'%S','%d')

        for x in range(8):
            a=ttk.Entry(master=self,width=10,validate="key",validatecommand=v2cmd)
            a.grid(column=1,row=x+1)
            a.insert(0,'1')
            b=ttk.Label(master=self,text='0')
            b.grid(column=0,row=x+1)
            self.output_list.append([a,b])

        for x in range(8):

            vcmd = (self.root.register(self.validate), '%P','%S','%d',x)

            def temp(r):
                def invcmd():
                    self.input_list[r][0].delete(0,tk.END)
                    self.input_list[r][0].insert(0,self.input_list[r][2])
                    self.input_list[r][0].config(validate="key")
                return invcmd

            a=ttk.Entry(master=self,width=10,validate="none",validatecommand=vcmd,invalidcommand=temp(x))
            a.grid(column=2,row=x+1)
            name=str(x+1)+"io"
            a.delete(0,tk.END)
            a.insert(0,name)
            self.app.board.flags[name]=[None,0]
            c=tk.IntVar()
            b=ttk.Checkbutton(master=self,variable=c)
            b.grid(column=3,row=x+1)
            a.config(validate="key")
            self.input_list.append([a,c,name])

    def save_to_file(self):
        out={}

        out["inputs"]=[x[2] for x in self.input_list]
        out["outputs"]=[x[0].get() for x in self.output_list]
        return out


    def load_from_file(self,data):

        assert(len(data["inputs"])==8)
        assert(len(data["outputs"])==8)

        for i in range(8):
            self.input_list[i][2]=data["inputs"][i]
            self.input_list[i][0].config(validate="none")
            self.input_list[i][0].delete(0,tk.END)
            self.input_list[i][0].insert(0,data["inputs"][i])
            self.input_list[i][0].config(validate="key")
            self.app.board.flags[self.input_list[i][2]]=[None,0]

        for i in range(8):
            self.output_list[i][0].config(validate="none")
            self.output_list[i][0].delete(0,tk.END)
            self.output_list[i][0].insert(0,data["outputs"][i])

        if(len(data)!=2): #inputs outputs
            print("File contains unimplemented feature in IOBoard")


    def validate_2(self,S,d):

        if(d=="1" and S in self.forbiden_chars):
            return False
        return True


    def validate(self, P,S,d,n):

        if(d=="1" and S in self.forbiden_chars):
            return False

        n=int(n)
        del self.app.board.flags[self.input_list[n][2]]
        self.input_list[n][2]=P
        try:
            self.app.board.flags[self.input_list[n][2]]
        except KeyError:
            self.app.board.flags[self.input_list[n][2]]=[None,0]
            return True

        i=1
        try:
            while 1:
                self.app.board.flags[self.input_list[n][2]+"."+str(i)]
                i+=1
        except KeyError:
            self.input_list[n][2]=self.input_list[n][2]+"."+str(i)
            self.app.board.flags[self.input_list[n][2]]=[None,0]


        return False



    def update(self):

        for x in self.output_list:
            try:
                x[1].config(text=str(self.app.board.flags[x[0].get()][1]))
            except KeyError:
                x[1].config(text="?")

        for x in self.input_list:
            self.app.board.flags[x[2]][1]=x[1].get()

class DirectionSelector(tk.Canvas):

    def __init__(self,root,conector_ints):

        self.root=root
        size=100
        super().__init__(root,width=size, height=size, background="#7A7A7a")

        self.xview_moveto(0)
        self.yview_moveto(0)

        self.conector_ints=conector_ints

        self.buttons=[]
        self.buttons.append(self.create_polygon(0,0,size/2,size/2,size,0,fill="#FF0000",outline="#EEEEEE"))
        self.buttons.append(self.create_polygon(size,0,size/2,size/2,size,size,fill="#FF0000",outline="#EEEEEE"))
        self.buttons.append(self.create_polygon(size,size,size/2,size/2,0,size,fill="#FF0000",outline="#EEEEEE"))
        self.buttons.append(self.create_polygon(0,0,size/2,size/2,0,size,fill="#FF0000",outline="#EEEEEE"))

        for i in range(len(self.buttons)):
            def generate_func(r):
                return lambda event: self.triangle_click(r)

            self.tag_bind(self.buttons[i],'<ButtonPress-1>',generate_func(i))



    def triangle_click(self,i):

        print('calc')
        if(self.conector_ints[i].get()==1):
            self.itemconfig(self.buttons[i],fill="#00FF00")
            self.conector_ints[i].set(0)

        elif(self.conector_ints[i].get()==0):
            self.itemconfig(self.buttons[i],fill="#FF0000")
            self.conector_ints[i].set(1)

        print(self.conector_ints[i])


class ToolBox(ttk.Frame):


    def __init__(self,root,app):
        ttk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.tool="select"

        self.select=ttk.Button(master=self,text="Select",command=lambda:self.change_tool("select"))
        self.horizontal=ttk.Button(master=self,text="Horizontal",command=lambda:self.change_tool("horizontal"))
        self.hswitch=ttk.Button(master=self,text="HSwitch",command=lambda:self.change_tool("hswitch"))
        self.delete=ttk.Button(master=self,text="Delete",command=lambda:self.change_tool("delete"))
        self.flag=ttk.Button(master=self,text="Flag",command=lambda:self.change_tool("flag"))
        self.auto=ttk.Button(master=self,text="Auto",command=lambda:self.change_tool("auto"))

        self.select.grid(row=0,column=0)
        self.auto.grid(row=0,column=1)
        self.delete.grid(row=0,column=2)
        self.horizontal.grid(row=0,column=3)
        self.hswitch.grid(row=0,column=4)
        self.flag.grid(row=0,column=5)



    def change_tool(self,name):
        print("changed to "+name)
        self.app.board.previous_shift_comand=False
        self.tool=name


if __name__ == '__main__':
    test=tk.Tk()

    c=DirectionSelector(test,[1,1,1,1])
    c.pack()
    test.mainloop()