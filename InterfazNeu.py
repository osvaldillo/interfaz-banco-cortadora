import sys 
import cv2 
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import serial
import time

class Thread(QThread):
    available = pyqtSignal(bool)
    a0Changed = pyqtSignal(bool)
    a1Changed = pyqtSignal(bool)
    b1Changed = pyqtSignal(bool)
    def __init__(self):
        super(Thread, self).__init__()
        self.setConnection()
    def setConnection(self):
        ports = [f'COM{i}' for i in range(4, 12)]
        for port in ports:
            with serial.Serial() as self.board:
                self.board.port = port
                try:
                    self.board.close()
                    self.board = serial.Serial(port, 115200)
                    self.conected= True
                    print("Succesfully connected to serial port")
                    break
                except serial.serialutil.SerialException:
                    continue
        else:
            print("Failed trying to connect to serial")
            self.conected = False
        return self.conected
    def disconnect(self):
        ports = [f'COM{i}' for i in range(4, 12)]
        for port in ports:
            with serial.Serial() as self.board:
                self.board.port = port
                try:
                    self.board.close()
                    break
                except serial.serialutil.SerialException:
                    continue
        else:
            print("No ports found")
        return True



    def run(self):
        while True:
            try:
                if self.board.in_waiting > 0:
                    self.available.emit(True)
                    time.sleep(0.2)

            except serial.serialutil.SerialException:
                pass

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

        self.thread= Thread()
        self.thread.available.connect(self.getData)
        self.thread.start()
        self.enableSerialConnection()

        self.AdvanceA.clicked.connect(self.sendData)
        self.AdvanceB.clicked.connect(self.sendData)
        self.RecoilA.clicked.connect(self.sendData)
        self.RecoilB.clicked.connect(self.sendData)
        self.Auto.clicked.connect(self.sendData)
        self.connectionButton.clicked.connect(self.enableSerialConnection)
        self.disconnectionButton.clicked.connect(self.disableSerialConnection)
        self.horizontalSlider.valueChanged.connect(self.sendData)
        
        self.GotoInstruct.setText("Instructions")
        self.GotoControls.setText("Controls")
    def enableSerialConnection(self):
        if self.thread.setConnection():
            pass
            self.connectionStateLabel.setText(f'Connected on {self.thread.board.port} port')
            self.connectionButton.setEnabled(False)
            self.disconnectionButton.setEnabled(True)
            self.AdvanceA.setEnabled(True)
            self.AdvanceB.setEnabled(True)
            self.RecoilA.setEnabled(True)
            self.RecoilB.setEnabled(True)
            self.Auto.setEnabled(True)
            #print("Enviado")
    def disableSerialConnection(self):
        if self.thread.disconnect():
            pass
            self.connectionStateLabel.setText(f'Not connected')
            self.connectionButton.setEnabled(True)
            self.AdvanceA.setEnabled(False)
            self.AdvanceB.setEnabled(False)
            self.RecoilA.setEnabled(False)
            self.RecoilB.setEnabled(False)
            self.Auto.setEnabled(False)
            self.disconnectionButton.setEnabled(False)
            self.thread.disconnect()
            #print("Desconectado")

    def sendData(self):
        if self.sender() == self.AdvanceA: send = 'A+'
        elif self.sender() == self.AdvanceB: send = 'B+'
        elif self.sender() == self.RecoilA: send = 'A-'
        elif self.sender() == self.RecoilB: send = 'B-'
        elif self.sender() == self.Auto: send = 'Start secuence'
        elif self.sender() == self.horizontalSlider: send = f'flow {self.horizontalSlider.value()}'
        self.thread.board.write((send + '\r').encode())


    def getData(self):
        if self.sender().available:
            receivedText = str(self.thread.board.readline())
            print(receivedText)
            if receivedText[6] == "0" and receivedText[12] == "1":
                self.AdvanceA.setEnabled(False)
                self.RecoilA.setEnabled(True)
            elif receivedText[6] == "0" and receivedText[12] == "0":
                self.AdvanceA.setEnabled(True)
                self.RecoilA.setEnabled(True)
            elif receivedText[6] == "1" and receivedText[12] == "0":
                self.AdvanceA.setEnabled(True)
                self.RecoilA.setEnabled(False)
            if receivedText[18] == "0":
                self.RecoilB.setEnabled(True)
                self.AdvanceB.setEnabled(False)
            else:
                self.RecoilB.setEnabled(False)
                self.AdvanceB.setEnabled(True)
        else:
            print("Couldn't get data")

    def updateActivationButtons(self):
        if self.thread.sensorA0 == '1' and self.thread.sensorA1 == '0':
            self.RecoilA.setEnabled(False)
            self.AdvanceA.setEnabled(True)
        elif self.thread.sensorA0 == '0' and self.thread.sensorA1 == '1':
            self.RecoilA.setEnabled(True)
            self.AdvanceA.setEnabled(False)
        if self.thread.sensorB1 == '1':
            self.RecoilB.setEnabled(True)
            self.AdvanceB.setEnabled(False)
        else:
            self.RecoilB.setEnabled(False)
            self.AdvanceB.setEnabled(True)

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
