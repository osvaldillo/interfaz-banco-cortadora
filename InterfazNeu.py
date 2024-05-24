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
        ports = [f'COM{i}' for i in range(4, 15)]
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
        ports = [f'COM{i}' for i in range(4, 15)]
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
        self.SliderHardness.valueChanged.connect(self.sendData)

        self.GotoInstruct.setText("Instrucciones")
        self.GotoControls.setText("Controles")

        self.autoFunInfo.clicked.connect(self.setInfo)
        self.rebanar.clicked.connect(self.setInfo)
        self.sliceInfo.clicked.connect(self.setInfo)
        self.hardInfo.clicked.connect(self.setInfo)
        self.advRecoInfo.clicked.connect(self.setInfo)
        self.sensorInfo.clicked.connect(self.setInfo)
        self.protocolInfo.clicked.connect(self.setInfo)
        self.instructInfo.clicked.connect(self.setInfo)

    def setInfo(self):
        if self.sender() == self.autoFunInfo:
            self.showInfo = "Cuando presiones este botón, la máquina comenzará a realizar cortes de manera automática, con los parámetros de corte establecidos. Si el cilindro está inicialmente extendido, primero se retraerá."
        elif self.sender() == self.rebanar:
            self.showInfo = "Este botón permite realizar un único corte al vegetal para corroborar el grosor de la rebanada."
        elif self.sender() == self.sliceInfo:
            self.showInfo = "Mueve este slider de manera suave. Sirve para calibrar la apertura de las llaves del cilindro, haciendo rebanadas más o menos gruesas."
        elif self.sender() == self.hardInfo:
            self.showInfo =  "Mueve este slider de manera suave. Sirve para calibrar la presión suministrada a la guillotina. Ajustala si es necesaria más presión."
        elif self.sender() == self.advRecoInfo:
            self.showInfo = "Los botones de avance y retroceso permiten mover los cilindros a sus posiciones máximas o mínimas manualmente. No se pueden usar mientras una secuencia se ejecuta."
        elif self.sender() == self.sensorInfo:
            self.showInfo = "Los sensores en el banco habilitan los botónes posibles en la interfaz. Por ejemplo, si un sensor indica que el cilindro de corte está retraído, deshabilitará el botón <Retraer> de ese cilindro."
        elif self.sender() == self.protocolInfo:
            self.showInfo = """
--Para limpiar el banco, asegúrese de desconectar todas las fuentes de alimentación: corriente eléctrica y presión neumática. 
--Limpie las partes electrónicas únicamente con alcohol isopropílico y un trapo. 
--Desmonte la guillotina, límpiela con jabón de grado alimenticio y desinfecte. Así mismo con el canal de los vegetales."""
        elif self.sender() == self.instructInfo:
            self.showInfo = """
--Conecte un cable USB a la placa de control del banco y presione el botón <Conectar> en esta interfaz. 
--Conecte el banco a una alimentación de 12Vcc. Suministre aire comprimido a una presión máxima de 6 bar. 
--Presione el botón verde para habilitar los cilindros, y el rojo para deshabilitarlos (usese el botón rojo como paro de emergencia). 
--Coloque un vegetal en el canal del banco. 
--Confiqure los parámetros de corte usando los deslizadores horizontales de esta interfaz. 
--Presione el botón <Comenzar Secuencia> de esta interfaz, y espere a que termine de realizar el corte. 
--Repita el proceso con todos sus vegetales. Al final de su uso, asegúrese de que los cilindros se encuentren en su posición retraída. 
--Antes de retirar sus alimentos, asegúrese de presionar el botón rojo. 
--Retire todas las fuentes de alimentación: eléctrica y neumática."""
        self.Images.setText(self.showInfo)

    def enableSerialConnection(self):
        if self.thread.setConnection():
            pass
            self.connectionStateLabel.setText(f'Conectado en puerto {self.thread.board.port}')
            self.connectionButton.setEnabled(False)
            self.disconnectionButton.setEnabled(True)
            self.AdvanceA.setEnabled(True)
            self.AdvanceB.setEnabled(True)
            self.RecoilA.setEnabled(True)
            self.RecoilB.setEnabled(True)
            self.Auto.setEnabled(True)
            #self.stop.setEnabled(True)
            self.slicingButton.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.SliderHardness.setEnabled(True)
            self.warningsLabel.setText('')


            #print("Enviado")
    def disableSerialConnection(self):
        if self.thread.disconnect():
            pass
            self.connectionStateLabel.setText(f'No conectado')
            self.connectionButton.setEnabled(True)
            self.AdvanceA.setEnabled(False)
            self.AdvanceB.setEnabled(False)
            self.RecoilA.setEnabled(False)
            self.RecoilB.setEnabled(False)
            self.Auto.setEnabled(False)
            self.disconnectionButton.setEnabled(False)
            #self.stop.setEnabled(False)
            self.slicingButton.setEnabled(False)
            self.horizontalSlider.setEnabled(False)
            self.SliderHardness.setEnabled(False)
            self.thread.disconnect()
            #print("Desconectado")

    def sendData(self):
        if self.sender() == self.AdvanceA: send = 'A+'
        elif self.sender() == self.AdvanceB: send = 'B+'
        elif self.sender() == self.RecoilA: send = 'A-'
        elif self.sender() == self.RecoilB: send = 'B-'
        elif self.sender() == self.Auto:
            send = 'S'
            self.AdvanceA.setEnabled(False)#borrar si es necesario
            self.AdvanceB.setEnabled(False)
            self.RecoilA.setEnabled(False)
            self.RecoilB.setEnabled(False)
            self.Auto.setEnabled(False)
            self.slicingButton.setEnabled(False)
            self.horizontalSlider.setEnabled(False)
            self.SliderHardness.setEnabled(False)
        elif self.sender() == self.horizontalSlider:
            send = f'F {self.horizontalSlider.value()}'
            time.sleep(0.01)
        elif self.sender() == self.SliderHardness:
            send = f'P {self.SliderHardness.value()}'
            time.sleep(0.01)
        elif self.sender() == self.slicingButton: send = 'C'
        print(send)
        try:
            self.thread.board.write((send + '\r\n').encode())
        except:
            self.disableSerialConnection()
            self.warningsLabel.setText('Placa desconectada')


    def getData(self):
        if self.sender().available:
            receivedText = str(self.thread.board.readline())
            print(receivedText)
            if "Traceback" in receivedText:
                self.warningsLabel.setText("Error en el código de la placa")
            elif "fin" in receivedText: #borrar si es necesario
                self.AdvanceA.setEnabled(True)
                self.AdvanceB.setEnabled(True)
                self.RecoilA.setEnabled(True)
                self.RecoilB.setEnabled(True)
                self.Auto.setEnabled(True)
                self.slicingButton.setEnabled(True)
                self.horizontalSlider.setEnabled(True)
                self.SliderHardness.setEnabled(True)
            else:
                if receivedText[6] == "0" and receivedText[12] == "1":
                    self.AdvanceA.setEnabled(False)
                    self.RecoilA.setEnabled(True)
                    self.thread.board.write(('A*' + '\r\n').encode())
                elif receivedText[6] == "0" and receivedText[12] == "0":
                    self.AdvanceA.setEnabled(True)
                    self.RecoilA.setEnabled(True)
                elif receivedText[6] == "1" and receivedText[12] == "0":
                    self.AdvanceA.setEnabled(True)
                    self.RecoilA.setEnabled(False)
                    self.thread.board.write(('A*' + '\r\n').encode())
                try:
                    if receivedText[18] == "0":
                        self.RecoilB.setEnabled(True)
                        self.AdvanceB.setEnabled(False)
                    else:
                        self.RecoilB.setEnabled(False)
                        self.AdvanceB.setEnabled(True)
                except IndexError:
                    print(receivedText)
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

    def Instruction(self):
        self.stackedWidget.setCurrentWidget(self.Instructions)
        self.GotoControls.clicked.connect(self.Control)
        self.Images.setText("Selecciona un botón para conocer información sobre un tema")
            
        
app=QApplication(sys.argv)
ventana=Window()
ventana.show()
app.exec_()
