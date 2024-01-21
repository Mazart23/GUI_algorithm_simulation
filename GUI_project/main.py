'''
GUI Algorithm Simulation
MIT License
Copyright (c) 2024 Artur Mazurkiewicz
'''


import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
                              QAbstractItemView, QWidget, QStackedWidget, QPushButton, QLabel, QLineEdit, QSpacerItem, \
                              QSizePolicy, QGraphicsOpacityEffect, QCheckBox, QScrollArea
from sys import argv, exit
from os import path
from PySide6.QtGui import QFont, QImage, QPixmap, QColor, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import identyfikacja_ust as ust


basedir = path.dirname(__file__)

plt.style.use('seaborn-v0_8')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

style = """
#tabela{
border: 2px solid #191970;  /* Grubość linii */
}
QMainWindow {
    background-color: #F8F8FF;
}
QPushButton{
    min-height: 20px;
    max-height: 40px;
    min-width: 150px;
    max-width: 250px;
    padding: 10px 20px 10px 20px;
    border-style: solid;
    border-color: #a2a2a2;
    border-width: 2px;
    border-radius: 5px;
    color: #484848;
    background-color: white;
    font-weight: bold;
    font-size: 14px;
    font-family: Arial;
}
QLabel{
    padding: 5px 5px 5px 5px;
    color: #484848;
    font-weight: bold;
    border-style: solid;
    font-family: Arial;
}
QPushButton:hover{
    color: #292929;
    border-color: #191970;
}
QPushButton:checked{
    background-color: #191970;
    color: white;
}
QPushButton:disabled{
    color: #d0d0d0;
    border-color: #d0d0d0;
}
QCheckBox {
    color: #484848;
    font-weight: bold;
    border-style: solid;
    font-family: Arial;
    font-size: 14px;
    spacing: 10px;
}
QCheckBox::indicator {
    width: 10px; /* Szerokość pola zaznaczenia */
    height: 10px; /* Wysokość pola zaznaczenia */
    background-color: #ffffff; /* Kolor tła pola zaznaczenia */
    border: 2px solid #a2a2a2; /* Grubość i styl obramowania */
    border-radius: 5px; /* Zaokrąglenie rogów pola zaznaczenia */
}
QCheckBox::indicator:hover{
    border: 2px solid #191970;
}
QCheckBox::indicator:checked{
    background-color: #191970;
}
QLineEdit{
    padding: 5px 5px 5px 5px;
    min-height: 15px;
    max-height: 15px;
    min-width: 35px;
    max-width: 35px;
    border-style: solid;
    border-color: #a2a2a2;
    border-width: 2px;
    border-radius: 1px;
    color: #484848;
    font-weight: bold;
    font-size: 14px;
    font-family: Arial;
}
QLineEdit:hover{
    border-color: #777777;
}
QLineEdit:focus {
    border-color: #191970;
    outline: none; /* Usunięcie domyślnego konturu podczas focusowania */
}

#staly1, #liniowy2, #sinus4 {
    min-height: 20px;
    max-height: 40px;
    min-width: 50px;
    max-width: 50px;
}
#alfa{
    min-height: 15px;
    max-height: 15px;
    min-width: 100px;
    max-width: 100px;
}
#plusminus{
    padding: 1px 1px 1px 1px;
    min-height: 30px;
    max-height: 30px;
    min-width: 30px;
    max-width: 30px;
    font-weight: bold;
    font-size: 24px;
    font-family: Arial;
}
#pole_wynikowe{
    background-color: white;
}
#propoz{
    min-height: 20px;
    max-height: 40px;
    min-width: 250px;
    max-width: 500px;
}
#tabela_but{
    min-width: 800px;
    max-width: 800px;
}
#przycisk_start{
    min-height: 50px;
    max-height: 50px;
    min-width: 250px;
    max-width: 300px;
    font-size: 20px;
}
QScrollArea { 
    border: 2px solid;
    border-color: #191970; 
    background-color: white;
}
#wybor_widget{
    background-color: white;
}
#W0, #W1, #W2, #W3, #W4, #W5, #W6, #W7, #W8, #W9{
    min-width: 80px;
    max-width: 80px;
}
"""


class StartWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.font_l = QFont()
        self.font_l.setPointSize(16)
        self.font_l.setItalic(True)
        self.font_l.setBold(False)
        self.font_s = QFont()
        self.font_s.setPointSize(12)

        self.opis = QLabel('Aplikacja została zaimplementowana na potrzeby realizacji projektu dyplomowego.')
        self.opis.setFont(self.font_s)
        self.logo = QLabel(self)
        self.image = QImage(path.join(basedir, 'logo_agh.jpg'))
        self.image_scal = self.image.scaled(self.image.width() // 2, self.image.height() // 2,
                                            mode=Qt.SmoothTransformation)
        self.pixmap = QPixmap.fromImage(self.image_scal)
        self.logo.setPixmap(self.pixmap)
        self.logo.setScaledContents(False)

        self.tytul = QLabel('''Opracowanie oprogramowania do symulacji wybranych algorytmów 
                                  identyfikacji parametrycznej i nieparametrycznej''')
        self.tytul.setFont(self.font_l)
        self.label_tytul = QLabel('Tytuł:')
        self.label_tytul.setFont(self.font_l)
        self.autor = QLabel('Artur Mazurkiewicz')
        self.autor.setFont(self.font_l)
        self.label_autor = QLabel('Autor:')
        self.label_autor.setFont(self.font_l)
        self.promotor = QLabel('prof. dr hab. inż. Janusz Gajda')
        self.promotor.setFont(self.font_l)
        self.label_promotor = QLabel('Opiekun:')
        self.label_promotor.setFont(self.font_l)
        self.rok = QLabel('2024')
        self.rok.setFont(self.font_l)
        self.label_rok = QLabel('Rok:')
        self.label_rok.setFont(self.font_l)

        self.opis_dzialania = QLabel('''Aplikacja ma charakter edukacyjny i służy do przeprowadzenia symulacji identyfikacji 
na zadanym przez użytkownika obiekcie przy pomocy wybranych algorytmów.''')
        self.opis_dzialania.setFont(self.font_s)
        self.start = QPushButton('Rozpocznij')

        self.layout_tytul = QHBoxLayout()
        self.layout_tytul.addWidget(self.label_tytul)
        self.spacer_tytul = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout_tytul.addItem(self.spacer_tytul)
        self.layout_tytul.addWidget(self.tytul)
        self.layout_tytul.addSpacing(10)

        self.layout_autor = QHBoxLayout()
        self.layout_autor.addSpacing(200)
        self.layout_autor.addWidget(self.label_autor)
        self.spacer_autor = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_autor.addItem(self.spacer_autor)
        self.layout_autor.addWidget(self.autor)
        self.layout_autor.addSpacing(120)

        self.layout_promotor = QHBoxLayout()
        self.layout_promotor.addSpacing(200)
        self.layout_promotor.addWidget(self.label_promotor)
        self.spacer_promotor = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_promotor.addItem(self.spacer_promotor)
        self.layout_promotor.addWidget(self.promotor)
        self.layout_promotor.addSpacing(120)

        self.layout_rok = QHBoxLayout()
        self.layout_rok.addSpacing(200)
        self.layout_rok.addWidget(self.label_rok)
        self.spacer_rok = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_rok.addItem(self.spacer_rok)
        self.layout_rok.addWidget(self.rok)
        self.layout_rok.addSpacing(120)

        self.info_layout = QVBoxLayout()
        self.info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_layout.addLayout(self.layout_tytul)
        self.info_layout.addSpacing(30)
        self.info_layout.addLayout(self.layout_autor)
        self.info_layout.addSpacing(10)
        self.info_layout.addLayout(self.layout_promotor)
        self.info_layout.addSpacing(10)
        self.info_layout.addLayout(self.layout_rok)

        self.lay_praca_widget = QVBoxLayout()
        self.praca_widget = QWidget()
        self.praca_widget.setMinimumSize(1300, 400)
        self.praca_widget.setMaximumSize(1300, 400)
        self.praca_widget.setStyleSheet('background-color: white;')
        self.praca_layout = QHBoxLayout(self.praca_widget)
        self.praca_layout.addWidget(self.logo)
        self.praca_layout.addSpacing(50)
        self.praca_layout.addLayout(self.info_layout)
        self.lay_praca_widget.addWidget(self.praca_widget)

        self.lay_opis = QVBoxLayout()
        self.lay_opis.addWidget(self.opis)
        self.lay_opis_dzialania = QVBoxLayout()
        self.lay_opis_dzialania.addWidget(self.opis_dzialania)
        self.lay_start = QVBoxLayout()
        self.start.setObjectName('przycisk_start')
        self.start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lay_start.addWidget(self.start)

        self.lay_opis.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay_praca_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay_opis_dzialania.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay_start.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(30)
        self.layout.addLayout(self.lay_opis)
        self.layout.addSpacing(30)
        self.layout.addLayout(self.lay_praca_widget)
        self.layout.addSpacing(30)
        self.layout.addLayout(self.lay_opis_dzialania)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.lay_start)
        self.layout.addSpacing(30)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)


class MainMenuWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.font = QFont()
        self.font.setPointSize(20)
        self.font_s = QFont()
        self.font_s.setPointSize(12)

        self.title = QLabel("TYP OBIEKTU")
        self.title.setFont(self.font)

        self.label_param = QLabel('Identyfikacja parametryczna:')
        self.label_param.setFont(self.font_s)
        self.button_stacjo = QPushButton("Stacjonarny")
        self.button_niestacjo = QPushButton("Niestacjonarny")
        self.button_nielin = QPushButton("Nieliniowy")
        self.label_nparam = QLabel('Identyfikacja nieparametryczna:')
        self.label_nparam.setFont(self.font_s)
        self.button_dynamiczny = QPushButton("Dynamiczny")

        self.layout_title = QHBoxLayout()
        self.layout_label_param = QHBoxLayout()
        self.layout_button_stacjo = QHBoxLayout()
        self.layout_button_niestacjo = QHBoxLayout()
        self.layout_button_nielin = QHBoxLayout()
        self.layout_label_nparam = QHBoxLayout()
        self.layout_button_dynamiczny = QHBoxLayout()

        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_label_param.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_stacjo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_niestacjo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_nielin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_label_nparam.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_dynamiczny.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_title.addWidget(self.title)
        self.layout_label_param.addWidget(self.label_param)
        self.layout_button_stacjo.addWidget(self.button_stacjo)
        self.layout_button_niestacjo.addWidget(self.button_niestacjo)
        self.layout_button_nielin.addWidget(self.button_nielin)
        self.layout_label_nparam.addWidget(self.label_nparam)
        self.layout_button_dynamiczny.addWidget(self.button_dynamiczny)

        self.layout.addLayout(self.layout_title)
        self.layout.addSpacing(40)
        self.layout.addLayout(self.layout_label_param)
        self.layout.addSpacing(5)
        self.layout.addLayout(self.layout_button_stacjo)
        self.layout.addSpacing(5)
        self.layout.addLayout(self.layout_button_niestacjo)
        self.layout.addSpacing(5)
        self.layout.addLayout(self.layout_button_nielin)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.layout_label_nparam)
        self.layout.addSpacing(5)
        self.layout.addLayout(self.layout_button_dynamiczny)

        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class BladWidget(QWidget):

    def __init__(self, okno, e):
        super().__init__()

        self.okno = okno
        self.e = e

        self.setStyleSheet(style)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font = QFont()
        self.font.setPointSize(20)
        self.font_s = QFont()
        self.font_s.setPointSize(12)

        self.title = QLabel("BŁĄD")
        self.title.setStyleSheet("color: red;")
        self.title.setFont(self.font)

        self.blad = QLabel("Wystąpił następujący błąd:")
        self.blad.setStyleSheet("color: red;")
        self.blad.setFont(self.font_s)

        self.blad_opis = QLabel(f'{e}')
        self.blad_opis.setStyleSheet("color: red;")
        self.blad_opis.setFont(self.font_s)

        self.button_cofnij = QPushButton("Cofnij")
        self.button_cofnij.clicked.connect(self.open_okno)

        self.layout_title = QVBoxLayout()
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_blad = QVBoxLayout()
        self.layout_blad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_blad_opis = QVBoxLayout()
        self.layout_blad_opis.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button = QVBoxLayout()
        self.layout_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_title.addWidget(self.title)
        self.layout_blad.addWidget(self.blad)
        self.layout_blad_opis.addWidget(self.blad_opis)
        self.layout_button.addWidget(self.button_cofnij)

        self.layout.addLayout(self.layout_title)
        self.layout.addSpacing(40)
        self.layout.addLayout(self.layout_blad)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.layout_blad_opis)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.layout_button)

        self.setLayout(self.layout)


    def open_okno(self):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(1)
        self.okno.setGraphicsEffect(opacity_effect)
        self.parent().setCurrentWidget(self.okno)

class WidokStacjonarny(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY OBIEKTU STACJONARNEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_rzad = QHBoxLayout()
        self.layout_row_rzad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_rzad = QLabel("Stopień wielomianu obiektu:")
        self.napis_rzad.setFont(self.font_s)
        self.layout_row_rzad.addWidget(self.napis_rzad)
        self.pole_rzad = QLineEdit(self)
        self.pole_rzad.setText("1")
        self.pole_rzad.setObjectName("rzad")
        self.pole_rzad.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.pole_rzad.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout_row_rzad.addWidget(self.pole_rzad)

        self.layout_row_blad_rzad = QHBoxLayout()
        self.blad_rzad = QLabel("")
        self.blad_rzad.setStyleSheet("color: red;")
        self.blad_rzad.setFont(self.font_s)
        self.layout_row_blad_rzad.addWidget(self.blad_rzad)
        self.layout_row_blad_rzad.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_parametry = QHBoxLayout()
        self.layout_row_parametry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_parametry = QLabel("Parametry obiektu:")
        self.napis_parametry.setFont(self.font_s)
        self.layout_row_parametry.addWidget(self.napis_parametry)
        self.pola_parametry = []

        self.layout_row_blad_parametry = QHBoxLayout()
        self.blad_parametry = QLabel("")
        self.blad_parametry.setFont(self.font_s)
        self.blad_parametry.setStyleSheet("color: red;")
        self.layout_row_blad_parametry.addWidget(self.blad_parametry)
        self.layout_row_blad_parametry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dodaj_pola(2, True)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_param_sym = QPushButton("Parametry symulacji")
        self.layout_row_buttons.addWidget(self.button_param_sym)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_rzad)
        self.main_layout.addLayout(self.layout_row_blad_rzad)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_parametry)
        self.main_layout.addLayout(self.layout_row_blad_parametry)
        self.main_layout.addSpacing(100)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_rzad.textChanged.connect(self.sprawdz)

        self.pola_status = list(np.zeros((len(self.pola_parametry) // 2,)))
        for pole in self.pola_parametry:
            if pole.objectName().startswith("Pole"):
                pole.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == "rzad":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad.setText("Wpisz liczbę całkowitą w przedziale 1-4")
                self.dodaj_pola(0, False)
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad.setText("Zawiera litery")
                self.dodaj_pola(0, False)
                self.button_param_sym.setEnabled(False)

            elif not 0 < tekst < 5 or not tekst == int(tekst):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad.setText("Musi zawierać liczbę całkowitą w przedziale 1-4")
                self.dodaj_pola(0, False)
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_rzad.setText("")
                self.dodaj_pola(int(tekst) + 1, True)
                self.button_param_sym.setEnabled(True)

            for pole in self.pola_parametry:
                if pole.objectName().startswith("Pole"):
                    pole.textChanged.connect(self.sprawdz)

        if pole_text.objectName().startswith('Pole'):
            numer = int(pole_text.objectName()[-1])

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_parametry.setText("Musi zawierać liczby")
                self.pola_status[numer - 1] = 1
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status[numer - 1] = 0
                if self.pola_status == list(np.zeros((len(self.pola_parametry) // 2, 1))):
                    self.blad_parametry.setText("")
                    self.button_param_sym.setEnabled(True)

    def dodaj_pola(self, pola, status):
        while len(self.pola_parametry):
            wid = self.pola_parametry.pop(-1)
            self.layout_row_parametry.removeWidget(wid)
            wid.deleteLater()

        self.pola_parametry.clear()

        if status:
            for i in range(pola):
                napis = QLabel(f"x<sup>{pola-i-1}</sup>:")
                napis.setFont(self.font_s)
                self.layout_row_parametry.addWidget(napis)
                self.pola_parametry.append(napis)
                pole = QLineEdit(self)
                pole.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                pole.setAlignment(Qt.AlignmentFlag.AlignLeft)
                pole.setText("1")
                pole.setObjectName(f"Pole_param_{i + 1}")
                self.layout_row_parametry.addWidget(pole)
                self.pola_parametry.append(pole)

        self.pola_status = list(np.zeros((len(self.pola_parametry) // 2, 1)))
        self.blad_parametry.setText("")

    def result(self):
        typ = 'Stacjonarny'
        rzad = int(self.pole_rzad.text())
        parametry = []

        for pole in self.pola_parametry:
            if pole.objectName().startswith("Pole"):
                parametry.append(float(pole.text()))

        return typ, rzad, np.array(parametry)


class CustomWidget(QWidget):
    def __init__(self, rzad):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_row = QHBoxLayout()

        self.label_rzad = QLabel(f'x<sup>{rzad}</sup>')
        self.label_rzad.setFont(self.font_s)
        self.buttons = []
        self.button_staly = QPushButton("stały")
        self.button_staly.setObjectName('staly1')
        self.buttons.append(self.button_staly)
        self.button_liniowy = QPushButton("liniowy")
        self.button_liniowy.setObjectName('liniowy2')
        self.buttons.append(self.button_liniowy)
        self.button_sin = QPushButton("sinus")
        self.button_sin.setObjectName('sinus4')
        self.buttons.append(self.button_sin)

        self.button_staly.setCheckable(True)
        self.button_liniowy.setCheckable(True)
        self.button_sin.setCheckable(True)

        self.widgety = []
        self.pola = []

        self.status = 0

        self.button_staly.clicked.connect(self.change)
        self.button_liniowy.clicked.connect(self.change)
        self.button_sin.clicked.connect(self.change)

        self.layout_row.addSpacing(50)
        self.layout_row.addWidget(self.label_rzad)
        self.layout_row.addSpacing(50)
        self.layout_row.addWidget(self.button_staly)
        self.layout_row.addWidget(self.button_liniowy)
        self.layout_row.addWidget(self.button_sin)

        self.layout_blad = QHBoxLayout()
        self.blad_param = QLabel("")
        self.blad_param.setStyleSheet("color: red;")
        self.blad_param.setFont(self.font_s)
        self.layout_blad.addWidget(self.blad_param)
        self.layout_blad.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.layout_row)
        self.main_layout.addLayout(self.layout_blad)

        self.setLayout(self.main_layout)

        self.button_sin.click()
        self.button_liniowy.click()
        self.button_staly.click()


    def change(self):
        but = self.sender()
        self.setObjectName(but.objectName()[:-1])
        if not but.isChecked():
            but.setChecked(not but.isChecked())
        else:
            self.wyswietl(but.objectName()[-1])
            self.sprawdz()

        for i in self.buttons:
            if i != but:
                i.setChecked(False)

    def wyswietl(self, name):
        for field in self.widgety:
            if isinstance(field, QWidget):
                self.layout_row.removeWidget(field)
                field.deleteLater()
            if isinstance(field, QSpacerItem):
                self.layout_row.removeItem(field)

        self.widgety.clear()
        self.pola.clear()
        if hasattr(self.parent(), 'dodaj_layout'):
            self.button_staly.toggled.connect(self.parent().sprawdz)
            self.button_liniowy.toggled.connect(self.parent().sprawdz)
            self.button_sin.clicked.connect(self.parent().sprawdz)

        self.pola_status = list(np.zeros((int(name),)))

        labels = []

        match int(name):
            case 1:
                labels = ['Współczynnik:']
            case 2:
                labels = ['Współczynnik kierunkowy:', 'Wyraz wolny:']
            case 4:
                labels = ['Składowa stała:', 'Amplituda:', 'Okres:', 'Faza:']

        spacer = QSpacerItem(50, 10)
        spacer1 = QSpacerItem(30, 10)
        self.widgety.append(spacer)
        self.layout_row.addSpacerItem(spacer)

        for i in range(int(name)):
            label = QLabel(labels[i])
            label.setFont(self.font_s)
            self.widgety.append(label)
            self.layout_row.addWidget(label)

            field = QLineEdit(self)
            field.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            if int(name) == 4:
                if i == 1:
                    field.setText('1')
                elif i == 2:
                    field.setText('10')
                else:
                    field.setText('0')
            else:
                field.setText('1')

            field.setObjectName(f'{i+1}')
            field.textChanged.connect(self.sprawdz)
            if isinstance(self.parent(), WidokNiestacjonarny):
                field.textChanged.connect(self.parent().sprawdz)

            self.widgety.append(field)
            self.pola.append(field)
            self.layout_row.addWidget(field)
            if i == 2:
                pi = QLabel("∙π")
                pi.setFont(self.font_s)
                self.widgety.append(pi)
                self.layout_row.addWidget(pi)
            self.widgety.append(spacer1)
            self.layout_row.addSpacerItem(spacer1)

        match int(name):
            case 1:
                spacer_end = QSpacerItem(556, 20)
            case 2:
                spacer_end = QSpacerItem(251, 20)
            case 4:
                spacer_end = QSpacerItem(0, 20)

        self.widgety.append(spacer_end)
        self.layout_row.addSpacerItem(spacer_end)

    def sprawdz(self):
        pole_text = self.sender()
        numer = int(pole_text.objectName()[-1])

        if len(pole_text.objectName()) > 1:
            self.blad_param.setText("")
            self.pola_status = list(np.zeros((len(self.pola),)))
            self.status = 0
            if isinstance(self.parent(), WidokNiestacjonarny):
                self.parent().sprawdz()
            return None

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if numer == 3:
            if tekst is None or float(tekst) == 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_param.setText("Musi zawierać liczby (okres musi zawierać liczby niezerowe)")
                self.pola_status[numer - 1] = 1
                self.status = 1
            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status[numer - 1] = 0
                if self.pola_status == list(np.zeros((len(self.pola),))):
                    self.blad_param.setText("")
                    self.status = 0
        else:
            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_param.setText("Musi zawierać liczby")
                self.pola_status[numer - 1] = 1
                self.status = 1

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status[numer - 1] = 0
                if self.pola_status == list(np.zeros((len(self.pola), ))):
                    self.blad_param.setText("")
                    self.status = 0


class WidokNiestacjonarny(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_usun = True

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY OBIEKTU NIESTACJONARNEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_rzad = QHBoxLayout()
        self.layout_row_rzad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_rzad = QLabel("Stopień wielomianu obiektu:")
        self.napis_rzad.setFont(self.font_s)
        self.layout_row_rzad.addWidget(self.napis_rzad)
        self.pole_rzad = QLineEdit(self)
        self.pole_rzad.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_rzad.setText("1")
        self.pole_rzad.setObjectName("rzad")
        self.layout_row_rzad.addWidget(self.pole_rzad)

        self.layout_row_blad_rzad = QHBoxLayout()
        self.blad_rzad = QLabel("")
        self.blad_rzad.setVisible(False)
        self.blad_rzad.setStyleSheet("color: red;")
        self.blad_rzad.setFont(self.font_s)
        self.layout_row_blad_rzad.addWidget(self.blad_rzad)
        self.layout_row_blad_rzad.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_parametry = QVBoxLayout()

        self.widgety_parametry = []

        self.napis_parametry = QLabel("Parametry obiektu:")
        self.napis_parametry.setFont(self.font_s)
        self.layout_row_parametry.addWidget(self.napis_parametry)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_param_sym = QPushButton("Parametry symulacji")
        self.layout_row_buttons.addWidget(self.button_param_sym)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_row_rzad)
        self.main_layout.addLayout(self.layout_row_blad_rzad)
        self.main_layout.addLayout(self.layout_row_parametry)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_rzad.textChanged.connect(self.sprawdz)

        self.dodaj_layout(2, True)

        self.row_status = list(np.zeros((len(self.widgety_parametry),)))

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text is None:
            pass
        elif pole_text.objectName() == "rzad":

            if not len(pole_text.text()):
                self.blad_rzad.setVisible(True)
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad.setText("Wpisz liczbę całkowitą w przedziale 1-4")
                self.napis_parametry.setVisible(False)
                self.dodaj_layout(0, False)
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                self.blad_rzad.setVisible(True)
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad.setText("Zawiera litery")
                self.napis_parametry.setVisible(False)
                self.dodaj_layout(0, False)
                self.button_param_sym.setEnabled(False)

            elif not 0 < tekst < 5 or not tekst == int(tekst):
                self.blad_rzad.setVisible(True)
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad.setText("Musi zawierać liczbę całkowitą w przedziale 1-4")
                self.napis_parametry.setVisible(False)
                self.dodaj_layout(0, False)
                self.button_param_sym.setEnabled(False)

            else:
                self.blad_rzad.setVisible(False)
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_rzad.setText("")
                self.napis_parametry.setVisible(True)
                if self.status_usun:
                    self.status_usun = False
                    self.dodaj_layout(int(tekst) + 1, True)
                    self.status_usun = True
                self.button_param_sym.setEnabled(True)

        if [row.status for row in self.widgety_parametry] == list(np.zeros((len(self.widgety_parametry),))):
            self.button_param_sym.setEnabled(True)
        else:
            self.button_param_sym.setEnabled(False)

    def dodaj_layout(self, layout, status):
        for i in self.widgety_parametry:
            i.button_staly.click()
            self.layout_row_parametry.removeWidget(i)
            i.deleteLater()

        self.widgety_parametry.clear()

        if status:
            for i in range(layout):
                widget = CustomWidget(layout - i - 1)
                self.layout_row_parametry.addWidget(widget)
                self.widgety_parametry.append(widget)
        self.layout_row_parametry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pola_status = list(np.zeros((len(self.widgety_parametry), 1)))


    def result(self):
        typ = 'Niestacjonarny'
        rzad = int(self.pole_rzad.text())
        parametry = []

        for row in self.widgety_parametry:
            sublst = [row.objectName()]
            for field in row.pola:
                sublst.append(field.text() if field.text().isalpha() else float(field.text()))
            parametry.append(sublst)

        return typ, rzad, parametry


class WidokNieliniowy(QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY OBIEKTU NIELINIOWEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_choice_napis = QVBoxLayout()
        self.choice_napis = QLabel("Wybór funkcji:")
        self.choice_napis.setFont(self.font_s)
        self.layout_choice_napis.addWidget(self.choice_napis)
        self.layout_choice_napis.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_choice = QHBoxLayout()
        self.layout_row_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_sin = QPushButton("Funkcja sinusoidalna")
        self.button_sin.setObjectName('sin')
        self.button_sin_2 = QPushButton("Suma dwóch funkcji sinusoidalnych")
        self.button_sin_2.setObjectName('sin_2')
        self.button_exp = QPushButton("Funkcja eksponencjalna")
        self.button_exp.setObjectName('exp')
        self.button_sin.setCheckable(True)
        self.button_sin_2.setCheckable(True)
        self.button_exp.setCheckable(True)
        self.layout_row_choice.addWidget(self.button_sin)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_sin_2)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_exp)

        self.layout_row_skl = QHBoxLayout()
        self.layout_row_skl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_skl = QLabel("Składowa stała:")
        self.napis_skl.setFont(self.font_s)
        self.layout_row_skl.addWidget(self.napis_skl)
        self.pole_skl = QLineEdit(self)
        self.pole_skl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_skl.setText("0")
        self.pole_skl.setObjectName("skl")
        self.layout_row_skl.addWidget(self.pole_skl)

        self.layout_row_blad_skl = QHBoxLayout()
        self.blad_skl = QLabel("")
        self.blad_skl.setStyleSheet("color: red;")
        self.blad_skl.setFont(self.font_s)
        self.layout_row_blad_skl.addWidget(self.blad_skl)
        self.layout_row_blad_skl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_amp = QHBoxLayout()
        self.layout_row_amp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_amp = QLabel("Amplituda:")
        self.napis_amp.setFont(self.font_s)
        self.layout_row_amp.addWidget(self.napis_amp)
        self.pole_amp = QLineEdit(self)
        self.pole_amp.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_amp.setText("1")
        self.pole_amp.setObjectName("amp")
        self.layout_row_amp.addWidget(self.pole_amp)

        self.layout_row_blad_amp = QHBoxLayout()
        self.layout_row_blad_amp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blad_amp = QLabel("")
        self.blad_amp.setStyleSheet("color: red;")
        self.blad_amp.setFont(self.font_s)
        self.layout_row_blad_amp.addWidget(self.blad_amp)

        self.layout_row_amp_2 = QHBoxLayout()
        self.layout_row_amp_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_amp_2 = QLabel("Amplituda:")
        self.napis_amp_2.setFont(self.font_s)
        self.layout_row_amp_2.addWidget(self.napis_amp_2)
        self.pole_amp_2 = QLineEdit(self)
        self.pole_amp_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_amp_2.setText("0.5")
        self.pole_amp_2.setObjectName("amp_2")
        self.layout_row_amp_2.addWidget(self.pole_amp_2)

        self.layout_row_blad_amp_2 = QHBoxLayout()
        self.blad_amp_2 = QLabel("")
        self.blad_amp_2.setStyleSheet("color: red;")
        self.blad_amp_2.setFont(self.font_s)
        self.layout_row_blad_amp_2.addWidget(self.blad_amp_2)
        self.layout_row_blad_amp_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_T = QHBoxLayout()
        self.layout_row_T.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_T = QLabel("Okres:")
        self.napis_T.setFont(self.font_s)
        self.layout_row_T.addWidget(self.napis_T)
        self.pole_T = QLineEdit(self)
        self.pole_T.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_T.setText("5")
        self.pole_T.setObjectName("T")
        self.layout_row_T.addWidget(self.pole_T)

        self.layout_row_blad_T = QHBoxLayout()
        self.blad_T = QLabel("")
        self.blad_T.setStyleSheet("color: red;")
        self.blad_T.setFont(self.font_s)
        self.layout_row_blad_T.addWidget(self.blad_T)
        self.layout_row_blad_T.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_T_2 = QHBoxLayout()
        self.layout_row_T_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_T_2 = QLabel("Okres:")
        self.napis_T_2.setFont(self.font_s)
        self.layout_row_T_2.addWidget(self.napis_T_2)
        self.pole_T_2 = QLineEdit(self)
        self.pole_T_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_T_2.setText("10")
        self.pole_T_2.setObjectName("T_2")
        self.layout_row_T_2.addWidget(self.pole_T_2)

        self.layout_row_blad_T_2 = QHBoxLayout()
        self.blad_T_2 = QLabel("")
        self.blad_T_2.setStyleSheet("color: red;")
        self.blad_T_2.setFont(self.font_s)
        self.layout_row_blad_T_2.addWidget(self.blad_T_2)
        self.layout_row_blad_T_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pi = QLabel("∙π")
        self.pi.setFont(self.font_s)
        self.layout_row_przes = QHBoxLayout()
        self.layout_row_przes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_przes = QLabel("Faza:")
        self.napis_przes.setFont(self.font_s)
        self.layout_row_przes.addWidget(self.napis_przes)
        self.pole_przes = QLineEdit(self)
        self.pole_przes.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_przes.setText("0")
        self.pole_przes.setObjectName("przes")
        self.layout_row_przes.addWidget(self.pole_przes)
        self.layout_row_przes.addWidget(self.pi)

        self.layout_row_blad_przes = QHBoxLayout()
        self.blad_przes = QLabel("")
        self.blad_przes.setStyleSheet("color: red;")
        self.blad_przes.setFont(self.font_s)
        self.layout_row_blad_przes.addWidget(self.blad_przes)
        self.layout_row_blad_przes.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pi_2 = QLabel("∙π")
        self.pi_2.setFont(self.font_s)
        self.pi_2.setVisible(False)
        self.layout_row_przes_2 = QHBoxLayout()
        self.layout_row_przes_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_przes_2 = QLabel("Faza:")
        self.napis_przes_2.setFont(self.font_s)
        self.layout_row_przes_2.addWidget(self.napis_przes_2)
        self.pole_przes_2 = QLineEdit(self)
        self.pole_przes_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_przes_2.setText("0")
        self.pole_przes_2.setObjectName("przes_2")
        self.layout_row_przes_2.addWidget(self.pole_przes_2)
        self.layout_row_przes_2.addWidget(self.pi_2)

        self.layout_row_blad_przes_2 = QHBoxLayout()
        self.blad_przes_2 = QLabel("")
        self.blad_przes_2.setStyleSheet("color: red;")
        self.blad_przes_2.setFont(self.font_s)
        self.layout_row_blad_przes_2.addWidget(self.blad_przes_2)
        self.layout_row_blad_przes_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_param_sym = QPushButton("Parametry symulacji")
        self.layout_row_buttons.addWidget(self.button_param_sym)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_choice_napis)
        self.main_layout.addLayout(self.layout_row_choice)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_row_skl)
        self.main_layout.addLayout(self.layout_row_blad_skl)
        self.main_layout.addLayout(self.layout_row_amp)
        self.main_layout.addLayout(self.layout_row_blad_amp)
        self.main_layout.addLayout(self.layout_row_T)
        self.main_layout.addLayout(self.layout_row_blad_T)
        self.main_layout.addLayout(self.layout_row_przes)
        self.main_layout.addLayout(self.layout_row_blad_przes)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_row_amp_2)
        self.main_layout.addLayout(self.layout_row_blad_amp_2)
        self.main_layout.addLayout(self.layout_row_T_2)
        self.main_layout.addLayout(self.layout_row_blad_T_2)
        self.main_layout.addLayout(self.layout_row_przes_2)
        self.main_layout.addLayout(self.layout_row_blad_przes_2)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.button_sin.clicked.connect(self.change)
        self.button_sin_2.clicked.connect(self.change)
        self.button_exp.clicked.connect(self.change)
        self.button_sin.toggled.connect(self.sprawdz)
        self.button_sin_2.toggled.connect(self.sprawdz)
        self.button_exp.toggled.connect(self.sprawdz)
        self.button_sin.click()

        self.pole_amp.textChanged.connect(self.sprawdz)
        self.pole_T.textChanged.connect(self.sprawdz)
        self.pole_przes.textChanged.connect(self.sprawdz)
        self.pole_amp_2.textChanged.connect(self.sprawdz)
        self.pole_T_2.textChanged.connect(self.sprawdz)
        self.pole_przes_2.textChanged.connect(self.sprawdz)
        self.pole_skl.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None


        if pole_text.objectName() == "amp":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Wpisz liczbę")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_amp.setText("")

        elif pole_text.objectName() == "amp_2":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp_2.setText("Wpisz liczbę")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp_2.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_amp_2.setText("")

        elif pole_text.objectName() == "T":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Wpisz liczbę dodatnią")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Musi zawierać liczbę dodatnią")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_T.setText("")

        elif pole_text.objectName() == "T_2":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T_2.setText("Wpisz liczbę dodatnią")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T_2.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T_2.setText("Musi zawierać liczbę dodatnią")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_T_2.setText("")

        elif pole_text.objectName() == "przes":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes.setText("Wpisz liczbę")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_przes.setText("")

        elif pole_text.objectName() == "przes_2":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes_2.setText("Wpisz liczbę")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes_2.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_przes_2.setText("")

        elif pole_text.objectName() == "skl":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_skl.setText("Wpisz liczbę")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_skl.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_skl.setText("")

        elif pole_text.objectName() == "st_czas":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Wpisz liczbę dodatnią")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Musi zawierać liczbę dodatnią")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_T.setText("")

        if self.button_sin.isChecked():
            if not (self.blad_amp.text() or self.blad_T.text() or self.blad_przes.text() or self.blad_skl.text()):
                self.button_param_sym.setEnabled(True)
            else:
                self.button_param_sym.setEnabled(False)

        elif self.button_sin_2.isChecked():

            if not (self.blad_amp.text() or self.blad_T.text() or self.blad_przes.text() or self.blad_amp_2.text() or
                    self.blad_T_2.text() or self.blad_przes_2.text() or self.blad_skl.text()) and \
                    self.pole_T.text() != self.pole_T_2.text():
                self.button_param_sym.setEnabled(True)

            else:
                self.button_param_sym.setEnabled(False)

        elif self.button_exp.isChecked():
            if not (self.blad_amp.text() or self.blad_T.text() or self.blad_skl.text()):
                self.button_param_sym.setEnabled(True)
            else:
                self.button_param_sym.setEnabled(False)

    def change(self):
        but = self.sender()
        if not but.isChecked():
            but.setChecked(not but.isChecked())
        else:
            if but.objectName() == 'sin':
                self.pole_T.setObjectName('T')
                self.napis_T.setText('Okres:')
                self.pi.setVisible(True)
                self.pi_2.setVisible(False)

                self.button_sin.setChecked(True)
                self.button_sin_2.setChecked(False)
                self.button_exp.setChecked(False)

                self.napis_skl.setVisible(True)
                self.pole_skl.setVisible(True)
                self.blad_skl.setVisible(True)
                self.napis_amp.setVisible(True)
                self.napis_amp.setText("Amplituda:")
                self.pole_amp.setVisible(True)
                self.blad_amp.setVisible(True)
                self.napis_T.setVisible(True)
                self.napis_T.setText("Okres:")
                self.pole_T.setVisible(True)
                self.blad_T.setVisible(True)
                self.napis_przes.setVisible(True)
                self.napis_przes.setText("Faza:")
                self.pole_przes.setVisible(True)
                self.blad_przes.setVisible(True)

                self.napis_amp_2.setVisible(False)
                self.pole_amp_2.setVisible(False)
                self.blad_amp_2.setVisible(False)
                self.napis_T_2.setVisible(False)
                self.pole_T_2.setVisible(False)
                self.blad_T_2.setVisible(False)
                self.napis_przes_2.setVisible(False)
                self.pole_przes_2.setVisible(False)
                self.blad_przes_2.setVisible(False)

            elif but.objectName() == 'sin_2':
                self.pole_T.setObjectName('T')
                self.napis_T.setText('Okres 1:')
                self.napis_amp.setText("Amplituda 1:")
                self.pi.setVisible(True)
                self.pi_2.setVisible(True)

                self.button_sin.setChecked(False)
                self.button_sin_2.setChecked(True)
                self.button_exp.setChecked(False)

                self.napis_przes.setVisible(True)
                self.napis_przes.setText("Faza 1:")
                self.pole_przes.setVisible(True)
                self.blad_przes.setVisible(True)

                self.napis_amp_2.setVisible(True)
                self.napis_amp_2.setText("Amplituda 2:")
                self.pole_amp_2.setVisible(True)
                self.blad_amp_2.setVisible(True)
                self.napis_T_2.setVisible(True)
                self.napis_T_2.setText("Okres 2:")
                self.pole_T_2.setVisible(True)
                self.blad_T_2.setVisible(True)
                self.napis_przes_2.setVisible(True)
                self.napis_przes_2.setText("Faza 2:")
                self.pole_przes_2.setVisible(True)
                self.blad_przes_2.setVisible(True)

            elif but.objectName() == 'exp':
                self.napis_T.setText('Stała czasowa:')
                self.pole_T.setObjectName('st_czas')
                self.napis_amp.setText("Wzmocnienie:")
                self.pi.setVisible(False)
                self.pi_2.setVisible(False)

                self.button_sin.setChecked(False)
                self.button_sin_2.setChecked(False)
                self.button_exp.setChecked(True)

                self.napis_przes.setVisible(False)
                self.pole_przes.setVisible(False)
                self.blad_przes.setVisible(False)
                self.napis_amp_2.setVisible(False)
                self.pole_amp_2.setVisible(False)
                self.blad_amp_2.setVisible(False)
                self.napis_T_2.setVisible(False)
                self.pole_T_2.setVisible(False)
                self.blad_T_2.setVisible(False)
                self.napis_przes_2.setVisible(False)
                self.pole_przes_2.setVisible(False)
                self.blad_przes_2.setVisible(False)

    def result(self):
        if self.button_sin.isChecked():
            typ = 'sinus'
            amp = float(self.pole_amp.text())
            T = float(self.pole_T.text())
            przes = float(self.pole_przes.text())
            skl = float(self.pole_skl.text())
            return typ, amp, T, przes, skl

        elif self.button_sin_2.isChecked():
            typ = 'sinus_2'
            amp = float(self.pole_amp.text())
            T = float(self.pole_T.text())
            przes = float(self.pole_przes.text())
            amp_2 = float(self.pole_amp_2.text())
            T_2 = float(self.pole_T_2.text())
            przes_2 = float(self.pole_przes_2.text())
            skl = float(self.pole_skl.text())
            return typ, amp, T, przes, amp_2, T_2, przes_2, skl

        elif self.button_exp.isChecked():
            typ = 'exp'
            amp = float(self.pole_amp.text())
            T = float(self.pole_T.text())
            skl = float(self.pole_skl.text())
            return typ, amp, T, skl


class WidokDynamiczny(QWidget):

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY OBIEKTU DYNAMICZNEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_choice_napis = QVBoxLayout()
        self.choice_napis = QLabel("Wybór obiektu:")
        self.choice_napis.setFont(self.font_s)
        self.layout_choice_napis.addWidget(self.choice_napis)
        self.layout_choice_napis.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_choice = QHBoxLayout()
        self.layout_row_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_sin = QPushButton("Inercyjny I rzędu")
        self.button_sin.setObjectName('sin')
        self.button_sin_2 = QPushButton("Inercyjny II rzędu")
        self.button_sin_2.setObjectName('sin_2')
        self.button_exp = QPushButton("Oscylacyjny")
        self.button_exp.setObjectName('exp')
        self.button_sin.setCheckable(True)
        self.button_sin_2.setCheckable(True)
        self.button_exp.setCheckable(True)
        self.layout_row_choice.addWidget(self.button_sin)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_sin_2)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_exp)

        self.layout_row_skl = QHBoxLayout()
        self.layout_row_skl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_skl = QLabel("Wzmocnienie:")
        self.napis_skl.setFont(self.font_s)
        self.layout_row_skl.addWidget(self.napis_skl)
        self.pole_skl = QLineEdit(self)
        self.pole_skl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_skl.setText("1")
        self.pole_skl.setObjectName("skl")
        self.layout_row_skl.addWidget(self.pole_skl)

        self.layout_row_blad_skl = QHBoxLayout()
        self.blad_skl = QLabel("")
        self.blad_skl.setStyleSheet("color: red;")
        self.blad_skl.setFont(self.font_s)
        self.layout_row_blad_skl.addWidget(self.blad_skl)
        self.layout_row_blad_skl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_amp = QHBoxLayout()
        self.layout_row_amp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_amp = QLabel("Stała czasowa:")
        self.napis_amp.setFont(self.font_s)
        self.layout_row_amp.addWidget(self.napis_amp)
        self.pole_amp = QLineEdit(self)
        self.pole_amp.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_amp.setText("0.2")
        self.pole_amp.setObjectName("amp")
        self.layout_row_amp.addWidget(self.pole_amp)

        self.layout_row_blad_amp = QHBoxLayout()
        self.layout_row_blad_amp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blad_amp = QLabel("")
        self.blad_amp.setStyleSheet("color: red;")
        self.blad_amp.setFont(self.font_s)
        self.layout_row_blad_amp.addWidget(self.blad_amp)

        self.layout_row_T = QHBoxLayout()
        self.layout_row_T.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_T = QLabel("Stała czasowa 2:")
        self.napis_T.setFont(self.font_s)
        self.layout_row_T.addWidget(self.napis_T)
        self.pole_T = QLineEdit(self)
        self.pole_T.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_T.setText("0.1")
        self.pole_T.setObjectName("T")
        self.layout_row_T.addWidget(self.pole_T)

        self.layout_row_blad_T = QHBoxLayout()
        self.blad_T = QLabel("")
        self.blad_T.setStyleSheet("color: red;")
        self.blad_T.setFont(self.font_s)
        self.layout_row_blad_T.addWidget(self.blad_T)
        self.layout_row_blad_T.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_param_sym = QPushButton("Parametry symulacji")
        self.layout_row_buttons.addWidget(self.button_param_sym)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_choice_napis)
        self.main_layout.addLayout(self.layout_row_choice)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_row_skl)
        self.main_layout.addLayout(self.layout_row_blad_skl)
        self.main_layout.addLayout(self.layout_row_amp)
        self.main_layout.addLayout(self.layout_row_blad_amp)
        self.main_layout.addLayout(self.layout_row_T)
        self.main_layout.addLayout(self.layout_row_blad_T)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.button_sin.clicked.connect(self.change)
        self.button_sin_2.clicked.connect(self.change)
        self.button_exp.clicked.connect(self.change)
        self.button_sin.toggled.connect(self.sprawdz)
        self.button_sin_2.toggled.connect(self.sprawdz)
        self.button_exp.toggled.connect(self.sprawdz)
        self.button_sin.click()

        self.pole_amp.textChanged.connect(self.sprawdz)
        self.pole_T.textChanged.connect(self.sprawdz)
        self.pole_skl.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == "amp":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Wpisz liczbę nieujemną")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            elif tekst < 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Musi zawierać liczbę nieujemną")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_amp.setText("")

        elif pole_text.objectName() == "T":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Wpisz liczbę nieujemną")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            elif tekst < 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Musi zawierać liczbę nieujemną")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_T.setText("")

        elif pole_text.objectName() == "skl":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_skl.setText("Wpisz liczbę")
                self.button_param_sym.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_skl.setText("Zawiera litery")
                self.button_param_sym.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_skl.setText("")

        if self.button_sin.isChecked():
            if not (self.blad_amp.text() or self.blad_skl.text()):
                self.button_param_sym.setEnabled(True)
            else:
                self.button_param_sym.setEnabled(False)

        elif self.button_sin_2.isChecked() or self.button_exp.isChecked():
            if not (self.blad_amp.text() or self.blad_T.text() or self.blad_skl.text()):
                self.button_param_sym.setEnabled(True)
            else:
                self.button_param_sym.setEnabled(False)

    def change(self):
        but = self.sender()
        if not but.isChecked():
            but.setChecked(not but.isChecked())
        else:
            if but.objectName() == 'sin':
                self.button_sin.setChecked(True)
                self.button_sin_2.setChecked(False)
                self.button_exp.setChecked(False)

                self.napis_amp.setText("Stała czasowa:")
                self.napis_T.setVisible(False)
                self.pole_T.setVisible(False)
                self.blad_T.setVisible(False)

            elif but.objectName() == 'sin_2':
                self.button_sin.setChecked(False)
                self.button_sin_2.setChecked(True)
                self.button_exp.setChecked(False)

                self.napis_amp.setText("Stała czasowa 1:")
                self.napis_T.setText("Stała czasowa 2:")
                self.napis_T.setVisible(True)
                self.pole_T.setVisible(True)
                self.blad_T.setVisible(True)

            elif but.objectName() == 'exp':
                self.napis_T.setText('Stała czasowa:')
                self.pole_T.setObjectName('st_czas')
                self.napis_amp.setText("Wzmocnienie:")
                self.button_sin.setChecked(False)
                self.button_sin_2.setChecked(False)
                self.button_exp.setChecked(True)

                self.napis_amp.setText("Współczynnik tłumienia:")
                self.napis_T.setText("Okres drgań nietłumionych:")
                self.napis_T.setVisible(True)
                self.pole_T.setVisible(True)
                self.blad_T.setVisible(True)

    def result(self):
        if self.button_sin.isChecked():
            typ = 'iner1'
            st_czas = float(self.pole_amp.text())
            wzm = float(self.pole_skl.text())
            return typ, wzm, st_czas

        elif self.button_sin_2.isChecked():
            typ = 'iner2'
            st_czas = float(self.pole_amp.text())
            st_czas_2 = float(self.pole_T.text())
            wzm = float(self.pole_skl.text())
            return typ, wzm, st_czas, st_czas_2

        elif self.button_exp.isChecked():
            typ = 'osc'
            tlum = float(self.pole_amp.text())
            okr_dr = float(self.pole_T.text())
            wzm = float(self.pole_skl.text())
            return typ, wzm, tlum, okr_dr


class WidokParametrySymulacji(QWidget):
    def __init__(self):
        super().__init__()

        self.rzad = 1
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY SYMULACJI OBIEKTU STACJONARNEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_rzad_m = QHBoxLayout()
        self.layout_row_rzad_m.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_rzad_m = QLabel("Stopień wielomianu modelu:")
        self.napis_rzad_m.setFont(self.font_s)
        self.layout_row_rzad_m.addWidget(self.napis_rzad_m)
        self.pole_rzad_m = QLineEdit(self)
        self.pole_rzad_m.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_rzad_m.setText(f'{self.rzad}')
        self.pole_rzad_m.setObjectName("rzad_m")
        self.layout_row_rzad_m.addWidget(self.pole_rzad_m)

        self.layout_row_blad_rzad_m = QHBoxLayout()
        self.blad_rzad_m = QLabel("")
        self.blad_rzad_m.setStyleSheet("color: red;")
        self.blad_rzad_m.setFont(self.font_s)
        self.layout_row_blad_rzad_m.addWidget(self.blad_rzad_m)
        self.layout_row_blad_rzad_m.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_N = QHBoxLayout()
        self.layout_row_N.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_N = QLabel("Liczba próbek:")
        self.napis_N.setFont(self.font_s)
        self.layout_row_N.addWidget(self.napis_N)
        self.pole_N = QLineEdit(self)
        self.pole_N.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_N.setText("100")
        self.pole_N.setObjectName("Liczba próbek")
        self.layout_row_N.addWidget(self.pole_N)

        self.layout_row_blad_N = QHBoxLayout()
        self.blad_N = QLabel("")
        self.blad_N.setStyleSheet("color: red;")
        self.blad_N.setFont(self.font_s)
        self.layout_row_blad_N.addWidget(self.blad_N)
        self.layout_row_blad_N.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakres = QHBoxLayout()
        self.layout_row_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakr_min = QLabel("Minimum:")
        self.napis_zakr_min.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_min)
        self.pole_zakr_min = QLineEdit(self)
        self.pole_zakr_min.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_min.setText("0")
        self.pole_zakr_min.setObjectName("Zakres 1")
        self.layout_row_zakres.addWidget(self.pole_zakr_min)

        self.layout_row_zakres.addSpacing(30)

        self.napis_zakr_max = QLabel("Maximum:")
        self.napis_zakr_max.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_max)
        self.pole_zakr_max = QLineEdit(self)
        self.pole_zakr_max.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_max.setText("10")
        self.pole_zakr_max.setObjectName("Zakres 2")
        self.layout_row_zakres.addWidget(self.pole_zakr_max)

        self.layout_row_blad_zakres = QHBoxLayout()
        self.blad_zakres = QLabel("")
        self.blad_zakres.setStyleSheet("color: red;")
        self.blad_zakres.setFont(self.font_s)
        self.layout_row_blad_zakres.addWidget(self.blad_zakres)
        self.layout_row_blad_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakl = QHBoxLayout()
        self.layout_row_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakl = QLabel("Odchylenie standardowe zakłóceń:")
        self.napis_zakl.setFont(self.font_s)
        self.layout_row_zakl.addWidget(self.napis_zakl)
        self.pole_zakl = QLineEdit(self)
        self.pole_zakl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakl.setText("1")
        self.pole_zakl.setObjectName("Zakłócenia")
        self.layout_row_zakl.addWidget(self.pole_zakl)

        self.layout_row_blad_zakl = QHBoxLayout()
        self.blad_zakl = QLabel("")
        self.blad_zakl.setStyleSheet("color: red;")
        self.blad_zakl.setFont(self.font_s)
        self.layout_row_blad_zakl.addWidget(self.blad_zakl)
        self.layout_row_blad_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_metoda = QPushButton("Wybór algorytmu")
        self.layout_row_buttons.addWidget(self.button_metoda)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_rzad_m)
        self.main_layout.addLayout(self.layout_row_blad_rzad_m)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_N)
        self.main_layout.addLayout(self.layout_row_blad_N)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_zakres)
        self.main_layout.addLayout(self.layout_row_blad_zakres)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_zakl)
        self.main_layout.addLayout(self.layout_row_blad_zakl)
        self.main_layout.addSpacing(100)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_rzad_m.textChanged.connect(self.sprawdz)
        self.pole_N.textChanged.connect(self.sprawdz)
        self.pole_zakr_min.textChanged.connect(self.sprawdz)
        self.pole_zakr_max.textChanged.connect(self.sprawdz)
        self.pole_zakl.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == "rzad_m":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad_m.setText(f"Wpisz liczbę całkowitą (sugerowana liczba równa stopniowi wielomianu obiektu: {self.rzad})")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad_m.setText("Zawiera litery")
                self.button_metoda.setEnabled(False)

            elif not 0 < tekst < 5 or not tekst == int(tekst):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_rzad_m.setText("Musi zawierać liczbę całkowitą w przedziale 1-4")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_rzad_m.setText("")
                if int(tekst) < int(self.pole_N.text()):
                    self.blad_N.setText("")
                    self.pole_N.setStyleSheet("color: #484848; background-color: white")
                else:
                    self.blad_N.setText("Musi zawierać liczbę całkowitą większą niż stopień wielomianu modelu")
                    self.pole_N.setStyleSheet("color: red; background-color: white")
                    self.button_metoda.setEnabled(False)

        if pole_text.objectName() == "Liczba próbek":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Wpisz liczbę całkowitą większą niż stopień wielomianu modelu")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 < tekst or not tekst == int(tekst):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Musi zawierać liczbę całkowitą większą niż stopień wielomianu modelu")
                self.button_metoda.setEnabled(False)

            else:
                try:
                    if not int(self.pole_rzad_m.text()) < int(tekst):
                        raise
                    pole_text.setStyleSheet("color: #484848; background-color: white")
                    self.blad_N.setText("")
                except:
                    pole_text.setStyleSheet("color: red; background-color: white")
                    self.blad_N.setText("Musi zawierać liczbę całkowitą większą niż stopień wielomianu modelu")
                    self.button_metoda.setEnabled(False)

        if pole_text.objectName().startswith('Zakres'):
            try:
                zakr_min = float(self.pole_zakr_min.text())
            except:
                zakr_min = None

            try:
                zakr_max = float(self.pole_zakr_max.text())
            except:
                zakr_max = None

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakres.setText("Musi zawierać liczby")
                self.button_metoda.setEnabled(False)

                if zakr_min is not None:
                    self.pole_zakr_min.setStyleSheet("color: #484848; background-color: white;")

                if zakr_max is not None:
                    self.pole_zakr_max.setStyleSheet("color: #484848; background-color: white;")

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakres.setText("")

                if zakr_min is None or zakr_max is None:
                    self.blad_zakres.setText("Musi zawierać liczby")
                    self.button_metoda.setEnabled(False)

            if zakr_max is not None and zakr_min is not None:

                if zakr_min >= zakr_max:
                    self.pole_zakr_min.setStyleSheet("color: red; background-color: white;")
                    self.pole_zakr_max.setStyleSheet("color: red; background-color: white;")
                    self.blad_zakres.setText("Maximum musi być większe od minimum")
                    self.button_metoda.setEnabled(False)

                else:
                    self.pole_zakr_min.setStyleSheet("color: #484848; background-color: white;")
                    self.pole_zakr_max.setStyleSheet("color: #484848; background-color: white;")
                    self.blad_zakres.setText("")

        if pole_text.objectName() == "Zakłócenia":
            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Wpisz liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 <= tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Musi zawierać liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakl.setText("")

        if not (self.blad_rzad_m.text() or self.blad_N.text() or self.blad_zakres.text() or self.blad_zakl.text()):
            self.button_metoda.setEnabled(True)

    def edit(self, rzad):
        self.rzad = rzad
        self.pole_rzad_m.setText(f'{rzad}')


    def result(self):
        rzad_m = int(self.pole_rzad_m.text())
        N = int(self.pole_N.text())
        zakr_min = float(self.pole_zakr_min.text())
        zakr_max = float(self.pole_zakr_max.text())
        zakl = float(self.pole_zakl.text())
        return rzad_m, N, zakr_min, zakr_max, zakl


class WidokParametrySymulacjiNiestacjo(QWidget):
    def __init__(self):
        super().__init__()

        self.rzad = 1
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY SYMULACJI OBIEKTU NIESTACJONARNEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_N = QHBoxLayout()
        self.layout_row_N.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_N = QLabel("Liczba próbek:")
        self.napis_N.setFont(self.font_s)
        self.layout_row_N.addWidget(self.napis_N)
        self.pole_N = QLineEdit(self)
        self.pole_N.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_N.setText("1000")
        self.pole_N.setObjectName("Liczba próbek")
        self.layout_row_N.addWidget(self.pole_N)

        self.layout_row_blad_N = QHBoxLayout()
        self.blad_N = QLabel("")
        self.blad_N.setStyleSheet("color: red;")
        self.blad_N.setFont(self.font_s)
        self.layout_row_blad_N.addWidget(self.blad_N)
        self.layout_row_blad_N.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakres = QHBoxLayout()
        self.layout_row_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakr_min = QLabel("Minimum:")
        self.napis_zakr_min.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_min)
        self.pole_zakr_min = QLineEdit(self)
        self.pole_zakr_min.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_min.setText("0")
        self.pole_zakr_min.setObjectName("Zakres 1")
        self.layout_row_zakres.addWidget(self.pole_zakr_min)

        self.layout_row_zakres.addSpacing(30)

        self.napis_zakr_max = QLabel("Maximum:")
        self.napis_zakr_max.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_max)
        self.pole_zakr_max = QLineEdit(self)
        self.pole_zakr_max.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_max.setText("10")
        self.pole_zakr_max.setObjectName("Zakres 2")
        self.layout_row_zakres.addWidget(self.pole_zakr_max)

        self.layout_row_blad_zakres = QHBoxLayout()
        self.blad_zakres = QLabel("")
        self.blad_zakres.setStyleSheet("color: red;")
        self.blad_zakres.setFont(self.font_s)
        self.layout_row_blad_zakres.addWidget(self.blad_zakres)
        self.layout_row_blad_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_wybieranie = QHBoxLayout()
        self.layout_wybieranie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_wybieranie = QLabel("Wymuszenie wybierane:")
        self.napis_wybieranie.setFont(self.font_s)
        self.layout_wybieranie.addWidget(self.napis_wybieranie)

        self.layout_row_choice = QHBoxLayout()
        self.layout_row_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_sekw = QPushButton("sekwencyjnie")
        self.button_sekw.setObjectName('sekwencyjne')
        self.button_los_sekw = QPushButton("losowo ze stałym krokiem")
        self.button_los_sekw.setObjectName('losowo-sekwencyjne')
        self.button_los = QPushButton("losowo ze zmiennym krokiem")
        self.button_los.setObjectName('losowe')
        self.button_sekw.setCheckable(True)
        self.button_los_sekw.setCheckable(True)
        self.button_los.setCheckable(True)
        self.layout_row_choice.addWidget(self.button_sekw)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_los_sekw)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_los)
        self.button_sekw.clicked.connect(self.change)
        self.button_los_sekw.clicked.connect(self.change)
        self.button_los.clicked.connect(self.change)

        self.layout_row_zakl = QHBoxLayout()
        self.layout_row_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakl = QLabel("Odchylenie standardowe zakłóceń:")
        self.napis_zakl.setFont(self.font_s)
        self.layout_row_zakl.addWidget(self.napis_zakl)
        self.pole_zakl = QLineEdit(self)
        self.pole_zakl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakl.setText("0.1")
        self.pole_zakl.setObjectName("Zakłócenia")
        self.layout_row_zakl.addWidget(self.pole_zakl)

        self.layout_row_blad_zakl = QHBoxLayout()
        self.blad_zakl = QLabel("")
        self.blad_zakl.setStyleSheet("color: red;")
        self.blad_zakl.setFont(self.font_s)
        self.layout_row_blad_zakl.addWidget(self.blad_zakl)
        self.layout_row_blad_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_metoda = QPushButton("Wybór algorytmu")
        self.layout_row_buttons.addWidget(self.button_metoda)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(50)
        self.main_layout.addLayout(self.layout_row_N)
        self.main_layout.addLayout(self.layout_row_blad_N)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakres)
        self.main_layout.addLayout(self.layout_row_blad_zakres)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_wybieranie)
        self.main_layout.addLayout(self.layout_row_choice)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakl)
        self.main_layout.addLayout(self.layout_row_blad_zakl)
        self.main_layout.addSpacing(50)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.button_los.click()
        self.pole_N.textChanged.connect(self.sprawdz)
        self.pole_zakr_min.textChanged.connect(self.sprawdz)
        self.pole_zakr_max.textChanged.connect(self.sprawdz)
        self.pole_zakl.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text is None:
            if not self.rzad < int(self.pole_N.text()):
                self.pole_N.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Musi zawierać liczbę całkowitą większą niż stopień wielomianu obiektu")
                self.button_metoda.setEnabled(False)

            else:
                self.pole_N.setStyleSheet("color: #484848; background-color: white")
                self.blad_N.setText("")

        elif pole_text.objectName() == "Liczba próbek":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Wpisz liczbę całkowitą większą niż stopień wielomianu obiektu")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not self.rzad < tekst or not tekst == int(tekst):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Musi zawierać liczbę całkowitą większą niż stopień wielomianu obiektu")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white")
                self.blad_N.setText("")

        elif pole_text.objectName().startswith('Zakres'):
            try:
                zakr_min = float(self.pole_zakr_min.text())
            except:
                zakr_min = None

            try:
                zakr_max = float(self.pole_zakr_max.text())
            except:
                zakr_max = None

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakres.setText("Musi zawierać liczby")
                self.button_metoda.setEnabled(False)

                if zakr_min is not None:
                    self.pole_zakr_min.setStyleSheet("color: #484848; background-color: white;")

                if zakr_max is not None:
                    self.pole_zakr_max.setStyleSheet("color: #484848; background-color: white;")

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakres.setText("")

                if zakr_min is None or zakr_max is None:
                    self.blad_zakres.setText("Musi zawierać liczby")
                    self.button_metoda.setEnabled(False)

            if zakr_max is not None and zakr_min is not None:

                if zakr_min >= zakr_max:
                    self.pole_zakr_min.setStyleSheet("color: red; background-color: white;")
                    self.pole_zakr_max.setStyleSheet("color: red; background-color: white;")
                    self.blad_zakres.setText("Maximum musi być większe od minimum")
                    self.button_metoda.setEnabled(False)

                else:
                    self.pole_zakr_min.setStyleSheet("color: #484848; background-color: white;")
                    self.pole_zakr_max.setStyleSheet("color: #484848; background-color: white;")
                    self.blad_zakres.setText("")


        elif pole_text.objectName() == "Zakłócenia":
            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Wpisz liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 <= tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Musi zawierać liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakl.setText("")

        if not (self.blad_N.text() or self.blad_zakres.text() or self.blad_zakl.text()):
            self.button_metoda.setEnabled(True)

    def change(self):
        but = self.sender()
        if not but.isChecked():
            but.setChecked(not but.isChecked())

        for i in [self.button_sekw, self.button_los_sekw, self.button_los]:
            if i != but:
                i.setChecked(False)


    def edit(self, rzad):
        self.rzad = rzad
        self.sprawdz()

    def result(self):
        N = int(self.pole_N.text())
        range_min = float(self.pole_zakr_min.text())
        range_max = float(self.pole_zakr_max.text())
        for but in [self.button_sekw, self.button_los_sekw, self.button_los]:
            if but.isChecked():
                wymuszenie_typ = but.objectName()
        zakl = float(self.pole_zakl.text())
        return N, range_min, range_max, wymuszenie_typ, zakl


class WidokParametrySymulacjiNielin(QWidget):
    def __init__(self):
        super().__init__()

        self.min_N = 4

        self.rzad = 1
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY SYMULACJI OBIEKTU NIELINIOWEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_N = QHBoxLayout()
        self.layout_row_N.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_N = QLabel("Liczba próbek:")
        self.napis_N.setFont(self.font_s)
        self.layout_row_N.addWidget(self.napis_N)
        self.pole_N = QLineEdit(self)
        self.pole_N.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_N.setText("1000")
        self.pole_N.setObjectName("Liczba próbek")
        self.layout_row_N.addWidget(self.pole_N)

        self.layout_row_blad_N = QHBoxLayout()
        self.blad_N = QLabel("")
        self.blad_N.setStyleSheet("color: red;")
        self.blad_N.setFont(self.font_s)
        self.layout_row_blad_N.addWidget(self.blad_N)
        self.layout_row_blad_N.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakres = QHBoxLayout()
        self.layout_row_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakr_min = QLabel("Minimum:")
        self.napis_zakr_min.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_min)
        self.pole_zakr_min = QLineEdit(self)
        self.pole_zakr_min.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_min.setText("0")
        self.pole_zakr_min.setObjectName("Zakres 1")
        self.layout_row_zakres.addWidget(self.pole_zakr_min)

        self.layout_row_zakres.addSpacing(30)

        self.napis_zakr_max = QLabel("Maximum:")
        self.napis_zakr_max.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_max)
        self.pole_zakr_max = QLineEdit(self)
        self.pole_zakr_max.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_max.setText("10")
        self.pole_zakr_max.setObjectName("Zakres 2")
        self.layout_row_zakres.addWidget(self.pole_zakr_max)

        self.layout_row_blad_zakres = QHBoxLayout()
        self.blad_zakres = QLabel("")
        self.blad_zakres.setStyleSheet("color: red;")
        self.blad_zakres.setFont(self.font_s)
        self.layout_row_blad_zakres.addWidget(self.blad_zakres)
        self.layout_row_blad_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakl = QHBoxLayout()
        self.layout_row_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakl = QLabel("Odchylenie standardowe zakłóceń:")
        self.napis_zakl.setFont(self.font_s)
        self.layout_row_zakl.addWidget(self.napis_zakl)
        self.pole_zakl = QLineEdit(self)
        self.pole_zakl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakl.setText("0.1")
        self.pole_zakl.setObjectName("Zakłócenia")
        self.layout_row_zakl.addWidget(self.pole_zakl)

        self.layout_row_blad_zakl = QHBoxLayout()
        self.blad_zakl = QLabel("")
        self.blad_zakl.setStyleSheet("color: red;")
        self.blad_zakl.setFont(self.font_s)
        self.layout_row_blad_zakl.addWidget(self.blad_zakl)
        self.layout_row_blad_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_metoda = QPushButton("Wybór algorytmu")
        self.layout_row_buttons.addWidget(self.button_metoda)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_N)
        self.main_layout.addLayout(self.layout_row_blad_N)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakres)
        self.main_layout.addLayout(self.layout_row_blad_zakres)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakl)
        self.main_layout.addLayout(self.layout_row_blad_zakl)
        self.main_layout.addSpacing(100)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_N.textChanged.connect(self.sprawdz)
        self.pole_zakr_min.textChanged.connect(self.sprawdz)
        self.pole_zakr_max.textChanged.connect(self.sprawdz)
        self.pole_zakl.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text is None:
            if not self.min_N <= int(self.pole_N.text()):
                self.pole_N.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Musi zawierać liczbę całkowitą większą lub równą niż liczba parametrów obiektu")
                self.button_metoda.setEnabled(False)

            else:
                self.pole_N.setStyleSheet("color: #484848; background-color: white")
                self.blad_N.setText("")

        elif pole_text.objectName() == "Liczba próbek":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Wpisz liczbę całkowitą większą lub równą niż liczba parametrów obiektu")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not self.min_N <= tekst or not tekst == int(tekst):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Musi zawierać liczbę całkowitą większą lub równą niż liczba parametrów obiektu")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white")
                self.blad_N.setText("")


        elif pole_text.objectName().startswith('Zakres'):
            try:
                zakr_min = float(self.pole_zakr_min.text())
            except:
                zakr_min = None

            try:
                zakr_max = float(self.pole_zakr_max.text())
            except:
                zakr_max = None

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakres.setText("Musi zawierać liczby")
                self.button_metoda.setEnabled(False)

                if zakr_min is not None:
                    self.pole_zakr_min.setStyleSheet("color: #484848; background-color: white;")

                if zakr_max is not None:
                    self.pole_zakr_max.setStyleSheet("color: #484848; background-color: white;")

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakres.setText("")

                if zakr_min is None or zakr_max is None:
                    self.blad_zakres.setText("Musi zawierać liczby")
                    self.button_metoda.setEnabled(False)

            if zakr_max is not None and zakr_min is not None:

                if zakr_min >= zakr_max:
                    self.pole_zakr_min.setStyleSheet("color: red; background-color: white;")
                    self.pole_zakr_max.setStyleSheet("color: red; background-color: white;")
                    self.blad_zakres.setText("Maximum musi być większe od miminum")
                    self.button_metoda.setEnabled(False)

                else:
                    self.pole_zakr_min.setStyleSheet("color: #484848; background-color: white;")
                    self.pole_zakr_max.setStyleSheet("color: #484848; background-color: white;")
                    self.blad_zakres.setText("")

        elif pole_text.objectName() == "Zakłócenia":
            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Wpisz liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 <= tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Musi zawierać liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakl.setText("")

        if not (self.blad_N.text() or self.blad_zakres.text() or self.blad_zakl.text()):
            self.button_metoda.setEnabled(True)

    def edit(self, min_N):
        self.min_N = min_N
        self.sprawdz()

    def result(self):
        N = int(self.pole_N.text())
        zakr_min = float(self.pole_zakr_min.text())
        zakr_max = float(self.pole_zakr_max.text())
        zakl = float(self.pole_zakl.text())
        return N, zakr_min, zakr_max, zakl


class WidokParametrySymulacjiDynamiczny(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY SYMULACJI OBIEKTU DYNAMICZNEGO")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_N = QHBoxLayout()
        self.layout_row_N.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_N = QLabel("Liczba próbek:")
        self.napis_N.setFont(self.font_s)
        self.layout_row_N.addWidget(self.napis_N)
        self.pole_N = QLineEdit(self)
        self.pole_N.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_N.setText("1000")
        self.pole_N.setObjectName("Liczba próbek")
        self.layout_row_N.addWidget(self.pole_N)

        self.layout_row_blad_N = QHBoxLayout()
        self.blad_N = QLabel("")
        self.blad_N.setStyleSheet("color: red;")
        self.blad_N.setFont(self.font_s)
        self.layout_row_blad_N.addWidget(self.blad_N)
        self.layout_row_blad_N.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakres = QHBoxLayout()
        self.layout_row_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakr_max = QLabel("Czas obserwacji:")
        self.napis_zakr_max.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.napis_zakr_max)
        self.pole_zakr_max = QLineEdit(self)
        self.pole_zakr_max.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakr_max.setText("20")
        self.pole_zakr_max.setObjectName("Zakres 2")
        self.layout_row_zakres.addWidget(self.pole_zakr_max)
        self.s = QLabel("[s]")
        self.s.setFont(self.font_s)
        self.layout_row_zakres.addWidget(self.s)

        self.layout_row_blad_zakres = QHBoxLayout()
        self.blad_zakres = QLabel("")
        self.blad_zakres.setStyleSheet("color: red;")
        self.blad_zakres.setFont(self.font_s)
        self.layout_row_blad_zakres.addWidget(self.blad_zakres)
        self.layout_row_blad_zakres.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakl_w = QHBoxLayout()
        self.layout_row_zakl_w.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakl_w = QLabel("Odchylenie standardowe sygnału wymuszającego:")
        self.napis_zakl_w.setFont(self.font_s)
        self.layout_row_zakl_w.addWidget(self.napis_zakl_w)
        self.pole_zakl_w = QLineEdit(self)
        self.pole_zakl_w.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakl_w.setText("1")
        self.pole_zakl_w.setObjectName("Zakłócenia_w")
        self.layout_row_zakl_w.addWidget(self.pole_zakl_w)

        self.layout_row_blad_zakl_w = QHBoxLayout()
        self.blad_zakl_w = QLabel("")
        self.blad_zakl_w.setStyleSheet("color: red;")
        self.blad_zakl_w.setFont(self.font_s)
        self.layout_row_blad_zakl_w.addWidget(self.blad_zakl_w)
        self.layout_row_blad_zakl_w.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zakl = QHBoxLayout()
        self.layout_row_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zakl = QLabel("Odchylenie standardowe zakłóceń:")
        self.napis_zakl.setFont(self.font_s)
        self.layout_row_zakl.addWidget(self.napis_zakl)
        self.pole_zakl = QLineEdit(self)
        self.pole_zakl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zakl.setText("0.01")
        self.pole_zakl.setObjectName("Zakłócenia")
        self.layout_row_zakl.addWidget(self.pole_zakl)

        self.layout_row_blad_zakl = QHBoxLayout()
        self.blad_zakl = QLabel("")
        self.blad_zakl.setStyleSheet("color: red;")
        self.blad_zakl.setFont(self.font_s)
        self.layout_row_blad_zakl.addWidget(self.blad_zakl)
        self.layout_row_blad_zakl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_metoda = QPushButton("Wybór algorytmu")
        self.layout_row_buttons.addWidget(self.button_metoda)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_N)
        self.main_layout.addLayout(self.layout_row_blad_N)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakres)
        self.main_layout.addLayout(self.layout_row_blad_zakres)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakl_w)
        self.main_layout.addLayout(self.layout_row_blad_zakl_w)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_zakl)
        self.main_layout.addLayout(self.layout_row_blad_zakl)
        self.main_layout.addSpacing(100)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_N.textChanged.connect(self.sprawdz)
        self.pole_zakr_max.textChanged.connect(self.sprawdz)
        self.pole_zakl.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == "Liczba próbek":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Wpisz liczbę całkowitą większą od 10")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 10 < tekst or not tekst == int(tekst):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N.setText("Musi zawierać liczbę całkowitą większą od 10")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white")
                self.blad_N.setText("")


        if pole_text.objectName().startswith('Zakres'):
            pole_text = self.sender()

            try:
                tekst = float(pole_text.text())
            except:
                tekst = None

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakres.setText("Wpisz liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakres.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 < tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakres.setText("Musi zawierać liczbę dodatnią")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakres.setText("")

        if pole_text.objectName() == "Zakłócenia_w":
            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl_w.setText("Wpisz liczbę dodatnią")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl_w.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 < tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl_w.setText("Musi zawierać liczbę dodatnią")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakl_w.setText("")

        if pole_text.objectName() == "Zakłócenia":
            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Wpisz liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Nie może zawierać liter")
                self.button_metoda.setEnabled(False)

            elif not 0 <= tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zakl.setText("Musi zawierać liczbę nieujemną")
                self.button_metoda.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zakl.setText("")

        if not (self.blad_N.text() or self.blad_zakres.text() or self.blad_zakl.text()):
            self.button_metoda.setEnabled(True)

    def result(self):
        N = int(self.pole_N.text())
        zakr_max = float(self.pole_zakr_max.text())
        zakl_w = float(self.pole_zakl_w.text())
        zakl = float(self.pole_zakl.text())
        return N, zakr_max, zakl_w, zakl


class WidokMetoda(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.font_l = QFont()
        self.font_l.setPointSize(20)
        self.font_s = QFont()
        self.font_s.setPointSize(12)

        self.title = QLabel("ALGORYTM")
        self.title.setFont(self.font_l)

        self.layout_title = QVBoxLayout()
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.napis_nieskorel = QLabel('Zadane zakłócenia nieskorelowane:')
        self.napis_nieskorel.setFont(self.font_s)
        self.button_LS = QPushButton("LS")
        self.button_RLS = QPushButton("RLS")
        self.napis_skorel = QLabel('Możliwość zadania zakłóceń skorelowanych i nieskorelowanych:')
        self.napis_skorel.setFont(self.font_s)
        self.button_GLS = QPushButton("GLS")
        self.button_return = QPushButton("Powrót")

        self.layout_napis_nieskorel = QHBoxLayout()
        self.layout_button_LS = QHBoxLayout()
        self.layout_button_RLS = QHBoxLayout()
        self.layout_napis_skorel = QHBoxLayout()
        self.layout_button_GLS = QHBoxLayout()
        self.layout_button_return = QHBoxLayout()

        self.layout_napis_nieskorel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_LS.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_RLS.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_napis_skorel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_GLS.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_button_return.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_napis_nieskorel.addWidget(self.napis_nieskorel)
        self.layout_button_LS.addWidget(self.button_LS)
        self.layout_button_RLS.addWidget(self.button_RLS)
        self.layout_napis_skorel.addWidget(self.napis_skorel)
        self.layout_button_GLS.addWidget(self.button_GLS)
        self.layout_button_return.addWidget(self.button_return)

        self.layout.addLayout(self.layout_title)
        self.layout.addSpacing(40)
        self.layout.addLayout(self.layout_napis_nieskorel)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.layout_button_LS)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.layout_button_RLS)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.layout_napis_skorel)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.layout_button_GLS)
        self.layout.addSpacing(50)
        self.layout.addLayout(self.layout_button_return)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

class WidokMetodaNiestacjo(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.title = QLabel("ALGORYTM")
        self.title.setFont(self.font_l)

        self.layout_title = QVBoxLayout()
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_RLS_zap = QPushButton("WRLS")
        self.button_return = QPushButton("Powrót")

        self.layout.addLayout(self.layout_title)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.button_RLS_zap)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.button_return)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

class WidokMetodaNielin(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.title = QLabel("ALGORYTM")
        self.title.setFont(self.font_l)

        self.layout_title = QVBoxLayout()
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_NLS = QPushButton("NLS")
        self.button_return = QPushButton("Powrót")

        self.layout.addLayout(self.layout_title)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.button_NLS)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.button_return)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class WidokMetodaDynamiczny(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.title = QLabel("ALGORYTM")
        self.title.setFont(self.font_l)

        self.layout_title = QVBoxLayout()
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_korel = QPushButton("Korelacyjny")
        self.button_return = QPushButton("Powrót")

        self.layout.addLayout(self.layout_title)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.button_korel)
        self.layout.addSpacing(40)
        self.layout.addWidget(self.button_return)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


class WidokRLS(QWidget):
    def __init__(self):
        super().__init__()

        self.N = 100
        self.rzad = 1

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY ALGORYTMU RLS")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_choice = QHBoxLayout()
        self.layout_row_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_arb = QPushButton("Podejście arbitralne")
        self.button_arb.setObjectName('arb')
        self.button_alt = QPushButton("Podejście alternatywne")
        self.button_alt.setObjectName('alt')
        self.button_arb.setCheckable(True)
        self.button_alt.setCheckable(True)
        self.layout_row_choice.addWidget(self.button_arb)
        self.layout_row_choice.addSpacing(20)
        self.layout_row_choice.addWidget(self.button_alt)

        self.button_arb.clicked.connect(self.change)
        self.button_alt.clicked.connect(self.change)

        self.layout_row_alfa = QHBoxLayout()
        self.layout_row_alfa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_alfa = QLabel("Skalar początkowej macierzy kowariancji:")
        self.napis_alfa.setFont(self.font_s)
        self.layout_row_alfa.addWidget(self.napis_alfa)
        self.pole_alfa = QLineEdit(self)
        self.pole_alfa.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_alfa.setText("100000000")
        self.pole_alfa.setObjectName("alfa")
        self.layout_row_alfa.addWidget(self.pole_alfa)

        self.layout_row_blad_alfa = QHBoxLayout()
        self.blad_alfa = QLabel("")
        self.blad_alfa.setStyleSheet("color: red;")
        self.blad_alfa.setFont(self.font_s)
        self.layout_row_blad_alfa.addWidget(self.blad_alfa)
        self.layout_row_blad_alfa.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_b0 = QHBoxLayout()
        self.layout_row_b0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_b0 = QLabel("Początkowe wartości współczynników modelu:")
        self.napis_b0.setFont(self.font_s)
        self.layout_row_b0.addWidget(self.napis_b0)

        self.pola_b0 = []

        self.layout_row_blad_b0 = QHBoxLayout()
        self.blad_b0 = QLabel("")
        self.blad_b0.setFont(self.font_s)
        self.blad_b0.setStyleSheet("color: red;")
        self.layout_row_blad_b0.addWidget(self.blad_b0)
        self.layout_row_blad_b0.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_N_pocz = QHBoxLayout()
        self.layout_row_N_pocz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_N_pocz = QLabel("Liczba próbek początkowych algorytmu LS:")
        self.napis_N_pocz.setFont(self.font_s)
        self.layout_row_N_pocz.addWidget(self.napis_N_pocz)
        self.pole_N_pocz = QLineEdit(self)
        self.pole_N_pocz.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_N_pocz.setText("10")
        self.pole_N_pocz.setObjectName("N_pocz")
        self.layout_row_N_pocz.addWidget(self.pole_N_pocz)

        self.layout_row_blad_N_pocz = QHBoxLayout()
        self.blad_N_pocz = QLabel("")
        self.blad_N_pocz.setStyleSheet("color: red;")
        self.blad_N_pocz.setFont(self.font_s)
        self.layout_row_blad_N_pocz.addWidget(self.blad_N_pocz)
        self.layout_row_blad_N_pocz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_wynik = QPushButton("Wynik")
        self.layout_row_buttons.addWidget(self.button_wynik)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_choice)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.layout_row_alfa)
        self.main_layout.addLayout(self.layout_row_blad_alfa)
        self.main_layout.addLayout(self.layout_row_b0)
        self.main_layout.addLayout(self.layout_row_blad_b0)
        self.main_layout.addLayout(self.layout_row_N_pocz)
        self.main_layout.addLayout(self.layout_row_blad_N_pocz)
        self.main_layout.addSpacing(100)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.button_arb.clicked.connect(self.sprawdz)
        self.button_alt.clicked.connect(self.sprawdz)
        self.button_arb.click()
        self.pole_alfa.textChanged.connect(self.sprawdz)
        self.pole_N_pocz.textChanged.connect(self.sprawdz)
        self.pola_status = list(np.zeros((1,)))

        for pole in self.pola_b0:
            pole.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == "alfa":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_alfa.setText("Wpisz liczbę dodatnią")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_alfa.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_alfa.setText("Musi zawierać liczby dodatnie")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_alfa.setText("")

        if pole_text.objectName().startswith('Pole'):
            numer = int(pole_text.objectName()[-1])

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_b0.setText("Musi zawierać liczby")
                self.pola_status[numer - 1] = 1
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status[numer - 1] = 0
                if self.pola_status == list(np.zeros((len(self.pola_b0) // 2, 1))):
                    self.blad_b0.setText("")

        if pole_text.objectName() == "N_pocz":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N_pocz.setText("Wpisz liczbę całkowitą dodatnią")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_N_pocz.setText("Nie może zawierać liter")
                self.button_wynik.setEnabled(False)

            else:
                try:
                    if not self.rzad < int(tekst) < self.N:
                        raise
                    pole_text.setStyleSheet("color: #484848; background-color: white")
                    self.blad_N_pocz.setText("")
                except:
                    pole_text.setStyleSheet("color: red; background-color: white")
                    self.blad_N_pocz.setText("Musi zawierać liczbę całkowitą większą niż stopień wielomianu modelu i mniejszą niż liczba próbek")
                    self.button_wynik.setEnabled(False)

        if self.button_arb.isChecked():
            if not (self.blad_alfa.text() or self.blad_b0.text()):
                self.button_wynik.setEnabled(True)
            else:
                self.button_wynik.setEnabled(False)
        if self.button_alt.isChecked():
            if not self.blad_N_pocz.text():
                self.button_wynik.setEnabled(True)
            else:
                self.button_wynik.setEnabled(False)

    def change(self):
        but = self.sender()
        if not but.isChecked():
            but.setChecked(not but.isChecked())
        else:
            if but.objectName() == 'alt':
                self.button_arb.setChecked(False)
                self.napis_alfa.setVisible(False)
                self.pole_alfa.setVisible(False)
                self.blad_alfa.setVisible(False)
                self.napis_b0.setVisible(False)
                for pole in self.pola_b0:
                    pole.setVisible(False)
                self.blad_b0.setVisible(False)

                self.napis_N_pocz.setVisible(True)
                self.pole_N_pocz.setVisible(True)
                self.blad_N_pocz.setVisible(True)

            else:
                self.button_alt.setChecked(False)
                self.napis_alfa.setVisible(True)
                self.pole_alfa.setVisible(True)
                self.blad_alfa.setVisible(True)
                self.napis_b0.setVisible(True)
                for pole in self.pola_b0:
                    pole.setVisible(True)
                self.blad_b0.setVisible(True)

                self.napis_N_pocz.setVisible(False)
                self.pole_N_pocz.setVisible(False)
                self.blad_N_pocz.setVisible(False)

    def edit(self, rzad, N):
        self.rzad = rzad
        self.N = N

        while len(self.pola_b0):
            wid = self.pola_b0.pop(-1)
            self.layout_row_b0.removeWidget(wid)
            wid.deleteLater()

        self.pola_b0.clear()


        for i in range(rzad+1):
            napis = QLabel(f"x<sup>{rzad-i}</sup>:")
            napis.setFont(self.font_s)
            self.layout_row_b0.addWidget(napis)
            self.pola_b0.append(napis)
            pole = QLineEdit(self)
            pole.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            pole.setAlignment(Qt.AlignmentFlag.AlignLeft)
            pole.setText("0")
            pole.setObjectName(f"Pole_b0_{i + 1}")
            self.layout_row_b0.addWidget(pole)
            self.pola_b0.append(pole)

        self.pola_status = list(np.zeros((len(self.pola_b0) // 2, 1)))
        self.blad_b0.setText("")

        for pole in self.pola_b0:
            if self.button_alt.isChecked():
                pole.setVisible(False)
            else:
                pole.setVisible(True)
            if isinstance(pole, QLineEdit):
                pole.textChanged.connect(self.sprawdz)

        if not (self.blad_alfa.text() or self.blad_b0.text()) and self.button_arb.isChecked():
            self.button_wynik.setEnabled(True)



    def result(self):
        if self.button_arb.isChecked():
            alfa = float(self.pole_alfa.text())
            b0 = []
            N_pocz = None
            for pole in self.pola_b0:
                if isinstance(pole, QLineEdit):
                    b0.append(float(pole.text()))
        else:
            alfa = None
            b0 = []
            N_pocz = int(self.pole_N_pocz.text())
            for pole in self.pola_b0:
                if isinstance(pole, QLineEdit):
                    b0.append(None)

        return alfa, np.array(b0).reshape(1, len(b0)), N_pocz


class WidokRLSZap(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font = QFont()
        self.font.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY ALGORYTMU WRLS")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_alfa = QHBoxLayout()
        self.layout_row_alfa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_alfa = QLabel("Skalar początkowej macierzy kowariancji:")
        self.napis_alfa.setFont(self.font)
        self.layout_row_alfa.addWidget(self.napis_alfa)
        self.pole_alfa = QLineEdit(self)
        self.pole_alfa.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_alfa.setText("100000000")
        self.pole_alfa.setObjectName("alfa")
        self.layout_row_alfa.addWidget(self.pole_alfa)

        self.layout_row_blad_alfa = QHBoxLayout()
        self.blad_alfa = QLabel("")
        self.blad_alfa.setStyleSheet("color: red;")
        self.blad_alfa.setFont(self.font)
        self.layout_row_blad_alfa.addWidget(self.blad_alfa)
        self.layout_row_blad_alfa.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_b0 = QHBoxLayout()
        self.layout_row_b0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_b0 = QLabel("Początkowe wartości współczynników modelu:")
        self.napis_b0.setFont(self.font)
        self.layout_row_b0.addWidget(self.napis_b0)

        self.pola_b0 = []

        self.layout_row_blad_b0 = QHBoxLayout()
        self.blad_b0 = QLabel("")
        self.blad_b0.setFont(self.font)
        self.blad_b0.setStyleSheet("color: red;")
        self.layout_row_blad_b0.addWidget(self.blad_b0)
        self.layout_row_blad_b0.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_zap = QHBoxLayout()
        self.layout_row_zap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_zap = QLabel("Współczynnik zapominania:")
        self.napis_zap.setFont(self.font)
        self.layout_row_zap.addWidget(self.napis_zap)
        self.pole_zap = QLineEdit(self)
        self.pole_zap.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_zap.setText("0.9")
        self.pole_zap.setObjectName("Zapominanie")
        self.layout_row_zap.addWidget(self.pole_zap)

        self.layout_row_blad_zap = QHBoxLayout()
        self.blad_zap = QLabel("")
        self.blad_zap.setStyleSheet("color: red;")
        self.blad_zap.setFont(self.font)
        self.layout_row_blad_zap.addWidget(self.blad_zap)
        self.layout_row_blad_zap.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_wynik = QPushButton("Wynik")
        self.layout_row_buttons.addWidget(self.button_wynik)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_alfa)
        self.main_layout.addLayout(self.layout_row_blad_alfa)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_b0)
        self.main_layout.addLayout(self.layout_row_blad_b0)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_row_zap)
        self.main_layout.addLayout(self.layout_row_blad_zap)
        self.main_layout.addSpacing(100)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_alfa.textChanged.connect(self.sprawdz)

        self.pola_status = list(np.zeros((1,)))

        self.pole_zap.textChanged.connect(self.sprawdz)

    def sprawdz(self):
        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == "alfa":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_alfa.setText("Wpisz liczbę dodatnią")

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_alfa.setText("Zawiera litery")

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_alfa.setText("Musi zawierać liczby dodatnie")

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_alfa.setText("")

        if pole_text.objectName().startswith('Pole'):
            numer = int(pole_text.objectName()[-1])

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_b0.setText("Musi zawierać liczby")
                self.pola_status[numer - 1] = 1

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status[numer - 1] = 0
                if self.pola_status == list(np.zeros((len(self.pola_b0) // 2, 1))):
                    self.blad_b0.setText("")

        if pole_text.objectName() == "Zapominanie":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zap.setText("Wpisz liczbę w zakresie 0-1")

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zap.setText("Zawiera litery")

            elif not 0 <= tekst <= 1:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_zap.setText("Musi zawierać liczbę w zakresie 0-1")

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_zap.setText("")

        if not (self.blad_alfa.text() or self.blad_b0.text() or self.blad_zap.text()):
            self.button_wynik.setEnabled(True)
        else:
            self.button_wynik.setEnabled(False)


    def edit_b0(self, rzad):
        while len(self.pola_b0):
            wid = self.pola_b0.pop(-1)
            self.layout_row_b0.removeWidget(wid)
            wid.deleteLater()

        self.pola_b0.clear()


        for i in range(rzad+1):
            napis = QLabel(f"x<sup>{rzad-i}</sup>:")
            napis.setFont(self.font)
            self.layout_row_b0.addWidget(napis)
            self.pola_b0.append(napis)
            pole = QLineEdit(self)
            pole.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            pole.setAlignment(Qt.AlignmentFlag.AlignLeft)
            pole.setText("0")
            pole.setObjectName(f"Pole_b0_{i + 1}")
            self.layout_row_b0.addWidget(pole)
            self.pola_b0.append(pole)

        self.pola_status = list(np.zeros((len(self.pola_b0) // 2, 1)))
        self.blad_b0.setText("")

        for pole in self.pola_b0:
            if isinstance(pole, QLineEdit):
                pole.textChanged.connect(self.sprawdz)

        if not (self.blad_alfa.text() or self.blad_b0.text() or self.blad_zap.text()):
            self.button_wynik.setEnabled(True)

    def result(self):
        alfa = float(self.pole_alfa.text())
        b0 = []
        wsp_zap = float(self.pole_zap.text())

        for pole in self.pola_b0:
            if isinstance(pole, QLineEdit):
                b0.append(float(pole.text()))

        return alfa, np.array(b0).reshape(1, len(b0)), wsp_zap


class WidokGLS(QWidget):

    def __init__(self):
        super().__init__()

        self.N = 100
        self.algorytm = 'GLS'

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("MACIERZ KOWARIANCJI ZAKŁÓCEŃ")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_pola = QVBoxLayout()
        self.layout_pola.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pola = []

        self.layout_manipulacja = QHBoxLayout()
        self.button_minus = QPushButton('-')
        self.button_minus.setObjectName('plusminus')
        self.button_minus.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.button_minus.setEnabled(False)
        self.napis_manipulacja = QLabel("Usuń / Dodaj przekątną")
        self.button_plus = QPushButton('+')
        self.button_plus.setObjectName('plusminus')
        self.button_plus.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.napis_manipulacja.setFont(self.font_s)

        self.layout_manipulacja.addSpacing(250)
        self.layout_manipulacja.addWidget(self.button_minus)
        self.layout_manipulacja.addSpacing(10)
        self.layout_manipulacja.addWidget(self.napis_manipulacja)
        self.layout_manipulacja.addSpacing(10)
        self.layout_manipulacja.addWidget(self.button_plus)
        self.layout_manipulacja.addSpacing(250)

        self.button_minus.clicked.connect(self.odejmij)
        self.button_plus.clicked.connect(self.dodaj)
        self.button_minus.clicked.connect(self.sprawdz)
        self.button_plus.clicked.connect(self.sprawdz)

        self.layout_blad = QHBoxLayout()
        self.blad_przek = QLabel("")
        self.blad_przek.setFont(self.font_s)
        self.blad_przek.setStyleSheet("color: red;")

        self.blad_wart = QLabel("")
        self.blad_wart.setFont(self.font_s)
        self.blad_wart.setStyleSheet("color: red;")

        self.layout_blad.addWidget(self.blad_przek)
        self.layout_blad.addWidget(self.blad_wart)

        self.layout_check_LS = QHBoxLayout()
        self.check_LS = QCheckBox("Przeprowadzenie obliczenia przy pomocy algorytmu LS")
        self.check_LS.stateChanged.connect(self.check_LS_change)
        self.layout_check_LS.addWidget(self.check_LS)
        self.layout_check_LS.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_macierz = QVBoxLayout()
        self.button_macierz = QPushButton('Zaproponuj macierz kowariancji zakłóceń')
        self.button_macierz.setObjectName('propoz')
        self.layout_macierz.addWidget(self.button_macierz)
        self.button_macierz.setVisible(False)
        self.button_macierz.clicked.connect(self.macierz_cov)
        self.blad_macierz = QLabel('')
        self.blad_macierz.setStyleSheet("color: red")
        self.blad_macierz.setFont(self.font_s)
        self.layout_macierz.addWidget(self.blad_macierz)
        self.layout_macierz.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_wynik = QPushButton("Wynik")
        self.layout_row_buttons.addWidget(self.button_wynik)
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addSpacing(40)
        self.main_layout.addLayout(self.layout_pola)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_manipulacja)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.layout_blad)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.main_layout.addLayout(self.layout_check_LS)
        self.main_layout.addLayout(self.layout_macierz)
        self.main_layout.addLayout(self.layout_row_buttons)

        self.setLayout(self.main_layout)

        self.pola_status = [0, 0]
        self.pola_status_p = []
        self.pola_status_w = []


    def sprawdz(self):
        pole_text = self.sender()

        self.blad_macierz.setText('')

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if pole_text.objectName() == 'plusminus':
            if not 1 in self.pola_status_p:
                self.pola_status[0] = 0
            if not 1 in self.pola_status_w:
                self.pola_status[1] = 0

        elif pole_text.objectName().startswith('P'):
            numer = int(pole_text.objectName()[-1])

            if tekst is None or float(tekst) != int(tekst) or int(tekst) <= 0 or int(tekst) >= self.N:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przek.setText("Wskazane pola nie zawierają licz całkowitych dodatnich mniejszych od liczby próbek")
                self.pola_status_p[numer] = 1
                self.pola_status[0] = 1
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status_p[numer] = 0
                if self.pola_status_p == list(np.zeros((len(self.pola), 1))):
                    self.blad_przek.setText("")
                    self.pola_status[0] = 0

        elif pole_text.objectName().startswith('W'):
            numer = int(pole_text.objectName()[-1])

            if tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_wart.setText("Wskazane pola zawierają tekst")
                self.pola_status_w[numer] = 1
                self.pola_status[1] = 1
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.pola_status_w[numer] = 0
                if self.pola_status_w == list(np.zeros((len(self.pola), 1))):
                    self.blad_wart.setText("")
                    self.pola_status[1] = 0

        if not self.pola_status[0]:
            self.blad_przek.setText("")
        if not self.pola_status[1]:
            self.blad_wart.setText("")
        if self.pola_status == [0, 0]:
            self.button_wynik.setEnabled(True)

    def dodaj(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        napis_przek = QLabel('Odległość od przekątnej głównej:')
        napis_przek.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        napis_przek.setFont(self.font_s)
        pole_przek = QLineEdit(self)
        pole_przek.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        pole_przek.setText(f'{len(self.pola) + 1}')
        pole_przek.setObjectName(f'P{len(self.pola)}')
        napis_wart = QLabel('Wartość:')
        napis_wart.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        napis_wart.setFont(self.font_s)
        pole_wart = QLineEdit(self)
        pole_wart.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        pole_wart.setText('1')
        pole_wart.setObjectName(f'W{len(self.pola)}')

        pole_przek.textChanged.connect(self.sprawdz)
        pole_wart.textChanged.connect(self.sprawdz)

        self.pola.append(layout)

        layout.addWidget(napis_przek)
        layout.addWidget(pole_przek)
        layout.addSpacing(50)
        layout.addWidget(napis_wart)
        layout.addWidget(pole_wart)

        self.layout_pola.addLayout(layout)

        self.pola_status_p.append(0)
        self.pola_status_w.append(0)

        if len(self.pola) == 10:
            self.button_plus.setEnabled(False)
        else:
            self.button_minus.setEnabled(True)

    def odejmij(self):
        usun = self.pola.pop(-1)
        while usun.count():
            item = usun.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.layout_pola.removeItem(usun)
        usun.deleteLater()

        self.pola_status_p.pop(-1)
        self.pola_status_w.pop(-1)

        if len(self.pola) == 0:
            self.button_minus.setEnabled(False)
        else:
            self.button_plus.setEnabled(True)

    def check_LS_change(self, state):
        if state:
            self.algorytm = 'LS'
        else:
            self.algorytm = 'GLS'

    def macierz_cov(self):
        self.button_macierz.setVisible(False)
        self.blad_macierz.setText('')
        przek_wart = self.parent().parent().ob_GLS.positive_matrix()
        for i, pole in enumerate(self.pola):
            pole.itemAt(4).widget().setText(f'{przek_wart[i][1]}')

    def edit_N(self, N):
        self.N = N

    def result(self):
        przek_wart = []
        for pole in self.pola:
            przek_wart.append([int(pole.itemAt(1).widget().text()), float(pole.itemAt(4).widget().text())])

        return self.algorytm, przek_wart


class WidokNLS(QWidget):
    def __init__(self):
        super().__init__()

        self.typ = 'sinus'

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font_s = QFont()
        self.font_s.setPointSize(12)
        self.font_l = QFont()
        self.font_l.setPointSize(20)

        self.layout_title = QVBoxLayout()
        self.title = QLabel("PARAMETRY ALGORYTMU NLS")
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.widget_wykr = QWidget()
        self.widget_wykr.setMaximumWidth(1000)
        self.layout_wykr = QVBoxLayout(self.widget_wykr)
        self.layout_wykr.addWidget(self.canvas)
        self.widget_wykr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setVisible(False)
        self.layout_wykres = QHBoxLayout()
        self.layout_wykres.addWidget(self.widget_wykr)
        self.layout_wykres.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_iter = QHBoxLayout()
        self.layout_row_iter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_iter = QLabel("Liczba pętli iteracyjnych:")
        self.napis_iter.setFont(self.font_s)
        self.layout_row_iter.addWidget(self.napis_iter)
        self.pole_iter = QLineEdit(self)
        self.pole_iter.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_iter.setText("10")
        self.pole_iter.setObjectName("iter")
        self.layout_row_iter.addWidget(self.pole_iter)

        self.layout_row_blad_iter = QHBoxLayout()
        self.blad_iter = QLabel("")
        self.blad_iter.setStyleSheet("color: red;")
        self.blad_iter.setFont(self.font_s)
        self.layout_row_blad_iter.addWidget(self.blad_iter)
        self.layout_row_blad_iter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_napis = QHBoxLayout()
        self.napis = QLabel("Początkowe wartości współczynników modelu:")
        self.napis.setFont(self.font_s)
        self.layout_row_napis.addWidget(self.napis)
        self.layout_row_napis.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_amp = QHBoxLayout()
        self.layout_row_amp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_amp = QLabel("Amplituda 1:")
        self.napis_amp.setFont(self.font_s)
        self.layout_row_amp.addWidget(self.napis_amp)
        self.pole_amp = QLineEdit(self)
        self.pole_amp.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_amp.setText("1")
        self.pole_amp.setObjectName("amp_1")
        self.layout_row_amp.addWidget(self.pole_amp)

        self.layout_row_amp.addSpacing(20)

        self.napis_amp_2 = QLabel("Amplituda 2:")
        self.napis_amp_2.setFont(self.font_s)
        self.layout_row_amp.addWidget(self.napis_amp_2)
        self.pole_amp_2 = QLineEdit(self)
        self.pole_amp_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_amp_2.setText("0.5")
        self.pole_amp_2.setObjectName("amp_2")
        self.layout_row_amp.addWidget(self.pole_amp_2)

        self.layout_row_blad_amp = QHBoxLayout()
        self.blad_amp = QLabel("")
        self.blad_amp.setStyleSheet("color: red;")
        self.blad_amp.setFont(self.font_s)
        self.blad_amp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_row_blad_amp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_row_blad_amp.addWidget(self.blad_amp, 1)

        self.blad_amp_2 = QLabel("")
        self.blad_amp_2.setStyleSheet("color: red;")
        self.blad_amp_2.setFont(self.font_s)
        self.blad_amp_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_row_blad_amp.addWidget(self.blad_amp_2, 1)
        self.blad_amp.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.blad_amp_2.setAlignment(Qt.AlignLeft | Qt.AlignLeft)

        self.layout_row_T = QHBoxLayout()
        self.layout_row_T.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_T = QLabel("Okres 1:")
        self.napis_T.setFont(self.font_s)
        self.layout_row_T.addWidget(self.napis_T)
        self.pole_T = QLineEdit(self)
        self.pole_T.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_T.setText("5")
        self.pole_T.setObjectName("T_1")
        self.layout_row_T.addWidget(self.pole_T)

        self.napis_st_czas = QLabel("Stała czasowa:")
        self.napis_st_czas.setFont(self.font_s)
        self.layout_row_T.addWidget(self.napis_st_czas)
        self.pole_st_czas = QLineEdit(self)
        self.pole_st_czas.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_st_czas.setText("5")
        self.pole_st_czas.setObjectName("st_czas")
        self.layout_row_T.addWidget(self.pole_st_czas)

        self.layout_row_T.addSpacing(20)

        self.napis_T_2 = QLabel("Okres 2:")
        self.napis_T_2.setFont(self.font_s)
        self.layout_row_T.addWidget(self.napis_T_2)
        self.pole_T_2 = QLineEdit(self)
        self.pole_T_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_T_2.setText("10")
        self.pole_T_2.setObjectName("T_2")
        self.layout_row_T.addWidget(self.pole_T_2)

        self.layout_row_blad_T = QHBoxLayout()
        self.blad_T = QLabel("")
        self.blad_T.setStyleSheet("color: red;")
        self.blad_T.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout_row_blad_T.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blad_T.setFont(self.font_s)
        self.layout_row_blad_T.addWidget(self.blad_T, 1)

        self.blad_T_2 = QLabel("")
        self.blad_T_2.setStyleSheet("color: red;")
        self.blad_T_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.blad_T_2.setFont(self.font_s)
        self.layout_row_blad_T.addWidget(self.blad_T_2, 1)
        self.blad_T.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.blad_T_2.setAlignment(Qt.AlignLeft | Qt.AlignLeft)

        self.blad_st_czas = QLabel("")
        self.blad_st_czas.setStyleSheet("color: red;")
        self.blad_st_czas.setFont(self.font_s)
        self.layout_row_blad_T.addWidget(self.blad_st_czas)
        self.blad_st_czas.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.pi = QLabel("∙π")
        self.pi.setFont(self.font_s)
        self.layout_row_przes = QHBoxLayout()
        self.layout_row_przes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_przes = QLabel("Faza 1:")
        self.napis_przes.setFont(self.font_s)
        self.layout_row_przes.addWidget(self.napis_przes)
        self.pole_przes = QLineEdit(self)
        self.pole_przes.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_przes.setText("0")
        self.pole_przes.setObjectName("przes_1")
        self.layout_row_przes.addWidget(self.pole_przes)
        self.layout_row_przes.addWidget(self.pi)

        self.layout_row_przes.addSpacing(20)

        self.pi_2 = QLabel("∙π")
        self.pi_2.setFont(self.font_s)
        self.napis_przes_2 = QLabel("Faza 2:")
        self.napis_przes_2.setFont(self.font_s)
        self.layout_row_przes.addWidget(self.napis_przes_2)
        self.pole_przes_2 = QLineEdit(self)
        self.pole_przes_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_przes_2.setText("0")
        self.pole_przes_2.setObjectName("przes_2")
        self.layout_row_przes.addWidget(self.pole_przes_2)
        self.layout_row_przes.addWidget(self.pi_2)

        self.layout_row_blad_przes = QHBoxLayout()
        self.blad_przes = QLabel("")
        self.blad_przes.setStyleSheet("color: red;")
        self.blad_przes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.blad_przes.setFont(self.font_s)
        self.layout_row_blad_przes.addWidget(self.blad_przes, 1)

        self.blad_przes_2 = QLabel("")
        self.blad_przes_2.setStyleSheet("color: red;")
        self.blad_przes_2.setFont(self.font_s)
        self.layout_row_blad_przes.addWidget(self.blad_przes_2, 1)
        self.layout_row_blad_przes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blad_przes.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.blad_przes_2.setAlignment(Qt.AlignLeft | Qt.AlignLeft)

        self.layout_row_skl = QHBoxLayout()
        self.layout_row_skl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_skl = QLabel("Składowa stała:")
        self.napis_skl.setFont(self.font_s)
        self.layout_row_skl.addWidget(self.napis_skl)
        self.pole_skl = QLineEdit(self)
        self.pole_skl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pole_skl.setText("0")
        self.pole_skl.setObjectName("skl")
        self.layout_row_skl.addWidget(self.pole_skl)

        self.layout_row_blad_skl = QHBoxLayout()
        self.blad_skl = QLabel("")
        self.blad_skl.setStyleSheet("color: red;")
        self.blad_skl.setFont(self.font_s)
        self.layout_row_blad_skl.addWidget(self.blad_skl)
        self.layout_row_blad_skl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_row_buttons = QHBoxLayout()
        self.layout_row_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Powrót")
        self.layout_row_buttons.addWidget(self.button_return)
        self.button_wynik = QPushButton("Wynik")
        self.layout_row_buttons.addWidget(self.button_wynik)

        self.main_layout.addLayout(self.layout_title)
        self.main_layout.addLayout(self.layout_wykres)
        self.main_layout.addLayout(self.layout_row_iter)
        self.main_layout.addLayout(self.layout_row_blad_iter)
        self.main_layout.addLayout(self.layout_row_napis)
        self.main_layout.addLayout(self.layout_row_skl)
        self.main_layout.addLayout(self.layout_row_blad_skl)
        self.main_layout.addLayout(self.layout_row_amp)
        self.main_layout.addLayout(self.layout_row_blad_amp)
        self.main_layout.addLayout(self.layout_row_T)
        self.main_layout.addLayout(self.layout_row_blad_T)
        self.main_layout.addLayout(self.layout_row_przes)
        self.main_layout.addLayout(self.layout_row_blad_przes)
        self.main_layout.addLayout(self.layout_row_buttons)
        self.setLayout(self.main_layout)

        self.pole_amp.textChanged.connect(self.sprawdz)
        self.pole_T.textChanged.connect(self.sprawdz)
        self.pole_przes.textChanged.connect(self.sprawdz)
        self.pole_amp_2.textChanged.connect(self.sprawdz)
        self.pole_T_2.textChanged.connect(self.sprawdz)
        self.pole_przes_2.textChanged.connect(self.sprawdz)
        self.pole_skl.textChanged.connect(self.sprawdz)
        self.pole_st_czas.textChanged.connect(self.sprawdz)
        self.pole_iter.textChanged.connect(self.sprawdz)

    def sprawdz(self):

        pole_text = self.sender()

        try:
            tekst = float(pole_text.text())
        except:
            tekst = None

        if self.sender() is None:
            pass

        elif pole_text.objectName() == "amp_1":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Wpisz liczbę")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_amp.setText("")

        elif pole_text.objectName() == "amp_2":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp_2.setText("Wpisz liczbę")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_amp_2.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_amp_2.setText("")

        elif pole_text.objectName() == "T_1":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Wpisz liczbę dodatnią")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T.setText("Musi zawierać liczbę dodatnią")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_T.setText("")

        elif pole_text.objectName() == "T_2":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T_2.setText("Wpisz liczbę dodatnią")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T_2.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            elif tekst <= 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_T_2.setText("Musi zawierać liczbę dodatnią")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_T_2.setText("")

        elif pole_text.objectName() == "przes_1":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes.setText("Wpisz liczbę")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_przes.setText("")

        elif pole_text.objectName() == "przes_2":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes_2.setText("Wpisz liczbę")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_przes_2.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_przes_2.setText("")

        elif pole_text.objectName() == "skl":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_skl.setText("Wpisz liczbę")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_skl.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_skl.setText("")

        elif pole_text.objectName() == "st_czas":
            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_st_czas.setText("Wpisz liczbę nieujemną")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_st_czas.setText("Zawiera litery")
                self.button_wynik.setEnabled(False)

            elif tekst < 0:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_st_czas.setText("Musi zawierać liczbę nieujemną")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_st_czas.setText("")

        elif pole_text.objectName() == "iter":

            if not len(pole_text.text()):
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_iter.setText("Wpisz liczbę całkowitą nieujemną")
                self.button_wynik.setEnabled(False)

            elif tekst is None:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_iter.setText("Nie może zawierać liter")
                self.button_wynik.setEnabled(False)

            elif not 0 <= tekst:
                pole_text.setStyleSheet("color: red; background-color: white")
                self.blad_iter.setText("Musi zawierać liczbę nieujemną")
                self.button_wynik.setEnabled(False)

            else:
                pole_text.setStyleSheet("color: #484848; background-color: white;")
                self.blad_iter.setText("")

        if self.typ == 'sinus':
            if not (self.blad_amp.text() or self.blad_T.text() or self.blad_przes.text()
                    or self.blad_skl.text() or self.blad_iter.text()):
                self.button_wynik.setEnabled(True)
            else:
                self.button_wynik.setEnabled(False)
        elif self.typ == 'sinus_2':
            if not (self.blad_amp.text() or self.blad_T.text() or self.blad_przes.text()
                    or self.blad_skl.text() or self.blad_amp_2.text() or self.blad_T_2.text()
                    or self.blad_przes_2.text() or self.blad_iter.text()):
                self.button_wynik.setEnabled(True)
            else:
                self.button_wynik.setEnabled(False)
        elif self.typ == 'exp':
            if not (self.blad_amp.text() or self.blad_st_czas.text()
                    or self.blad_skl.text() or self.blad_iter.text()):
                self.button_wynik.setEnabled(True)
            else:
                self.button_wynik.setEnabled(False)

    def edit_typ(self, typ):
        self.typ = typ
        match self.typ:
            case 'sinus':
                self.pi.setVisible(True)
                self.pi_2.setVisible(False)
                self.napis_skl.setVisible(True)
                self.pole_skl.setVisible(True)
                self.blad_skl.setVisible(True)
                self.napis_amp.setVisible(True)
                self.napis_amp.setText("Amplituda:")
                self.pole_amp.setVisible(True)
                self.blad_amp.setVisible(True)
                self.napis_T.setVisible(True)
                self.napis_T.setText("Okres:")
                self.pole_T.setVisible(True)
                self.blad_T.setVisible(True)
                self.napis_przes.setVisible(True)
                self.napis_przes.setText("Faza:")
                self.pole_przes.setVisible(True)
                self.blad_przes.setVisible(True)

                self.napis_amp_2.setVisible(False)
                self.pole_amp_2.setVisible(False)
                self.blad_amp_2.setVisible(False)
                self.napis_T_2.setVisible(False)
                self.pole_T_2.setVisible(False)
                self.blad_T_2.setVisible(False)
                self.napis_st_czas.setVisible(False)
                self.pole_st_czas.setVisible(False)
                self.blad_st_czas.setVisible(False)
                self.napis_przes_2.setVisible(False)
                self.pole_przes_2.setVisible(False)
                self.blad_przes_2.setVisible(False)

                self.blad_amp.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
                self.blad_T.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
                self.blad_przes.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

            case 'sinus_2':
                self.pi.setVisible(True)
                self.pi_2.setVisible(True)
                self.napis_skl.setVisible(True)
                self.pole_skl.setVisible(True)
                self.blad_skl.setVisible(True)
                self.napis_amp.setVisible(True)
                self.napis_amp.setText("Amplituda 1:")
                self.pole_amp.setVisible(True)
                self.blad_amp.setVisible(True)
                self.napis_T.setVisible(True)
                self.napis_T.setText("Okres 1:")
                self.pole_T.setVisible(True)
                self.blad_T.setVisible(True)
                self.napis_przes.setVisible(True)
                self.napis_przes.setText("Faza 1:")
                self.pole_przes.setVisible(True)
                self.blad_przes.setVisible(True)

                self.napis_amp_2.setVisible(True)
                self.pole_amp_2.setVisible(True)
                self.blad_amp_2.setVisible(True)
                self.napis_T_2.setVisible(True)
                self.pole_T_2.setVisible(True)
                self.blad_T_2.setVisible(True)
                self.napis_przes_2.setVisible(True)
                self.pole_przes_2.setVisible(True)
                self.blad_przes_2.setVisible(True)

                self.napis_st_czas.setVisible(False)
                self.pole_st_czas.setVisible(False)
                self.blad_st_czas.setVisible(False)

                self.blad_amp.setAlignment(Qt.AlignRight | Qt.AlignRight)
                self.blad_T.setAlignment(Qt.AlignRight | Qt.AlignRight)
                self.blad_przes.setAlignment(Qt.AlignRight | Qt.AlignRight)

            case 'exp':
                self.pi.setVisible(False)
                self.pi_2.setVisible(False)
                self.napis_skl.setVisible(True)
                self.pole_skl.setVisible(True)
                self.blad_skl.setVisible(True)
                self.napis_amp.setVisible(True)
                self.napis_amp.setText("Wzmocnienie:")
                self.pole_amp.setVisible(True)
                self.blad_amp.setVisible(True)
                self.napis_st_czas.setVisible(True)
                self.pole_st_czas.setVisible(True)
                self.blad_st_czas.setVisible(True)

                self.napis_T.setVisible(False)
                self.pole_T.setVisible(False)
                self.blad_T.setVisible(False)
                self.napis_przes.setVisible(False)
                self.pole_przes.setVisible(False)
                self.blad_przes.setVisible(False)
                self.napis_amp_2.setVisible(False)
                self.pole_amp_2.setVisible(False)
                self.blad_amp_2.setVisible(False)
                self.napis_T_2.setVisible(False)
                self.pole_T_2.setVisible(False)
                self.blad_T_2.setVisible(False)
                self.napis_przes_2.setVisible(False)
                self.pole_przes_2.setVisible(False)
                self.blad_przes_2.setVisible(False)

                self.blad_amp.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

        self.sprawdz()

    def plot_odp(self, u, y):
        self.u = u
        self.y = y

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.canvas.setVisible(True)
        self.widget_wykr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.figure.tight_layout(rect=(0.03, 0.03, 0.97, 0.98))
        self.ax.set_xlabel('Argument')
        self.ax.set_ylabel('Sygnał')
        self.ax.set_title('Wynik pomiaru odpowiedzi obiektu')
        self.ax.grid(True)
        self.ax.plot(self.u, self.y, 'o', color='#191970', markersize=3, label="Odpowiedź obiektu")
        self.ax.set_xlim(min(self.u), max(self.u))
        self.canvas.draw()


    def result(self):
        match self.typ:
            case 'sinus':
                amp_0 = float(self.pole_amp.text())
                T_0 = float(self.pole_T.text())
                przes_0 = float(self.pole_przes.text())
                skl_0 = float(self.pole_skl.text())
                iter = int(self.pole_iter.text())
                return iter, amp_0, T_0, przes_0, skl_0

            case 'sinus_2':
                amp1_0 = float(self.pole_amp.text())
                amp2_0 = float(self.pole_amp_2.text())
                T1_0 = float(self.pole_T.text())
                T2_0 = float(self.pole_T_2.text())
                przes1_0 = float(self.pole_przes.text())
                przes2_0 = float(self.pole_przes_2.text())
                skl_0 = float(self.pole_skl.text())
                iter = int(self.pole_iter.text())
                return iter, amp1_0, T1_0, przes1_0, amp2_0, T2_0, przes2_0, skl_0

            case 'exp':
                amp_0 = float(self.pole_amp.text())
                st_czas_0 = float(self.pole_st_czas.text())
                skl_0 = float(self.pole_skl.text())
                iter = int(self.pole_iter.text())
                return iter, amp_0, st_czas_0, skl_0


class WidokWynik(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.font_l = QFont()
        self.font_l.setPointSize(20)
        self.font_s = QFont()
        self.font_s.setPointSize(12)

        self.main_layout = QHBoxLayout()

        self.layout_title = QVBoxLayout()
        self.title = QLabel("WYNIKI")
        self.title.setStyleSheet(style)
        self.title.setFont(self.font_l)
        self.layout_title.addWidget(self.title)
        self.layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wybor_widget = QWidget()
        self.wybor_widget.setObjectName('wybor_widget')
        self.wybor_layout = QVBoxLayout(self.wybor_widget)
        self.wybor_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.wybor_widget.setLayout(self.wybor_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumSize(300, 500)
        self.scroll_area.setMaximumSize(300, 800)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.wybor_widget)
        self.scroll_area.setStyleSheet(style)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.boczny_widget = QWidget()
        self.boczny_layout = QVBoxLayout(self.boczny_widget)
        self.boczny_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.napis = QLabel('Symulacja')
        self.napis.setStyleSheet(style)
        self.napis.setFont(self.font_s)
        self.napis.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.napis_layout = QHBoxLayout()
        self.napis_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.napis_layout.addWidget(self.napis)
        self.scroll_area_layout = QHBoxLayout()
        self.scroll_area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_area_layout.addWidget(self.scroll_area)

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_return = QPushButton("Dodaj")
        self.button_return.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.button_return.setStyleSheet(style)
        self.button_layout.addWidget(self.button_return)

        self.boczny_layout.addLayout(self.napis_layout)
        self.boczny_layout.addLayout(self.scroll_area_layout)
        self.boczny_layout.addLayout(self.button_layout)

        self.boczny_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.wynik_widget = QStackedWidget()
        self.wynik_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.obiekty_wynik = []
        self.buttons = []

        self.main_layout.addWidget(self.boczny_widget)
        self.main_layout.addWidget(self.wynik_widget)

        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.layout_title)
        self.layout.addLayout(self.main_layout)

        self.setLayout(self.layout)

    def rysuj_wyniki(self, obiekt, param_sym, metoda):
        self.obiekty_wynik.append(WykresWidget(obiekt, param_sym, metoda))
        if obiekt.typ == 'Stacjonarny' or obiekt.typ in ['sinus', 'sinus_2', 'exp']:
            self.obiekty_wynik[-1].table()
        self.wynik_widget.addWidget(self.obiekty_wynik[-1])
        self.wynik_widget.setCurrentWidget(self.obiekty_wynik[-1])
        self.update(metoda)

    def update(self, met):
        if self.obiekty_wynik[-1].metoda_typ == 'GLS':
            self.buttons.append(QPushButton(f"{self.obiekty_wynik[-1].obiekt_typ}, {met.algorytm}"))
        else:
            self.buttons.append(
                QPushButton(f"{self.obiekty_wynik[-1].obiekt_typ}, {self.obiekty_wynik[-1].metoda_typ}"))
        self.buttons[-1].setStyleSheet(style)
        self.wybor_layout.addWidget(self.buttons[-1])

        self.buttons[-1].setCheckable(True)
        self.curr = self.buttons[-1]
        for but in self.buttons[:-1]:
            but.setChecked(False)
        self.buttons[-1].click()
        self.buttons[-1].clicked.connect(self.change_widok)

    def change_widok(self):
        if self.curr == self.sender():
            self.sender().setChecked(True)
        else:
            self.curr.setChecked(False)
        self.curr = self.sender()

        nr = 0
        for i in range(len(self.buttons)):
            if self.sender() is self.buttons[i]:
                nr = i

        self.wynik_widget.setCurrentWidget(self.obiekty_wynik[nr])


class WykresWidgetParametr(QWidget):
    def __init__(self, number, sublst, b_, b_wzorzec):
        super().__init__()
        self.number = number
        self.setObjectName(f'{number}')
        self.typ = sublst[0]
        match self.typ:
            case 'staly':
                self.napis = f'f(x) = {sublst[1]}'
            case 'liniowy':
                self.napis = f'f(x) = {sublst[1]} ∙ a + {sublst[2]}'
            case 'sinus':
                self.napis = f'f(x) = {sublst[1]} + {sublst[2]} ∙ sin(2 ∙ π ∙ x / {sublst[3]} + {sublst[4]} ∙ π)'

        self.b_ = b_
        self.b_wzorzec = b_wzorzec
        self.N = len(self.b_wzorzec)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.ax = self.figure.add_subplot(111)

        self.ax.plot(np.arange(0, self.N), self.b_, color='#191970', linewidth=1.2, label="Parametr obiektu")
        self.ax.plot(np.arange(0, self.N), self.b_wzorzec, 'o', color='red', markersize=4, label="Współczynnik modelu")

        self.ax.set_xlim(0, self.N-1)

        self.ax.set_xlabel('Numer pętli')
        self.ax.set_ylabel('Wartość')
        self.ax.set_title(f'Parametr $x^{self.number}$, zadany jako {self.napis}')
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)


class WykresWidget(QWidget):
    def __init__(self, obiekt, param_sym, metoda):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.wykresy = QStackedWidget()
        self.setObjectName('pole_wynikowe')
        self.setLayout(self.main_layout)
        self.font_ = QFont()
        self.font_.setPointSize(12)

        if obiekt.ret()[0] == "Nieliniowy":
            match obiekt.ret()[1]:
                case 'sinus':
                    self.obiekt_typ, self.typ_nielin, self.amp, self.T, self.przes, self.skl = obiekt.ret()
                case 'sinus_2':
                    self.obiekt_typ, self.typ_nielin, self.amp, self.T, self.przes, self.amp2, self.T2, self.przes2, self.skl = obiekt.ret()
                case 'exp':
                    self.obiekt_typ, self.typ_nielin, self.amp, self.st_czas, self.skl = obiekt.ret()
        elif obiekt.ret()[0] == "Dynamiczny":
            match obiekt.ret()[1]:
                case 'iner1':
                    self.obiekt_typ, self.typ_dynamiczny, self.G, self.wzm, self.st_czas = obiekt.ret()
                case 'iner2':
                    self.obiekt_typ, self.typ_dynamiczny, self.G, self.wzm, self.st_czas_1, self.st_czas_2s = obiekt.ret()
                case 'osc':
                    self.obiekt_typ, self.typ_dynamiczny, self.G, self.wzm, self.tlum, self.okr_dr = obiekt.ret()
        else:
            self.obiekt_typ, self.stopien, self.b_i = obiekt.ret()

        if self.obiekt_typ == "Stacjonarny":
            self.stopien_m, self.N, self.zakr_min, self.zakr_max, self.od_std = param_sym.ret()
        elif self.obiekt_typ == "Nieliniowy":
            self.N, self.zakr_min, self.zakr_max, self.od_std = param_sym.ret()
        elif self.obiekt_typ == "Dynamiczny":
            self.N, self.zakr_max, self.od_std_w, self.od_std = param_sym.ret()
            self.zakr_min = 0
        else:
            self.N, self.zakr_min, self.zakr_max, self.wymuszenie_typ, self.od_std = param_sym.ret()

        self.metoda_typ, self.u, self.y, self.y_m, self.b_m, self.b, self.b_wzorzec, self.cov = metoda.calc()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.wykresy.addWidget(self.canvas)
        self.main_layout.addWidget(self.wykresy)
        self.wykresy.setCurrentWidget(self.canvas)

        self.ax = self.figure.add_subplot(111)

        self.length = len(self.u)

        self.var_zero()

        self.ax.set_xlim(min(self.u), max(self.u))
        self.ax.set_ylim(min([min(self.y), min(self.y_m)]), max([max(self.y), max(self.y_m)]))

        if self.obiekt_typ == "Dynamiczny":
            self.points, = self.ax.plot([], [], linewidth=1.2, color='#191970', label="Odpowiedź impulsowa obiektu")
            self.line, = self.ax.plot([], [], linewidth=1.2, color='red', label="Odpowiedź impulsowa modelu")
            self.ax.set_xlabel('Czas')
            self.ax.set_ylabel('Sygnał wyjściowy')
        else:
            self.points, = self.ax.plot([], [], 'o', markersize=4, color='#191970', label="Odpowiedź obiektu")
            self.line, = self.ax.plot([], [], linewidth=1.2, color='red', label="Odpowiedź modelu")
            self.ax.set_xlabel('Sygnał wejściowy')
            self.ax.set_ylabel('Odpowiedź')

        if self.metoda_typ == 'GLS':
            self.ax.set_title(
                f'Obiekt {self.obiekt_typ.lower()}, algorytm {metoda.algorytm}, zakłócenia {metoda.korel}')
        else:
            self.ax.set_title(
                f'Obiekt {self.obiekt_typ.lower()}, algorytm {self.metoda_typ}, zakłócenia nieskorelowane')
        self.ax.grid(True)
        self.ax.legend()

        self.speed = 1000 / self.length
        self.wys_elem = int(np.ceil(self.length / 1000)) ** 2

        if 700 < self.length < 1300:
            self.wys_elem = 2

        if self.obiekt_typ == "Dynamiczny":
            self.u_aprox = np.linspace(self.zakr_min, 0.1 * self.zakr_max, int(0.1 * self.N))
        else:
            self.u_aprox = np.linspace(self.zakr_min, self.zakr_max, 1000)

        self.fr = int(self.length // self.wys_elem)
        self.anim = FuncAnimation(self.figure, self.update_plot, blit=True, frames=self.fr,
                                  interval=self.speed, repeat=False)

        if self.b_wzorzec is None and self.b_m is not None:
            self.table_layout = QHBoxLayout()
            self.show_button_layout = QHBoxLayout()
            self.show_button = QPushButton("▼ Ukryj tabelę z wynikami ▼")
            self.show_button.setStyleSheet(style)
            self.show_button.setObjectName("tabela_but")
            self.show_button.clicked.connect(self.show)
            self.show_button_layout.addWidget(self.show_button)
            self.show_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if not self.metoda_typ == 'NLS':
                self.table_widget = QTableWidget((max(self.stopien, self.stopien_m)+1), 4)
            else:
                match self.typ_nielin:
                    case 'sinus':
                        self.table_widget = QTableWidget(4, 4)
                    case 'sinus_2':
                        self.table_widget = QTableWidget(7, 4)
                    case 'exp':
                        self.table_widget = QTableWidget(3, 4)

            self.table_widget.setStyleSheet(style)
            self.table_widget.setObjectName('tabela')
            self.table_layout.addWidget(self.table_widget)
            self.table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table_widget.setHorizontalHeaderLabels(['Parametry obiektu', 'Współczynniki modelu',
                                                         'Błąd bezwzględny', 'Błąd względny'])

            if self.obiekt_typ == "Stacjonarny":
                self.table_widget.setVerticalHeaderLabels(
                    [f'{i + 1}' for i in range(max(self.stopien, self.stopien_m)+1)])
                self.table_widget.setMinimumSize(619, (max(self.stopien, self.stopien_m) + 1) * 35 + 28)
                self.table_widget.setMaximumSize(619, (max(self.stopien, self.stopien_m) + 1) * 35 + 28)

            elif self.obiekt_typ == "Nieliniowy":
                if self.typ_nielin == 'sinus':
                    self.table_widget.setVerticalHeaderLabels(['Amplituda', 'Okres', 'Faza', 'Składowa stała'])
                    self.table_widget.setMinimumSize(697, 168)
                    self.table_widget.setMaximumSize(697, 168)
                elif self.typ_nielin == 'sinus_2':
                    self.table_widget.setVerticalHeaderLabels(['Amplituda 1', 'Okres 1', 'Faza 1', 'Amplituda 2', 'Okres 1', 'Faza 1', 'Składowa stała'])
                    self.table_widget.setMinimumSize(697, 273)
                    self.table_widget.setMaximumSize(697, 273)
                elif self.typ_nielin == 'exp':
                    self.table_widget.setVerticalHeaderLabels(['Amplituda', 'Stała czasowa', 'Składowa stała'])
                    self.table_widget.setMinimumSize(697, 133)
                    self.table_widget.setMaximumSize(697, 133)
            self.table_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

            self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addLayout(self.show_button_layout)

            self.main_layout.addLayout(self.table_layout)

            if self.cov is not None:
                self.macierz_layout = QVBoxLayout()
                self.macierz_cov = QTableWidget(self.stopien_m + 1, self.stopien_m + 1)
                self.macierz_cov.setObjectName('tabela')
                self.macierz_cov.setStyleSheet(style)
                self.macierz_napis = QLabel('Macierz kowariancji estymatora')
                self.macierz_napis.setStyleSheet(style)
                self.macierz_napis.setFont(self.font_)
                self.macierz_napis.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                self.macierz_cov.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                self.macierz_layout.addWidget(self.macierz_napis, alignment=Qt.AlignCenter)
                self.macierz_layout.addWidget(self.macierz_cov, alignment=Qt.AlignCenter)
                self.macierz_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_layout.addLayout(self.macierz_layout)
                self.macierz()

        elif self.b_m is not None:
            self.layout_wybor_parametru = QHBoxLayout()

            self.wykresy_list = [self.canvas]
            self.buttons = []

            for i, sublst in enumerate(self.b):
                self.wykresy_list.append(WykresWidgetParametr(len(self.b) - i - 1, sublst, self.b_wzorzec[:, i], self.b_m[i, :]))
                self.wykresy.addWidget(self.wykresy_list[-1])
                self.buttons.append(QPushButton(f'Parametr x^{len(self.b) - i - 1}'))
                self.buttons[-1].setCheckable(True)
                self.buttons[-1].setStyleSheet(style)
                self.buttons[-1].setObjectName(f'{i + 1}')
                self.layout_wybor_parametru.addWidget(self.buttons[-1])
                self.buttons[-1].clicked.connect(self.change_wykres)

            self.curr = self.buttons[0]
            self.buttons[0].setChecked(True)
            self.buttons[0].click()

            self.layout_wybor_parametru.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.main_layout.addLayout(self.layout_wybor_parametru)

    def update_plot(self, frame):
        for i in range(self.wys_elem):
            self.var_u[self.wys_elem*frame+i] = self.u[self.wys_elem*frame+i]
            self.var_y[self.wys_elem*frame+i] = self.y[self.wys_elem*frame+i]

        self.points.set_data(self.var_u, self.var_y)

        if frame == self.fr - 1:
            self.var_zero()
            self.animation_aprox()

        return self.points, self.line

    def animation_aprox(self):
        if self.obiekt_typ == "Dynamiczny":
            frames = int(0.1 * self.N)
        else:
            frames = 500
        self.anim_aprox = FuncAnimation(self.figure, self.update_plot_aprox, blit=True, frames=frames,
                                  interval=1, repeat=False)

    def update_plot_aprox(self, frame):
        m = 1 if self.obiekt_typ == "Dynamiczny" else 2
        for i in range(m):
            self.var_aprox_u[m * frame + i] = self.u_aprox[m * frame + i]
            self.var_aprox_y[m * frame + i] = self.y_m[m * frame + i]

        self.line.set_data(self.var_aprox_u, self.var_aprox_y)

        if frame == 999:
            self.var_zero()

        return self.points, self.line

    def var_zero(self):
        self.var_u = np.full((self.length,), None)
        self.var_y = np.full((self.length,), None)
        self.var_aprox_u = np.full((1000,), None)
        self.var_aprox_y = np.full((1000,), None)

    def table(self):
        leng = 0

        if self.metoda_typ == 'NLS':
            match self.typ_nielin:
                case 'sinus':
                    leng = 4
                case 'sinus_2':
                    leng = 7
                case 'exp':
                    leng = 3

        for row in range((max(self.stopien, self.stopien_m)+1) if not self.metoda_typ == 'NLS' else leng):
            self.table_widget.setRowHeight(row, 35)
            item = QTableWidgetItem(f"{self.b[row]:.2f}")
            self.table_widget.setItem(row, 0, item)
            item = QTableWidgetItem(f"{self.b_m[row]:.2f}")
            self.table_widget.setItem(row, 1, item)

            if self.metoda_typ == 'NLS':
                blad_bezwzgl = abs(self.b[row] - self.b_m[row])
                item = QTableWidgetItem(
                    f"{blad_bezwzgl:.2f}" if 100000 > blad_bezwzgl >= 0.01 else f"{blad_bezwzgl:.2e}")
                self.table_widget.setItem(row, 2, item)
                if self.b[row]:
                    blad_wzgl = 100 * abs(self.b[row] - self.b_m[row]) / self.b[row]
                    item = QTableWidgetItem(f"{blad_wzgl:.2f}%" if 100000 > blad_wzgl >= 0.01 else f"{blad_wzgl:.2e}%")
                    self.table_widget.setItem(row, 3, item)
                else:
                    item = QTableWidgetItem("-")
                    self.table_widget.setItem(row, 3, item)

            else:
                blad_bezwzgl = abs(self.b[row] - self.b_m[row])
                item = QTableWidgetItem(
                    f"{blad_bezwzgl:.2f}" if 100000 > blad_bezwzgl >= 0.01 else f"{blad_bezwzgl:.2e}")
                self.table_widget.setItem(row, 2, item)
                if self.b[row]:
                    blad_wzgl = 100 * abs(self.b[row] - self.b_m[row]) / self.b[row]
                    item = QTableWidgetItem(f"{blad_wzgl:.2f}%" if 100000 > blad_wzgl >= 0.01 else f"{blad_wzgl:.2e}%")
                    self.table_widget.setItem(row, 3, item)
                else:
                    item = QTableWidgetItem("-")
                    self.table_widget.setItem(row, 3, item)

        for col in range(4):
            self.table_widget.setColumnWidth(col, 150)

    def macierz(self):
        self.macierz_cov.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.macierz_cov.verticalHeader().setVisible(False)
        self.macierz_cov.horizontalHeader().setVisible(False)
        self.macierz_cov.setVisible(True)
        for col in range(self.stopien_m + 1):
            for row in range(self.stopien_m + 1):
                self.macierz_cov.setRowHeight(row, 35)
                item = QTableWidgetItem(f"{self.cov[row, col]:.2f}" if 1000 > self.cov[row, col] >= 0.01 else f"{self.cov[row, col]:.2e}")
                self.macierz_cov.setItem(row, col, item)
            self.macierz_cov.setColumnWidth(col, 70)

        self.macierz_cov.setMinimumSize((self.stopien_m + 1) * 70 + 4, (self.stopien_m + 1) * 35 + 4)
        self.macierz_cov.setMaximumSize((self.stopien_m + 1) * 70 + 4, (self.stopien_m + 1) * 35 + 4)
    def show(self):
        current_visibility = self.table_widget.isVisible()
        self.table_widget.setVisible(not current_visibility)
        if self.obiekt_typ == 'Stacjonarny':
            self.macierz_cov.setVisible(not current_visibility)
            self.macierz_napis.setVisible(not current_visibility)
        if current_visibility:
            self.show_button.setText('▲ Pokaż tabelę z wynikami ▲')
        else:
            self.show_button.setText('▼ Ukryj tabelę z wynikami ▼')

    def change_wykres(self):
        if self.curr == self.sender():
            self.sender().setChecked(True)
        else:
            self.curr.setChecked(False)
        self.curr = self.sender()
        but = int(self.sender().objectName())
        self.wykresy.setCurrentWidget(self.wykresy_list[but])


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Oprogramowanie do symulacji algorytmów")
        self.setWindowIcon(QIcon(path.join(basedir, 'logo.ico')))
        self.setGeometry(50, 50, 800, 600)
        self.setMinimumSize(1350, 700)

        self.central_widget = QStackedWidget()

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(248, 248, 255))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.setCentralWidget(self.central_widget)
        self.start = StartWidget()
        self.menu = MainMenuWidget()
        self.stacjo = WidokStacjonarny()
        self.niestacjo = WidokNiestacjonarny()
        self.nielin = WidokNieliniowy()
        self.dynamiczny = WidokDynamiczny()
        self.param_sym = WidokParametrySymulacji()
        self.param_sym_niestacjo = WidokParametrySymulacjiNiestacjo()
        self.param_sym_nielin = WidokParametrySymulacjiNielin()
        self.param_sym_dynamiczny = WidokParametrySymulacjiDynamiczny()
        self.metoda = WidokMetoda()
        self.metoda_niestacjo = WidokMetodaNiestacjo()
        self.metoda_nielin = WidokMetodaNielin()
        self.metoda_dynamiczny = WidokMetodaDynamiczny()
        self.RLS = WidokRLS()
        self.RLS_zap = WidokRLSZap()
        self.GLS = WidokGLS()
        self.NLS = WidokNLS()
        self.wynik = WidokWynik()

        self.central_widget.addWidget(self.start)
        self.central_widget.addWidget(self.menu)
        self.central_widget.addWidget(self.stacjo)
        self.central_widget.addWidget(self.niestacjo)
        self.central_widget.addWidget(self.nielin)
        self.central_widget.addWidget(self.dynamiczny)
        self.central_widget.addWidget(self.param_sym)
        self.central_widget.addWidget(self.param_sym_niestacjo)
        self.central_widget.addWidget(self.param_sym_nielin)
        self.central_widget.addWidget(self.param_sym_dynamiczny)
        self.central_widget.addWidget(self.metoda)
        self.central_widget.addWidget(self.metoda_niestacjo)
        self.central_widget.addWidget(self.metoda_nielin)
        self.central_widget.addWidget(self.metoda_dynamiczny)
        self.central_widget.addWidget(self.RLS)
        self.central_widget.addWidget(self.RLS_zap)
        self.central_widget.addWidget(self.GLS)
        self.central_widget.addWidget(self.NLS)
        self.central_widget.addWidget(self.wynik)

        self.animations_in = []
        self.animations_out = []

        for index in range(self.central_widget.count() - 1):
            widget = self.central_widget.widget(index)
            widget.setStyleSheet(style)
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)
            anim_in = QPropertyAnimation(effect, b"opacity")
            anim_in.setStartValue(0)
            anim_in.setEndValue(1)
            anim_in.setDuration(750)
            anim_in.setEasingCurve(QEasingCurve.InOutCubic)
            self.animations_in.append(anim_in)
            if index in [10, 13, 14, 15, 16, 17]:
                anim_out = QPropertyAnimation(effect, b"opacity")
                anim_out.setStartValue(1)
                anim_out.setEndValue(0)
                anim_out.setDuration(750)
                anim_out.setEasingCurve(QEasingCurve.InOutCubic)
                self.animations_out.append(anim_out)

        self.time = QTimer(self)
        self.time.setInterval(750)
        self.time.timeout.connect(self.open_wynik)

        self.open_start()

        self.start.start.clicked.connect(self.open_menu)

        self.menu.button_stacjo.clicked.connect(self.open_stacjo)
        self.menu.button_niestacjo.clicked.connect(self.open_niestacjo)
        self.menu.button_nielin.clicked.connect(self.open_nielin)
        self.menu.button_dynamiczny.clicked.connect(self.open_dynamiczny)

        self.stacjo.button_return.clicked.connect(self.open_menu)
        self.stacjo.button_param_sym.clicked.connect(self.open_param_sym)

        self.param_sym.button_metoda.clicked.connect(self.open_metoda)
        self.param_sym.button_return.clicked.connect(self.open_stacjo)

        self.niestacjo.button_return.clicked.connect(self.open_menu)
        self.niestacjo.button_param_sym.clicked.connect(self.open_param_sym_niestacjo)

        self.param_sym_niestacjo.button_metoda.clicked.connect(self.open_metoda_niestacjo)
        self.param_sym_niestacjo.button_return.clicked.connect(self.open_niestacjo)

        self.nielin.button_return.clicked.connect(self.open_menu)
        self.nielin.button_param_sym.clicked.connect(self.open_param_sym_nielin)

        self.param_sym_nielin.button_metoda.clicked.connect(self.open_metoda_nielin)
        self.param_sym_nielin.button_return.clicked.connect(self.open_nielin)

        self.dynamiczny.button_return.clicked.connect(self.open_menu)
        self.dynamiczny.button_param_sym.clicked.connect(self.open_param_sym_dynamiczny)

        self.param_sym_dynamiczny.button_metoda.clicked.connect(self.open_metoda_dynamiczny)
        self.param_sym_dynamiczny.button_return.clicked.connect(self.open_dynamiczny)

        self.metoda.button_LS.clicked.connect(self.open_wynik_LS)
        self.metoda.button_RLS.clicked.connect(self.open_RLS)
        self.metoda.button_GLS.clicked.connect(self.open_GLS)
        self.metoda.button_return.clicked.connect(self.open_param_sym)

        self.metoda_niestacjo.button_RLS_zap.clicked.connect(self.open_RLS_zap)
        self.metoda_niestacjo.button_return.clicked.connect(self.open_param_sym_niestacjo)

        self.metoda_nielin.button_NLS.clicked.connect(self.open_NLS)
        self.metoda_nielin.button_return.clicked.connect(self.open_param_sym_nielin)

        self.metoda_dynamiczny.button_korel.clicked.connect(self.open_wynik_korel)
        self.metoda_dynamiczny.button_return.clicked.connect(self.open_param_sym_dynamiczny)

        self.RLS.button_return.clicked.connect(self.open_metoda)
        self.RLS.button_wynik.clicked.connect(self.open_wynik_RLS)

        self.RLS_zap.button_return.clicked.connect(self.open_metoda_niestacjo)
        self.RLS_zap.button_wynik.clicked.connect(self.open_wynik_RLS_zap)

        self.GLS.button_return.clicked.connect(self.open_metoda)
        self.GLS.button_wynik.clicked.connect(self.open_wynik_GLS)

        self.NLS.button_return.clicked.connect(self.open_metoda_nielin)
        self.NLS.button_wynik.clicked.connect(self.open_wynik_NLS)

        self.wynik.button_return.clicked.connect(self.open_menu)

    def open_start(self):
        self.central_widget.setCurrentWidget(self.start)
        self.animations_in[0].start()

    def open_menu(self):
        self.central_widget.setCurrentWidget(self.menu)
        self.animations_in[1].start()


    def open_stacjo(self):
        self.central_widget.setCurrentWidget(self.stacjo)
        self.animations_in[2].start()

    def open_niestacjo(self):
        self.central_widget.setCurrentWidget(self.niestacjo)
        self.animations_in[3].start()

    def open_nielin(self):
        self.central_widget.setCurrentWidget(self.nielin)
        self.animations_in[4].start()

    def open_dynamiczny(self):
        self.central_widget.setCurrentWidget(self.dynamiczny)
        self.animations_in[5].start()

    def open_param_sym(self):
        self.central_widget.setCurrentWidget(self.param_sym)
        self.animations_in[6].start()
        if isinstance(self.sender().parent(), WidokStacjonarny):
            typ, rzad, parametry = self.stacjo.result()
            self.param_sym.edit(rzad)
            self.obkt = ust.ObiektLiniowy(typ, rzad, parametry)

    def open_param_sym_niestacjo(self):
        self.central_widget.setCurrentWidget(self.param_sym_niestacjo)
        self.animations_in[7].start()
        if isinstance(self.sender().parent(), WidokNiestacjonarny):
            typ, rzad, parametry = self.niestacjo.result()
            self.param_sym_niestacjo.edit(rzad)
            self.obkt = ust.ObiektLiniowy(typ, rzad, parametry)

    def open_param_sym_nielin(self):
        self.central_widget.setCurrentWidget(self.param_sym_nielin)
        self.animations_in[8].start()
        if isinstance(self.sender().parent(), WidokNieliniowy):
            typ = self.nielin.result()[0]
            self.NLS.edit_typ(typ)
            match typ:
                case 'sinus':
                    self.param_sym_nielin.edit(4)
                    amp, T, przes, skl = self.nielin.result()[1:]
                    self.obkt = ust.ObiektNieliniowy(typ, amp, T, przes, skl)
                case 'sinus_2':
                    self.param_sym_nielin.edit(7)
                    amp, T, przes, amp_2, T_2, przes_2, skl = self.nielin.result()[1:]
                    self.obkt = ust.ObiektNieliniowy(typ, amp, T, przes, amp_2, T_2, przes_2, skl)
                case 'exp':
                    self.param_sym_nielin.edit(3)
                    amp, st_czas, skl = self.nielin.result()[1:]
                    self.obkt = ust.ObiektNieliniowy(typ, amp, st_czas, skl)

    def open_param_sym_dynamiczny(self):
        self.central_widget.setCurrentWidget(self.param_sym_dynamiczny)
        self.animations_in[9].start()
        if isinstance(self.sender().parent(), WidokDynamiczny):
            typ = self.dynamiczny.result()[0]
            match typ:
                case 'iner1':
                    wzm, st_czas = self.dynamiczny.result()[1:]
                    self.obkt = ust.ObiektDynamiczny(typ, wzm, st_czas)
                case 'iner2':
                    wzm, st_czas, st_czas_2 = self.dynamiczny.result()[1:]
                    self.obkt = ust.ObiektDynamiczny(typ, wzm, st_czas, st_czas_2)
                case 'osc':
                    wzm, tlum, okr_dr = self.dynamiczny.result()[1:]
                    self.obkt = ust.ObiektDynamiczny(typ, wzm, tlum, okr_dr)

    def open_metoda(self):
        self.central_widget.setCurrentWidget(self.metoda)
        self.animations_in[10].start()
        rzad_m, N, zakr_min, zakr_max, zakl = self.param_sym.result()
        self.parametry = ust.Parametry(self.obkt, rzad_m, N, zakr_min, zakr_max, zakl)

    def open_metoda_niestacjo(self):
        self.central_widget.setCurrentWidget(self.metoda_niestacjo)
        self.animations_in[11].start()
        N, range_min, range_max, wymuszenie_typ, zakl = self.param_sym_niestacjo.result()
        self.parametry_niestacjo = ust.ParametryNiestacjo(self.obkt, N, range_min, range_max, wymuszenie_typ, zakl)

    def open_metoda_nielin(self):
        self.central_widget.setCurrentWidget(self.metoda_nielin)
        self.animations_in[12].start()
        N, range_min, range_max, zakl = self.param_sym_nielin.result()
        self.parametry_nielin = ust.ParametryNieliniowy(self.obkt, N, range_min, range_max, zakl)
        self.NLS.canvas.setVisible(False)

    def open_metoda_dynamiczny(self):
        self.central_widget.setCurrentWidget(self.metoda_dynamiczny)
        self.animations_in[13].start()
        N, range_max, zakl_w, zakl = self.param_sym_dynamiczny.result()
        self.parametry = ust.ParametryDynamiczny(self.obkt, N, range_max, zakl_w, zakl)

    def open_wynik_LS(self):
        try:
            self.ob_LS = ust.LS(self.obkt, self.parametry)
            self.animations_out[0].start()
            self.wynik.rysuj_wyniki(self.obkt, self.parametry, self.ob_LS)
            self.time.start()
        except Exception as e:
            self.blad = BladWidget(self.metoda, e)
            self.central_widget.addWidget(self.blad)
            self.central_widget.setCurrentWidget(self.blad)

    def open_RLS(self):
        self.RLS.edit(self.param_sym.result()[0], self.param_sym.result()[1])
        self.central_widget.setCurrentWidget(self.RLS)
        self.animations_in[14].start()

    def open_wynik_RLS(self):
        alfa, b0, N_pocz = self.RLS.result()
        try:
            self.ob_RLS = ust.RLS(self.obkt, self.parametry, alfa, b0, N_pocz)
            self.animations_out[2].start()
            self.wynik.rysuj_wyniki(self.obkt, self.parametry, self.ob_RLS)
            self.time.start()
        except Exception as e:
            self.blad = BladWidget(self.RLS, e)
            self.central_widget.addWidget(self.blad)
            self.central_widget.setCurrentWidget(self.blad)

    def open_RLS_zap(self):
        self.RLS_zap.edit_b0(self.niestacjo.result()[1])
        self.central_widget.setCurrentWidget(self.RLS_zap)
        self.animations_in[15].start()

    def open_wynik_RLS_zap(self):
        alfa, b0, wsp_zap = self.RLS_zap.result()
        try:
            self.ob_RLS_zap = ust.RLSZapominanie(self.obkt, self.parametry_niestacjo, alfa, b0, wsp_zap)
            self.animations_out[3].start()
            self.wynik.rysuj_wyniki(self.obkt, self.parametry_niestacjo, self.ob_RLS_zap)
            self.time.start()
        except Exception as e:
            self.blad = BladWidget(self.RLS_zap, e)
            self.central_widget.addWidget(self.blad)
            self.central_widget.setCurrentWidget(self.blad)

    def open_GLS(self):
        self.GLS.edit_N(self.param_sym.result()[1])
        self.central_widget.setCurrentWidget(self.GLS)
        self.animations_in[16].start()

    def open_wynik_GLS(self):
        algorytm, przek_wart = self.GLS.result()
        try:
            self.ob_GLS = ust.GLS(self.obkt, self.parametry, przek_wart, algorytm)
            if self.ob_GLS.check():
                self.animations_out[4].start()
                self.wynik.rysuj_wyniki(self.obkt, self.parametry, self.ob_GLS)
                self.time.start()
            else:
                self.GLS.blad_macierz.setText('Macierz nie jest dodatnio określona - wymagana korekta macierzy')
                self.GLS.button_macierz.setVisible(True)
        except Exception as e:
            self.blad = BladWidget(self.GLS, e)
            self.central_widget.addWidget(self.blad)
            self.central_widget.setCurrentWidget(self.blad)

    def open_NLS(self):
        def plot():
            self.NLS.plot_odp(u, y)
        self.parametry_nielin.calc()
        u, y = self.parametry_nielin.calc_ret()
        self.central_widget.setCurrentWidget(self.NLS)
        self.NLS.figure.clear()
        self.animations_in[17].start()
        self.animations_in[17].finished.connect(plot)

    def open_wynik_NLS(self):
        self.NLS.canvas.setVisible(False)
        try:
            match self.obkt.ret()[1]:
                case 'sinus':
                    iter, amp_0, T_0, przes_0, skl_0 = self.NLS.result()
                    self.ob_NLS = ust.NLS(self.obkt, self.parametry_nielin, iter, amp_0, T_0, przes_0, skl_0)
                case 'sinus_2':
                    iter, amp_0, T_0, przes_0, amp2_0, T2_0, przes2_0, skl_0 = self.NLS.result()
                    self.ob_NLS = ust.NLS(self.obkt, self.parametry_nielin, iter, amp_0, T_0, przes_0, amp2_0, T2_0, przes2_0, skl_0)
                case 'exp':
                    iter, amp_0, st_czas_0, skl_0 = self.NLS.result()
                    self.ob_NLS = ust.NLS(self.obkt, self.parametry_nielin, iter, amp_0, st_czas_0, skl_0)
            self.animations_out[5].start()
            self.wynik.rysuj_wyniki(self.obkt, self.parametry_nielin, self.ob_NLS)
            self.time.start()
        except Exception as e:
            self.NLS.canvas.setVisible(True)
            self.blad = BladWidget(self.NLS, e)
            self.central_widget.addWidget(self.blad)
            self.central_widget.setCurrentWidget(self.blad)

    def open_wynik_korel(self):
        try:
            self.ob_korel = ust.Korel(self.obkt, self.parametry)
            self.animations_out[1].start()
            self.wynik.rysuj_wyniki(self.obkt, self.parametry, self.ob_korel)
            self.time.start()
        except Exception as e:
            self.blad = BladWidget(self.metoda_dynamiczny, e)
            self.central_widget.addWidget(self.blad)
            self.central_widget.setCurrentWidget(self.blad)

    def open_wynik(self):
        self.central_widget.setCurrentWidget(self.wynik)
        self.time.stop()


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(argv)
    else:
        app = QApplication.instance()
    window = App()
    window.show()
    exit(app.exec())
