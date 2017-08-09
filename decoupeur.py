# -*- coding: iso-8859-1 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import os
import doAbout
import doListLayers2
from qgis.gui  import QgsMapCanvas

# chargement des fichiers d'interface graphique
import doListLayers2
import doAbout
import fonctionsF

class MainPlugin(object):
  def __init__(self, iface):
    self.name = "decoupeur"
    #référence à l'objet interface QGIS
    self.iface = iface

  def initGui(self):
    self.menu=QMenu("decoupeur")

    #déclaration des actions élémentaires
    menuIcon = getThemeIcon("decoupeur.png")
    self.commande2 = QAction(QIcon(menuIcon),"decoupeur ...",self.iface.mainWindow())
    self.commande2.setText("decoupeur ...")

    menuIcon = getThemeIcon("about.png")
    self.about = QAction(QIcon(menuIcon), "A propos ...", self.iface.mainWindow())
    self.about.setText("A propos ...")

    
    #Construction du menu
    self.menu.addAction(self.commande2)
    self.menu.addSeparator()
    self.menu.addAction(self.about)

    #Exemple de QFontComboBox
    FontComboBox = QtGui.QFontComboBox()
    FontComboBox.setGeometry(QtCore.QRect(10, 10, 100, 20))
    FontComboBox.setObjectName("FontComboBox") 

    #Construction de la barre d'outils
    self.toolBarName = "Ma Barre"
    toolbar = self.iface.addToolBar(self.toolBarName)
    self.toolbar = toolbar
    self.toolbar.addAction(self.commande2)
    
    #Connection de la commande à l'action
    
    QObject.connect(self.commande2,SIGNAL("triggered()"),self.LoadDlgBoxQt2)
    QObject.connect(self.about,SIGNAL("triggered()"),self.doInfo)

    menuBar = self.iface.mainWindow().menuBar()
    menuBar.addMenu(self.menu)

  #Méthode au déchargement de l'extension
  def unload(self): pass

   
  #Exemple d'appel d'une boîte de dialogue (ici : exemple d'objets Qt) 
  def LoadDlgBoxQt2(self):
      d = doListLayers2.Dialog()
      #d.show()
      d.exec_()

  def doInfo(self):
      d = doAbout.Dialog()
      d.exec_()


#Fonction de reconstruction du chemin absolu vers la ressource image
def getThemeIcon(theName):
    myPath = CorrigePath(os.path.dirname(__file__));
    myDefPathIcons = myPath + "/icons/"
    myDefPath = myPath.replace("\\","/")+ theName;
    myDefPathIcons = myDefPathIcons.replace("\\","/")+ theName;
    myCurThemePath = QgsApplication.activeThemePath() + "/plugins/" + theName;
    myDefThemePath = QgsApplication.defaultThemePath() + "/plugins/" + theName;
    #Attention, ci-dessous, le chemin est à persoonaliser :
    #remplacer "extension" par le nom du répertoire de l'extension.
    myQrcPath = "python/plugins/extension/" + theName;
    if QFile.exists(myDefPath): return myDefPath
    elif QFile.exists(myDefPathIcons): return myDefPathIcons  
    elif QFile.exists(myCurThemePath): return myCurThemePath
    elif QFile.exists(myDefThemePath): return myDefThemePath
    elif QFile.exists(myQrcPath): return myQrcPath
    elif QFile.exists(theName): return theName
    else: return ""

#Fonction de correction des chemins
#(ajout de slash en fin de chaîne)
def CorrigePath(nPath):
    nPath = str(nPath)
    a = len(nPath)
    subC = "/"
    b = nPath.rfind(subC, 0, a)
    if a != b : return (nPath + "/")
    else: return nPath  
