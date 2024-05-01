import sys 
import cv2 
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap 

class Window(QMainWindow): 
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ProyectoNeu.ui",self) 
        
        self.setWindowTitle("Pneumatic Interface")
        self.Start() 
        self.setStyleSheet('background-color: #55557f')  
        
        # self.img_cil = QPixmap('CilindroSF.png')  
        # self.label_5.setPixmap(self.img_cil)
        self.label_5.setStyleSheet('border-image : url(CilindroSF1.png);')
        self.label_6.setStyleSheet('border-image : url(CilindroSF1.png);')
        self.label_9.setStyleSheet('border-image : url(CilindroSF1.png);')
        self.label_4.setStyleSheet('border-image : url(CilindroSF1.png);')
        self.Carrot.setStyleSheet('border-image : url(Carrot.png);')
        self.Cucumber.setStyleSheet('border-image : url(Cucumber.png);')
        self.Ban.setStyleSheet('border-image : url(Ban.png);') 
        
        self.GotoInstruct.setText("Instructions")
        self.GotoControls.setText("Controls")

        
    def Start(self): 
        self.stackedWidget.setCurrentWidget(self.Controls)
        self.GotoInstruct.clicked.connect(self.Instruction)
        
    def Control(self): 
        self.stackedWidget.setCurrentWidget(self.Controls)
        self.GotoInstruct.clicked.connect(self.Instruction)

    def Status(self): 
        pass 
    def Instruction(self): 
        self.stackedWidget.setCurrentWidget(self.Instructions) 
        self.GotoControls.clicked.connect(self.Control)
            
        
app=QApplication(sys.argv)
ventana=Window()
ventana.show()
app.exec_()
