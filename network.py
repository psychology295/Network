import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as f
import os


class Initialization:
    def __init__(self):
        self.PCList=[]
        self.CableList=[]
        self.CreateCable()
        self.CreatePC()
        self.StartMainApp()
        
    def CreatePC(self):
        for pc in os.listdir(path='Device/PC'):
            self.PCList.append(Computer(pc))
        for pc_obj in self.PCList:
            f = open(f'Device/PC/{pc_obj.name}/connection.txt', 'r')
            connect_cable=f.read()
            for cable in self.CableList:    
                if connect_cable == 0:
                    break
                elif cable.name==connect_cable:
                    pc_obj.connect(cable)
            f.close()
            
    def CreateCable(self):
        for cable in os.listdir(path='Device/Cable'):
            self.CableList.append(Cable(cable))
    def StartMainApp(self):
        App = tk.Tk()
        App.geometry("300x500")
        App.title('com1')
        for c in self.PCList:
            app=Application(root=App,c=c,CableList=self.CableList)
        self.SelectCable=SelectCable(root=App,CableList=self.CableList)    
        App.mainloop()
    
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
                f = open(f'Device/PC/{address.name}/connection.txt', 'w')
                f.write(self.name)
                f.close()
                return 1

    #Deviceと切断する
    def disconnect(self,address):
        for c in range(len(self.connection)):
            if self.connection[c]==address:
                self.connection[c]=0
                f = open(f'Device/PC/{address.name}/connection.txt', 'w')
                f.write("0")
                f.close()
                return 1
        print("cannot connect")
    
    def recieveMessage(self,message,pc):
        if self.connection[0]==pc:
            recievePort=0
            sendPort=1
        elif self.connection[1]==pc:
            recievePort=1
            sendPort=0
        else:
            print("Error")
        f = open(f'Device/Cable/{self.name}/RecieveMessage.txt', 'w')
        f.write(message)
        f.close()
        self.sendMessage(self,sendPort)
        
    def sendMessage(self,message,sendPort):
        f = open(f'Device/Cable/{self.name}/RecieveMessage.txt', 'r')
        message=f.read()
        f.close()
        self.connection[sendPort].recieveMessage(message)

class Computer:
#Computerのクラス
    def __init__(self,name):
        #Computerの名前
        self.name = name
        #接続されているCable
        self.connection=0
        
    #Cableと接続する
    def connect(self,address):
        if address.connect(self)==1:
            self.connection=address
        
    #Cableと切断する
    def disconnect(self,address):
        if address.disconnect(self)==1:
            self.connection=0

    def sendMessage(self):
        f = open(f'Device/PC/{self.name}/SendMessage.txt', 'r')
        message = f.readlines()
        for line in message:
            self.connection.recieveMessage(line,self)
        f.close()
    
    def recieveMessage(self,message):
        f = open(f'Device/PC/{self.name}/RecieveMessage.txt','a')
        f.write(message)
        f.close()  
    
#MainAppに表示するDeviceのFrame
class Application(tk.Frame):
    def __init__(self,root,c,CableList):
        super().__init__(root,
            width=420,height=140,
            borderwidth=4,relief='groove')
        self.pack()
        self.pack_propagate(0)
        self.root=root
        self.create_widgets(c,CableList)

    def create_widgets(self,c,CableList):
        #Deviceの名前を表示
        name_lbl=tk.Label(self, justify="center",text=c.name)
        name_lbl.pack()
        
        #Deviceに接続しているCableの名前
        self.lbl=tk.StringVar()
        self.lbl.set(f'connect:{c.connection.name}')
        connect_lbl=tk.Label(self, justify="center",textvariable=self.lbl)
        connect_lbl.pack()

        #DeviceをCableに接続するボタン
        connect_btn=tk.Button(self)
        connect_btn['text']='Connect'        
        connect_btn['command']=lambda:self.connect(c,CableList[0])
        connect_btn.pack()
        
        #Deviceに接続されているCableを切断するボタン
        disconnect_btn=tk.Button(self)
        disconnect_btn['text']='Disconnect'
        disconnect_btn['command']=lambda:self.disconnect(c,CableList[0])
        disconnect_btn.pack()

        #DeviceのWindowを開くボタン
        browse_btn=tk.Button(self)
        browse_btn['text']='Browse'
        browse_btn['command']=lambda:self.browse(c)
        browse_btn.pack()

    #Connectボタンを押したときの処理
    def connect(self,c,address):
        c.connect(address)
        self.lbl.set(f'connect:{c.connection.name}')

    #Disconnectボタンを押したときの処理
    def disconnect(self,c,address):
        c.disconnect(address)
        self.lbl.set(f'connect:{c.connection.name}')

    #Browseボタンを押したときの処理
    def browse(self,device):
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
        connect_lbl=tk.Label(self, justify="center",text=f'connect:{c.connection.name}')
        connect_lbl.pack()

        #Messageを送るボタン
        send_btn=tk.Button(self)
        send_btn['text']='Send'
        send_btn['command']=lambda:self.sendMessage(c)
        send_btn.pack()
        

    #Connectボタンを押したときの処理
    def connect(self,c,address):
        c.connect(address)
        self.lbl.set(f'connect:{c.connection.name}')

    #Disconnectボタンを押したときの処理
    def disconnect(self,c,address):
        c.disconnect(address)
        self.lbl.set(f'connect:{c.connection.name}')

    #Browseボタンを押したときの処理
    def browse(self,device,address):
        #DeviceDialogを表示する
        DeviceDialog = tk.Tk()
        DeviceDialog.geometry("300x500")
        DeviceDialog.title(device.name)
        app=DeviceDialogApp(root=DeviceDialog,device=device)
        DeviceDialog.mainloop()

    def sendMessage(self,pc):
        pc.sendMessage()
        
    
class SelectCable(tk.Frame):
    def __init__(self,root,CableList):
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

main=Initialization()