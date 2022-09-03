from PyQt4 import QtGui
import json

# the back end interface, written in PyQT 4
# The GUI is used by the real concierge as the back end.

class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.readjson()
              
        self.l1 = QtGui.QLabel('This is the admin backend', self)
        self.l1.setFont(QtGui.QFont('Bold', 40))
        self.l1.adjustSize()
        self.l1.move(200, 100)  
        
        # Add 
        self.l2 = QtGui.QLabel('Add buttons', self)
        self.l2.setFont(QtGui.QFont('Bold', 20))
        self.l2.adjustSize()
        self.l2.move(200, 300)        
        
        self.destination = QtGui.QLineEdit("Destination", self)
        self.destination.setGeometry(200, 350, 300, 50)
        self.route = QtGui.QLineEdit("Route", self)
        self.route.setGeometry(200, 400, 300, 50)

        self.b1 = QtGui.QPushButton('Add', self)
        self.b1.setFont(QtGui.QFont('Bold', 20))
        self.b1.adjustSize()
        self.b1.move(550, 410) 
        self.b1.clicked.connect(self.b1_clicked) 
        
        # Delete
        self.l3 = QtGui.QLabel('Delete buttons', self)
        self.l3.setFont(QtGui.QFont('Bold', 20))
        self.l3.adjustSize()
        self.l3.move(200, 500)
        
        self.cb = QtGui.QComboBox(self)
        for i in range(self.numLocation):
            self.cb.addItem(self.jsondata['map'][i]["destination"])
        self.cb.setGeometry(200, 550, 300, 50)
        
        self.b2 = QtGui.QPushButton('Delete', self)
        self.b2.setFont(QtGui.QFont('Bold', 20))
        self.b2.adjustSize()
        self.b2.move(550, 550) 
        self.b2.clicked.connect(self.b2_clicked)      
        
        self.setWindowTitle('Admin')  
        self.showMaximized()
        
        
    def readjson(self):
        f = open('userInterface.json')
        self.jsondata = json.load(f)    
        self.numLocation = len(self.jsondata['map'])    # location & direction lists recorded in json          
        f.close 
      

    # add a key-value pair in json
    def b1_clicked(self):
        self.jsondata['map'].append({"route": str(self.route.text()), "destination": str(self.destination.text())})
        self.writejson()
        
        self.cb.addItem(self.destination.text())
        self.destination.setText("Destination")
        self.route.setText("Route")
        
        self.dialogwin()
        

    # delete a key-value pair in json
    def b2_clicked(self):
        self.jsondata['map'].remove(next(item for item in self.jsondata['map'] if item["destination"] == self.cb.currentText()))
        self.writejson()
        
        cbid = self.cb.findText(self.cb.currentText())
        self.cb.removeItem(cbid)
        
        self.dialogwin()
        
       
    def writejson(self):
        with open('userInterface.json', 'w') as f:
            json.dump(self.jsondata, f)
            f.close
        
    
    def dialogwin(self):
        dialog = QtGui.QMessageBox()
        dialog.setText("Modification success")
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()
        
    
if __name__ == "__main__":
    app = QtGui.QApplication([])
    usergui = MainWindow()
    usergui.show()
    app.exec_()
