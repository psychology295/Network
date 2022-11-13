import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as f

class Cable:
#Cableのクラス
    def __init__(self,name):
        #Cableの名前
        self.name = name
        #Cableに接続されているDevice
        self.connection=[0,0]
    
    #接続Deviceと接続する
    def connect(self,address):
    
        for c in range(len(self.connection)):
            if self.connection[c]==0:
                self.connection[c]=address
                return 1
            
    #Deviceと切断する
    def disconnect(self,address):
        for c in range(len(self.connection)):
            if self.connection[c]==address:
                self.connection[c]=0
                return 1
        print("cannot connect")

class Computer:
#Computerのクラス
    def __init__(self,name):
        #Computerの名前
        self.name = name
        #接続されているCable
        self.connection=0
        
    #Cableと接続する
    def connect(self,address):
        if address.connect(self.name)==1:
            self.connection=address.name
        print(self.connection)
        
    #Cableと切断する
    def disconnect(self,address):
        if address.disconnect(self.name)==1:
            self.connection=0
        print(self.connection)

#MainAppに表示するDeviceのFrame
class Application(tk.Frame):
    def __init__(self,root,c):
        super().__init__(root,
            width=420,height=140,
            borderwidth=4,relief='groove')
        self.pack()
        self.pack_propagate(0)
        self.root=root
        self.create_widgets(c)

    def create_widgets(self,c):
        #Deviceの名前を表示
        name_lbl=tk.Label(self, justify="center",text=c.name)
        name_lbl.pack()
        
        #Deviceに接続しているCableの名前
        self.lbl=tk.StringVar()
        self.lbl.set(f'connect:{c.connection}')
        connect_lbl=tk.Label(self, justify="center",textvariable=self.lbl)
        connect_lbl.pack()

        #DeviceをCableに接続するボタン
        connect_btn=tk.Button(self)
        connect_btn['text']='Connect'        
        connect_btn['command']=lambda:self.connect(c,cable1)
        connect_btn.pack()
        
        #Deviceに接続されているCableを切断するボタン
        disconnect_btn=tk.Button(self)
        disconnect_btn['text']='Disconnect'
        disconnect_btn['command']=lambda:self.disconnect(c,cable1)
        disconnect_btn.pack()

        #DeviceのWindowを開くボタン
        browse_btn=tk.Button(self)
        browse_btn['text']='Browse'
        browse_btn['command']=lambda:self.browse(c,cable1)
        browse_btn.pack()

    #Connectボタンを押したときの処理
    def connect(self,c,address):
        c.connect(address)
        self.lbl.set(f'connect:{c.connection}')

    #Disconnectボタンを押したときの処理
    def disconnect(self,c,address):
        c.disconnect(address)
        self.lbl.set(f'connect:{c.connection}')

    #Browseボタンを押したときの処理
    def browse(self,device,address):
        #DeviceDialogを表示する
        DeviceDialog = tk.Tk()
        DeviceDialog.geometry("300x500")
        DeviceDialog.title(device.name)
        app=DeviceDialogApp(root=DeviceDialog,device=device)
        DeviceDialog.mainloop()

#Deviceの情報を表示するダイアログ
class DeviceDialogApp(tk.Frame):
    def __init__(self,root,device):
        super().__init__(root,
            width=420,height=140,
            borderwidth=4,relief='groove')
        self.pack()
        self.pack_propagate(0)
        self.root=root
        self.create_widgets(device)
    def create_widgets(self,c):
        #Deviceの名前を表示
        name_lbl=tk.Label(self, justify="center",text=f'DeviceName:{c.name}')
        name_lbl.pack()
        
        #Deviceに接続しているCableの名前
        connect_lbl=tk.Label(self, justify="center",text=f'connect:{c.connection}')
        connect_lbl.pack()

    #Connectボタンを押したときの処理
    def connect(self,c,address):
        c.connect(address)
        self.lbl.set(f'connect:{c.connection}')

    #Disconnectボタンを押したときの処理
    def disconnect(self,c,address):
        c.disconnect(address)
        self.lbl.set(f'connect:{c.connection}')

    #Browseボタンを押したときの処理
    def browse(self,device,address):
        #DeviceDialogを表示する
        DeviceDialog = tk.Tk()
        DeviceDialog.geometry("300x500")
        DeviceDialog.title(device.name)
        app=DeviceDialogApp(root=DeviceDialog,device=device)
        DeviceDialog.mainloop()


    

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
        self.selected_radio=tk.IntVar()
        radio_1=tk.Radiobutton(self,text='Cable1',variable=self.selected_radio,value=0)
        radio_1.pack()


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