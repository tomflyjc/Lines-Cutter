# -*- coding: utf-8 -*-

import os.path
from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,320,600).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")
         
        self.label_2 = QtGui.QLabel(Dialog)
        self.labelImage = QtGui.QLabel(Dialog)
        myPath = os.path.dirname(__file__)+"/icons/onema.png";
        myDefPath = myPath.replace("\\","/");
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        
        font = QtGui.QFont()
        font.setPointSize(15) 
        font.setWeight(50) 
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,1,1,2)
        self.gridlayout.addWidget(self.labelImage,1,5,1,2)
         
        self.textEdit = QtGui.QTextEdit(Dialog)

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.width = 320
        self.textEdit.height = 360
        self.textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
       
        self.gridlayout.addWidget(self.textEdit,2,1,5,2) 

        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,4,2,1,1) 

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,3,1,1,1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "decoupeur", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "decoupeur 0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-weight:600;\">"
        "Plus Proche Point Projeté :</span>" "  Ce plugin est conçu pour obtenir à partir d'une sélection de points, leurs plus proches projections sur une couche de lignes.                                                              "+
        " <br><b>Attention:</b><br> <b>il fonctionne exclusivement à partir d'objets points et lignes et non multi-points et multi-lignes !</b>                                              " +
        " Pour qu'il fonctionne, il faut effectuer une sélection d'objets dans chaques couches.                                                                                             "+
        " Il produit une couche de points projetés reprenant la table attributaire de la couche de départ mais augmentée de plusieurs nouveaux champs:                                                                                          "+
        " - une colonne distance qui correspond à la distance du point initial à la ligne la plus proche,                                                         " +
        " - deux champs de coordonnées qui sont les coordonnées du point de départ avant projection,                                                                  " +                                                           
        " - deux champs de coordonnées qui sont les coordonnées du point projeté sur cette ligne,                                                                     " +
        " - deux champs de coordonnées qui sont les coordonnées du point median entre point de départ et point projeté sur cette ligne.                                        " +
        " Ce plugin s'inspire librement de l'article: http://gis.stackexchange.com/questions/396/nearest-neighbor-between-a-point-layer-and-a-line-layer                                                              "+
        " Il utilise plus exactement la dernière solution proposée à cette question sur ce forum  et qui utilise le module shapely                                                        "+
        "                                                                                                                                                                           "+

        " Cette extension ne fait pas partie du moteur de Qgis et tout probleme ne peut être adressé aux développeurs QGIS, mais à l'auteur: </p></td></tr></table>"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        "<p style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        #"<font color='#0000FF'><b><u> Jean-Christohe Baudin</u></b></font><br><br>"
        "<br><b>jeanchristophebaudin@ymail.com</b><br>"
        "<br><br><i>code 0.1 (16 juin 2017).</i></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

