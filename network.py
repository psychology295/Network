import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as f

class Cable:
    def __init__(self,name):
        self.name = name
        self.connection=[0,0]
    def connect(self,address):
        for c in range(len(self.connection)):
            if self.connection[c]==0:
                self.connection[c]=address
                return 1
    def disconnect(self,address):
        for c in range(len(self.connection)):
            if self.connection[c]==address:
                self.connection[c]=0
                return 1
        print("cannot connect")

class Computer:
    def __init__(self,name):
        self.name = name
        self.connection=0
        
    def connect(self,address):
        if address.connect(self.name)==1:
            self.connection=address.name
        print(self.connection)
        
    def disconnect(self,address):
        if address.disconnect(self.name)==1:
            self.connection=0
        print(self.connection)
            
class Application(tk.Frame):
    def __init__(self,root,c):
        super().__init__(root,
            width=420,height=100,
            borderwidth=4,relief='groove')
        self.pack()
        self.pack_propagate(0)
        self.root=root
        self.create_widgets(c)

        
    def create_widgets(self,c):
        name_lbl=tk.Label(self, justify="center",text=c.name)
        name_lbl.pack()
        
        self.lbl=tk.StringVar()
        self.lbl.set(f'connect:{c.connection}')
        connect_lbl=tk.Label(self, justify="center",textvariable=self.lbl)
        connect_lbl.pack()

        connect_btn=tk.Button(self)
        connect_btn['text']='Connect'
        
        connect_btn['command']=lambda:self.connect(c,cable1)
        connect_btn.pack()
        
        disconnect_btn=tk.Button(self)
        disconnect_btn['text']='Disconnect'
        disconnect_btn['command']=lambda:self.disconnect(c,cable1)
        disconnect_btn.pack()

            
    def connect(self,c,address):
        c.connect(address)
        self.lbl.set(f'connect:{c.connection}')

    def disconnect(self,c,address):
        c.disconnect(address)
        self.lbl.set(f'connect:{c.connection}')

class SelectCable(tk.Frame):
    def __init__(self,root):
        super().__init__(root,
            width=420,height=100,
            borderwidth=4,relief='groove')
        self.pack()
        self.pack_propagate(0)
        self.root=root
        self.create_widgets()

        
    def create_widgets(self):
        name_lbl=tk.Label(self, justify="center",text='Cable')
        name_lbl.pack()
        

            
    def connect(self,c,address):
        c.connect(address)
        self.lbl.set(f'connect:{c.connection}')

    def disconnect(self,c,address):
        c.disconnect(address)
        self.lbl.set(f'connect:{c.connection}')


com1=Computer("YaginumaPC")
com2=Computer("FukuharaPC")
comList=[com1,com2]
cable1=Cable("Cable1")

App = tk.Tk()
App.geometry("300x500")
App.title('com1')
for c in comList:
    app=Application(root=App,c=c)
SelectCable=SelectCable(root=App)    
App.mainloop()