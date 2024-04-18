import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLCDNumber, QLabel,QMenuBar,  QStatusBar, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
import serial
class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Vegetable_Cutter.ui", self)
        self.setWindowTitle("Vegetable cutter")
        #self.setGeometry(0, 0, 1500, 700)
        self.conectar()
        self.botonConectar.clicked.connect(self.conectar)
        self.botonCilindroEmpujador.clicked.connect(self.enviar)
        self.botonGuillotina.clicked.connect(self.enviar)

    def conectar(self, bt='Conectar'):
        try: btnTxt = self.sender().text()
        except: btnTxt = bt
        #Conectar
        if btnTxt == "Conectar":
            puertos = [f'COM{i}' for i in range(4, 12)]

            for puerto in puertos:
                with serial.Serial() as self.placa:
                    self.placa.port = puerto
                    try:
                        #self.placa.close()
                        self.placa = serial.Serial(puerto, 9600)
                        self.conectado = True
                        self.botonConectar.setText("Desconectar")
                        self.labelConexion.setText(f'Conectado en {self.placa.port}')
                        print(self.conectado)
                        break
                    except serial.serialutil.SerialException:
                        continue
            else:
                print("No se encuentra ningun puerto")
                self.labelConexion.setText(f'No se encuentra ningun puerto')
                self.conectado = False
        #Desconectar
        else:
            puertos = [f'COM{i}' for i in range(4, 12)]
            for puerto in puertos:
                with serial.Serial() as placa:
                    placa.port = puerto
                    try:
                        placa.close()
                        self.conectado = False
                        self.botonConectar.setText("Conectar")
                        self.labelConexion.setText(f'Desconectado')
                        print(self.conectado)
                        break
                    except serial.serialutil.SerialException:
                        continue
            else:
                print("No hay nada conectado")
                self.labelConexion.setText(f'No se encuentra ningun puerto')
                self.conectado = False

    def enviar(self):
        if self.sender() == self.botonCilindroEmpujador: send = 'C'
        elif self.sender() == self.botonGuillotina: send = 'G'
        else: print("No digas mmds")
        if self.conectado:
            if self.sender().text() == "Extender":
                self.placa.write(f'E{send}'.encode())
                self.sender().setText("Contraer")
            else:
                self.placa.write(f'C{send},'.encode())
                self.sender().setText("Extender")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    app.exec_()