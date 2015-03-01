import tkinter as tk

class IOBoard(tk.Frame):


    def __init__(self,root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.output_list=[]
        self.input_list=[]


        tk.Label(master=self,text="Outputs").grid(column=1,row=0)
        tk.Label(master=self,text="Inputs").grid(column=2,row=0)

        for x in range(8):
            a=tk.Entry(master=self,width=10)
            a.grid(column=1,row=x+1)
            a.insert(0,'1')
            b=tk.Label(master=self,text='0')
            b.grid(column=0,row=x+1)
            self.output_list.append([a,b])

        for x in range(8):

            vcmd = (self.root.register(self.validate), '%P',x)

            def temp(r):
                def invcmd():
                    print("::",r)
                    self.input_list[r][0].delete(0,tk.END)
                    self.input_list[r][0].insert(0,self.input_list[r][2])
                    self.input_list[r][0].config(validate="key")
                return invcmd

            a=tk.Entry(master=self,width=10,validate="none",validatecommand=vcmd,invalidcommand=temp(x))
            a.grid(column=2,row=x+1)
            name=str(x+1)+"io"
            a.delete(0,tk.END)
            a.insert(0,name)
            self.app.board.flags[name]=[None,0]
            c=tk.IntVar()
            b=tk.Checkbutton(master=self,variable=c)
            b.grid(column=3,row=x+1)
            a.config(validate="key")
            self.input_list.append([a,c,name])


    def validate(self, P,n):
        print("validated",n)

        n=int(n)
        del self.app.board.flags[self.input_list[n][2]]
        self.input_list[n][2]=P
        try:
            self.app.board.flags[self.input_list[n][2]]
        except KeyError:
            self.app.board.flags[self.input_list[n][2]]=[None,0]
            return True
        print('modding')
        i=1
        try:
            while 1:
                self.app.board.flags[self.input_list[n][2]+"."+str(i)]
                i+=1
        except KeyError:
            self.input_list[n][2]=self.input_list[n][2]+"."+str(i)
            self.app.board.flags[self.input_list[n][2]]=[None,0]
        print(self.input_list[n][2])

        return False



    def update(self):

        for x in self.output_list:
            try:
                x[1].config(text=str(self.app.board.flags[x[0].get()][1]))
            except KeyError:
                x[1].config(text="?")

        for x in self.input_list:
            # print(x[2])
            self.app.board.flags[x[2]]=[None,x[1].get()]




class ToolBox(tk.Frame):


    def __init__(self,root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.tool="select"

        self.select=tk.Button(master=self,text="Select",command=lambda:self.change_tool("select"))
        self.horizontal=tk.Button(master=self,text="Horizontal",command=lambda:self.change_tool("horizontal"))
        self.hswitch=tk.Button(master=self,text="HSwitch",command=lambda:self.change_tool("hswitch"))

        self.select.grid(row=0,column=0)
        self.horizontal.grid(row=0,column=1)
        self.hswitch.grid(row=0,column=2)


    def change_tool(self,name):
        print("changed to "+name)
        self.tool=name

