import sys 
import cv2 
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import serial
import time

class Hilo(QThread):
    available = pyqtSignal(bool)
    def __init__(self):
        super(Hilo, self).__init__()
        self.setConnection()
    def setConnection(self):
        ports = [f'COM{i}' for i in range(4, 12)]
        for port in ports:
            with serial.Serial() as self.board:
                self.board.port = port
                try:
                    self.board.close()
                    self.board = serial.Serial(port, 9600)
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
                    time.sleep(0.1)
            except serial.serialutil.SerialException:
                pass

class Window(QMainWindow): 
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ProyectoNeu.ui",self) 
        
        self.setWindowTitle("Pneumatic Interface")
        self.Start()
        self.setConnection()
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

        self.AdvanceA.clicked.connect(self.sendData)
        self.AdvanceB.clicked.connect(self.sendData)
        self.RecoilA.clicked.connect(self.sendData)
        self.RecoilB.clicked.connect(self.sendData)
        self.Auto.clicked.connect(self.sendData)
        self.connectionButton.clicked.connect(self.setConnection)
        self.horizontalSlider.valueChanged.connect(self.sendData)
        
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

    def setConnection(self, bt='Connect'):
        try: btnTxt = self.sender().text()
        except: btnTxt = bt
        #Conectar
        if btnTxt == "Connect":
            ports = [f'COM{i}' for i in range(4, 12)]

            for port in ports:
                with serial.Serial() as self.board:
                    self.board.port = port
                    try:
                        #self.placa.close()
                        self.board = serial.Serial(port, 9600)
                        self.conected = True
                        self.connectionButton.setText("Disconnect")
                        self.connectionStateLabel.setText(f'Connected on {self.board.port}')
                        #print(self.cone)
                        break
                    except serial.serialutil.SerialException:
                        continue
            else:
                print("Port nor found")
                self.connectionStateLabel.setText(f'Port not found.')
                self.conected = False
        #Desconectar
        else:
            ports = [f'COM{i}' for i in range(4, 12)]
            for port in ports:
                with serial.Serial() as board:
                    board.port = port
                    try:
                        board.close()
                        self.conected = False
                        self.connectionButton.setText("Connect")
                        self.connectionStateLabel.setText(f'Disconnected')
                        #print(self.conectado)
                        break
                    except serial.serialutil.SerialException:
                        continue
            else:
                #print("No hay nada conectado")
                self.labelConexion.setText(f'Port not found.')
                self.conected = False

    def sendData(self):
        if self.conected:
            if self.sender() == self.AdvanceA: send = 'A+'
            elif self.sender() == self.AdvanceB: send = 'B+'
            elif self.sender() == self.RecoilA: send = 'A-'
            elif self.sender() == self.RecoilB: send = 'B-'
            elif self.sender() == self.Auto: send = 'Start secuence'
            elif self.sender() == self.horizontalSlider: send = f'flow({self.horizontalSlider.value()})'
            self.board.write(f'{send},'.encode())
            
        
app=QApplication(sys.argv)
ventana=Window()
ventana.show()
app.exec_()
