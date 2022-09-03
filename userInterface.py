from threading import Thread
from PyQt4 import QtGui, QtCore
import zmq, sys, json, time
from functools import partial

# the user interface, written in PyQT 4
# The GUI is designed to interact with the user. It also connects with the robot control (main.py).

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.readjson()
        
        self.mapwin = MapWindow()  
        
        self.l1 = QtGui.QLabel('Welcome! I am the concierge. Feel free to talk with me!', self)
        self.l1.setFont(QtGui.QFont('Bold', 40))
        self.l1.resize(1500, 60)
        self.l1.move(200, 100)  
        
        self.mapbt = QtGui.QPushButton('Map', self)
        self.mapbt.setFont(QtGui.QFont('Bold', 40))
        self.mapbt.adjustSize()
        self.mapbt.move(200, 300) 
        self.mapbt.clicked.connect(self.map_clicked) 
        
        # Generate buttons and direction-windows in batch dynamically, according to JSON file
        self.destination = [' ' for i in range(self.numLocation)] 
        self.route = [' ' for i in range(self.numLocation)]
        self.dirbt = [' ' for i in range(self.numLocation)] 
        self.dirwin = [' ' for i in range(self.numLocation)]           
        
        for i in range(self.numLocation):
            self.destination[i] = self.jsondata['map'][i]["destination"]     
            self.route[i] = self.jsondata['map'][i]["route"]
            
            self.dirwin[i] = DirectionWindow(self.route[i])
            
            self.dirbt[i] = QtGui.QPushButton(self.destination[i], self)
            self.dirbt[i].setFont(QtGui.QFont('Bold', 40))
            self.dirbt[i].adjustSize()
            self.dirbt[i].move(200, 400 + i * 100) 
            self.dirbt[i].clicked.connect(partial(self.dir_clicked, self.dirwin[i])) 
 
        self.setWindowTitle('Concierge')  
        self.showMaximized()
        
        # run the server thread       
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.update_progress.connect(self.reactToMSG)
        
        
    # handle the signal from the server thread
    def reactToMSG(self, msg):
          
        # reaction to msg
        if "where am i" in msg:
            self.mapwin.showMaximized()
            usergui.hide() 
            for i in range(self.numLocation):
                self.dirwin[i].hide()   
        elif "bar" in msg:
            destid = self.destination.index('bar')
            self.dirwin[destid].showMaximized()
            usergui.hide() 
            self.mapwin.hide()
        elif "robot battle event" in msg or "robot battery event" in msg:
            destid = self.destination.index('The robot battle event!')
            self.dirwin[destid].showMaximized()
            usergui.hide() 
            self.mapwin.hide()
        elif "thank you" in msg or "thanks" in msg or "sex" in msg or "6" in msg or "fix" in msg:
            usergui.show() 
            self.mapwin.hide()
            for i in range(self.numLocation):
                self.dirwin[i].hide()  
        
    def readjson(self):
        f = open('userInterface.json')
        self.jsondata = json.load(f)  
        self.numLocation = len(self.jsondata['map'])    # location & direction lists recorded in json          
        f.close 
        
      
    def map_clicked(self):
        self.mapwin.showMaximized()
        usergui.hide()

             
    def dir_clicked(self, window):
        window.showMaximized()
        usergui.hide()
        
    
class WorkerThread(QtCore.QThread):
    update_progress = QtCore.pyqtSignal(str)    # signal
    
    # communication with robot control (userInterface.py is server)
    def run(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        
        # listen to message from the client
        try:
            while True:
                message = self.socket.recv()        # receive msg from robot
                self.socket.send(b"ack")
                
                self.update_progress.emit(message)  # send msg to the main thread      
        except:
            print("Server error detected")
       

class MapWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MapWindow, self).__init__()
        
        self.l1 = QtGui.QLabel(self)
        self.mapimg = QtGui.QPixmap('superfloor map.png')
        self.l1.setPixmap(self.mapimg)
        self.l1.resize(self.mapimg.width(), self.mapimg.height())
        self.l1.move(350, 100)
               
        self.b1 = QtGui.QPushButton('Back', self)
        self.b1.setFont(QtGui.QFont('Bold', 40))
        self.b1.resize(200, 60)
        self.b1.move(100, 900) 
        self.b1.clicked.connect(self.b1_clicked) 

        self.setWindowTitle('Map')  


    def b1_clicked(self):
        self.hide()
        usergui.show()


class DirectionWindow(QtGui.QMainWindow):
    
    def __init__(self, route):
        super(DirectionWindow, self).__init__()
        
        self.l1 = QtGui.QLabel(route, self)
        self.l1.setFont(QtGui.QFont('Bold', 40))
        self.l1.adjustSize()
        self.l1.move(200, 100)
               
        self.dirb1 = QtGui.QPushButton('Back', self)
        self.dirb1.setFont(QtGui.QFont('Bold', 40))
        self.dirb1.resize(200, 60)
        self.dirb1.move(100, 900) 
        self.dirb1.clicked.connect(self.dirb1_clicked) 

        self.setWindowTitle('Direction')  


    def dirb1_clicked(self):
        self.hide()
        usergui.show()
        
        
if __name__ == "__main__":
    app = QtGui.QApplication([])
    usergui = MainWindow()
    usergui.show()
    app.exec_()    