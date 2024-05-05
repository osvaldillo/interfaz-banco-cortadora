import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import serial



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
                    time.sleep(1)
            except serial.serialutil.SerialException:
                pass

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("multiHilos.ui", self)
        self.setWindowTitle("Prueba multihilos")
        self.hilo = Hilo()
        self.hilo.available.connect(self.recibir)
        self.hilo.start()
        self.conectarse()

        self.botonEnviar.clicked.connect(self.enviar)
        self.botonConectar.clicked.connect(self.conectarse)
        self.botonDesconectar.clicked.connect(self.desconectarse)

    def conectarse(self):
        if self.hilo.connectar():
            self.labelConexion.setText(f'Conectado en {self.hilo.board.port}')
            self.botonDesconectar.setEnabled(True)
            self.botonEnviar.setEnabled(True)
            self.botonConectar.setEnabled(False)
            print("Enviado")

    def desconectarse(self):
        #self.hilo.board.write("P,".encode('utf-8'))
        if self.hilo.desconnectar():
            self.labelConexion.setText(f'No conectado')
            self.hilo.desconnectar()
            self.botonDesconectar.setEnabled(False)
            self.botonEnviar.setEnabled(False)
            self.botonConectar.setEnabled(True)
            print("Desconectado")

    def enviar(self):
        self.hilo.board.write("P,".encode('utf-8'))


    def recibir(self):
        if self.sender().available:
            texto = self.hilo.board.readline().decode("utf-8")
            self.labelRecepcion.setText(texto)
        else:
            print("No se pudo recibir")






app = QApplication(sys.argv)
ventana = Window()
ventana.show()
app.exec_()
