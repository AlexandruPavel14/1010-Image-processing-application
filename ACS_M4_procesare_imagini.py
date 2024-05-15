import sys
import cv2
import math
import numpy as np
from scipy.sparse import linalg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDialog,
    QDoubleSpinBox,
    QFontComboBox,
    QGridLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox
   
)
import statistics
 
class InterfataPrincipala(QMainWindow):
 
    def __init__(self,parent=None):
       
       
        super(InterfataPrincipala,self).__init__(parent)
        self.setWindowTitle("Algoritmi de calcul stiintific (Recunoasterea formelor) - Modul 4 - Procesare imagini")
        self.btn_poza = QPushButton('Alegere imagine')
        self.btn_poza.clicked.connect(self.getPoza)
        self.label_rezultat = QLabel(self)
        self.label_tine_minte_cale = QLabel('')
        self.poza_aleasa = QLabel()

        labelPrimaPoza = QLabel("Imaginea aleasa")
        labelAdouaPoza = QLabel("Imaginea procesata ")

        self.efect_rotire = QPushButton('Rotire imagine')
        self.efect_flip = QPushButton('Flip')
        self.efect_dilatare = QPushButton('Dilatare')
        self.efect_erodare = QPushButton('Erodare')
        self.efect_blurgaussian = QPushButton('Blur Gaussian')
        self.efect_filtrubilateral = QPushButton('Filtru bilateral')
        self.efect_medianblur = QPushButton('Median blur')
        self.efect_text = QPushButton('Adaugare text')
        self.canalcolor = QPushButton('Canal color')
        self.efect_resize = QPushButton('Redimensionare')
        self.translatare = QPushButton('Translatare imagine')
 
        self.efect_rotire.clicked.connect(self.rotire_imgagine)
        self.efect_flip.clicked.connect(self.flip_imagine)
        self.efect_filtrubilateral.clicked.connect(self.filtru_bilateral_imagine)
        self.efect_dilatare.clicked.connect(self.dilatare_imagine)
        self.efect_blurgaussian.clicked.connect(self.blur_gaussian_imagine)
        self.efect_text.clicked.connect(self.afisare_text_imagine)
        self.efect_medianblur.clicked.connect(self.median_blur_imagine)
        self.translatare.clicked.connect(self.translateaza_imagine)
        self.efect_resize.clicked.connect(self.redimensionare_imagine)
        self.efect_erodare.clicked.connect(self.erodare_imagine)
        self.canalcolor.clicked.connect(self.canale_color_imagine)
 
        layout_poze = QHBoxLayout()
        layout_poze.addWidget(self.poza_aleasa)
        layout_poze.addWidget(self.label_rezultat)

        layout_labelprimapoza = QHBoxLayout()
        layout_labelprimapoza.addWidget(labelPrimaPoza)
        layout_labelprimapoza.addWidget(labelAdouaPoza)

        layout_butoane_functii = QHBoxLayout()
        layout_butoane_functii.addWidget(self.efect_rotire)
        layout_butoane_functii.addWidget(self.efect_flip)
        layout_butoane_functii.addWidget(self.efect_filtrubilateral)
        layout_butoane_functii.addWidget(self.efect_dilatare)
        layout_butoane_functii.addWidget(self.efect_blurgaussian)
        layout_butoane_functii.addWidget(self.efect_medianblur)
        layout_butoane_functii.addWidget(self.efect_text)
        layout_butoane_functii.addWidget(self.canalcolor)
        layout_butoane_functii.addWidget(self.efect_resize)
        layout_butoane_functii.addWidget(self.efect_erodare)
        layout_butoane_functii.addWidget(self.translatare)
 
        layout_principal = QGridLayout()
        layout_principal.addLayout(layout_poze,4,0)
        layout_principal.addLayout(layout_labelprimapoza,3,0)
        layout_principal.addWidget(self.btn_poza,2,0)
        layout_principal.addLayout(layout_butoane_functii,1,0)
 
        widget = QWidget()
        widget.setLayout(layout_principal)
        self.setCentralWidget(widget)
        self.show()
 
    def getPoza(self):
        self.label_rezultat.clear()
       
        fname = QFileDialog.getOpenFileName(self, 'Open file',
         '/Users/daniel/Desktop/PROIECTE/FMI-A3/A3S1-ASC/M4/PozeM4',"Image files (*.jpg *.gif)")
        self.poza_aleasa.setPixmap(QPixmap(fname[0]))
        self.label_tine_minte_cale.setText(fname[0])
 
    def eroare_imagine_neselectata(self):
        mesaj_eroare = QMessageBox()
        mesaj_eroare.setIcon(QMessageBox.Information)
        mesaj_eroare.setText("Imaginea dorită nu este selectată!")
        mesaj_eroare.setWindowTitle("Eroare - Imagine neselectată")
        mesaj_eroare.setDetailedText("Pentru a se putea efectua această operație este nevoie să se apese pe butonul: Alegere imagine")
        mesaj_eroare.exec_()

    def flip_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        self.rez = cv2.flip(pozaTest,1)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
   
    def dilatare_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        kernel = np.ones((5, 5), np.uint8)
        self.rez = cv2.dilate(pozaTest, kernel, iterations=1)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
 
    def erodare_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        kernel = np.ones((5, 5), np.uint8)
        self.rez = cv2.erode(pozaTest, kernel, iterations=1)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
 
    def filtru_bilateral_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        self.rez = cv2.bilateralFilter(pozaTest,d=15,sigmaColor=75,sigmaSpace=75)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
   
    def blur_gaussian_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        borderSize = (5,5)
        self.rez = cv2.GaussianBlur(pozaTest,borderSize,cv2.BORDER_DEFAULT)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
 
    def afisare_text_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        org = (50,50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 0)
        fontScale = 1
        thickness = 2
        self.rez = cv2.putText(pozaTest, 'Bichon maltez', org, font,
                   fontScale, color, thickness, cv2.LINE_AA)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
   
    def median_blur_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        self.rez = cv2.medianBlur(pozaTest,5)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
   
    def redimensionare_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        self.rez = cv2.resize(pozaTest, (125, 225),
               interpolation = cv2.INTER_LINEAR)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
   
    def rotire_imgagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        self.rez = cv2.rotate(pozaTest,cv2.ROTATE_180)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
 
    def translateaza_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        inaltime,latime = pozaTest.shape[:2]
        dim_i,dim_l = inaltime / 4, latime / 4
        matrice_translatie = np.float32([[1,0,dim_i],[0,1,dim_l]])
        self.rez = cv2.warpAffine(pozaTest,matrice_translatie,(inaltime,latime))
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
 
    def canale_color_imagine(self):
        self.label_rezultat.clear()
        cale = self.label_tine_minte_cale.text()
       
        if(len(cale) == 0):
            self.eroare_imagine_neselectata()
            return
        pozaTest = cv2.imread(cale)
        self.rez = cv2.cvtColor(pozaTest,cv2.COLOR_BGR2RGB)
        self.convert = QImage(self.rez, self.rez.shape[1], self.rez.shape[0], self.rez.strides[0], QImage.Format.Format_BGR888)
        self.label_rezultat.setPixmap(QPixmap.fromImage(self.convert))
 
if __name__ == '__main__':
   
    app = QApplication(sys.argv)
 
    main = InterfataPrincipala()
   
    main.show()
   
    sys.exit(app.exec_())  