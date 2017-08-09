# -*- coding: iso-8859-1 -*-
#nécessaire pour les connections signals / slots
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os.path
from PyQt4 import QtCore, QtGui

# import de QGIS
from qgis import *
from qgis.core import *
from qgis.gui import *
from qgis.gui import QgsMapCanvas
from qgis.utils import iface
import shapely
from shapely.geometry import Point, LineString, Polygon,MultiPolygon
from shapely.wkb import loads
from shapely.wkt import  dumps
from shapely.ops import cascaded_union
import processing

import os
import fonctionsF
import doAbout

class Ui_Dialog(object):
    def __init__(self, iface):
        self.iface = iface
    
    def setupUi(self, Dialog):
        self.iface = iface
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,330,340).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowTitle("decoupeur")
        
        # QLabel lancer recherche
        self.label10 = QtGui.QLabel(Dialog)
        self.label10.setGeometry(QtCore.QRect(15,20,300,18))
        self.label10.setObjectName("label10")
        self.label10.setText("Sélectionner une couche de points à projeter :  ")

        ListeCouchesPoint=[""]
        NbCouches=self.iface.mapCanvas().layerCount()
        if NbCouches==0: QMessageBox.information(None,"information:","Pas de couches ! ")
        else:
            for i in range(0,NbCouches):
                couche=self.iface.mapCanvas().layer(i)
                # 0 pour point
                if couche.geometryType()== 0 or couche.geometryType()==3 :
                    if couche.isValid():
                       ListeCouchesPoint.append(couche.name())
                    else:
                       QMessageBox.information(None,"information:","Pas de couche de points! ")
                       return None
        self.ComboBoxPoints = QtGui.QComboBox(Dialog)
        self.ComboBoxPoints.setMinimumSize(QtCore.QSize(300, 25))
        self.ComboBoxPoints.setMaximumSize(QtCore.QSize(300, 25))
        self.ComboBoxPoints.setGeometry(QtCore.QRect(10, 45, 300,25))
        self.ComboBoxPoints.setObjectName("ComboBoxPoints")
        for i in range(len(ListeCouchesPoint)):  self.ComboBoxPoints.addItem(ListeCouchesPoint[i])

        # QLabel de couche ligne
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15,70,280,23))
        self.label.setObjectName("label")
        self.label.setText("<u>Sélectionner sur quelle couche effectuer la projection: </u>")

        ListeCouchesLigne=[""]
        NbCouches=self.iface.mapCanvas().layerCount()
        for i in range(0,NbCouches):
            couche=self.iface.mapCanvas().layer(i)
            # 1 pour ligne
            if couche.geometryType()== 1 or couche.geometryType()== 2 or couche.geometryType()== 4 or couche.geometryType()== 5:
                if couche.isValid():
                   ListeCouchesLigne.append(couche.name())
                else:
                   QMessageBox.information(None,"information:","pas de couches avec lineaire ou bordure ! ")
                   return None
        
        self.ComboBoxLignes = QtGui.QComboBox(Dialog)
        self.ComboBoxLignes.setMinimumSize(QtCore.QSize(300, 25))
        self.ComboBoxLignes.setMaximumSize(QtCore.QSize(300, 25))
        self.ComboBoxLignes.setGeometry(QtCore.QRect(10, 90, 300,25))
        self.ComboBoxLignes.setObjectName("ComboBoxLignes")
        for i in range(len(ListeCouchesLigne)):  self.ComboBoxLignes.addItem(ListeCouchesLigne[i])

        #Exemple de QPushButton
        self.DoButton = QtGui.QPushButton(Dialog)
        self.DoButton.setMinimumSize(QtCore.QSize(200, 20))
        self.DoButton.setMaximumSize(QtCore.QSize(200, 20))        
        self.DoButton.setGeometry(QtCore.QRect(60,140, 200, 20))
        self.DoButton.setObjectName("DoButton")
        self.DoButton.setText(" Lancer le decoupage !")

        self.label_2 = QtGui.QLabel(Dialog)
        self.labelImage = QtGui.QLabel(Dialog)
        self.labelImage.setMinimumSize(QtCore.QSize(300,100))
        self.labelImage.setMaximumSize(QtCore.QSize(300,100))        
        self.labelImage.setGeometry(QtCore.QRect(30, 200, 300,100))
        myPath = os.path.dirname(__file__)+"/icons/onema_logo_quad.jpg";
        myDefPath = myPath.replace("\\","/");
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
     
        #Exemple de QLCDNumber
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMinimumSize(QtCore.QSize(260, 15))
        self.progressBar.setMaximumSize(QtCore.QSize(260, 15))
        self.progressBar.setGeometry(QtCore.QRect(30,175,260,15))
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
            """QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center;}"""
            """QProgressBar::chunk {background-color: #6C96C6; width: 20px;}"""
        )
        #Pose a minima une valeur de la barre de progression / slide contrôle
        self.progressBar.setValue(0)
        
        
        #Exemple de QPushButton
        self.aboutButton = QtGui.QPushButton(Dialog)
        self.aboutButton.setMinimumSize(QtCore.QSize(70, 20))
        self.aboutButton.setMaximumSize(QtCore.QSize(70, 20))        
        self.aboutButton.setGeometry(QtCore.QRect(30, 310, 70, 23))
        self.aboutButton.setObjectName("aboutButton")
        self.aboutButton.setText(" A propos...")
        
        self.PushButton = QtGui.QPushButton(Dialog)
        self.PushButton.setMinimumSize(QtCore.QSize(100, 20))
        self.PushButton.setMaximumSize(QtCore.QSize(100, 20))
        self.PushButton.setGeometry(QtCore.QRect(185, 310, 100,20))
        self.PushButton.setObjectName("PushButton")
        self.PushButton.setText("Fermer")

        QtCore.QObject.connect(self.PushButton,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QObject.connect(self.ComboBoxPoints,QtCore.SIGNAL("currentIndexChanged(QString)"),self.onComboP)
        QtCore.QObject.connect(self.ComboBoxLignes,QtCore.SIGNAL("currentIndexChanged(QString)"),self.onComboL)
        QtCore.QObject.connect(self.aboutButton, SIGNAL("clicked()"), self.doAbout)
        QtCore.QObject.connect(self.DoButton, SIGNAL("clicked()"), self.Run)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
                                                             
    def onComboP(self):
        SelectionP = self.ComboBoxPoints.currentText()
        #QMessageBox.information(None,"information:","couche selectionnee: "+ (SelectionP))
        CoucheP=fonctionsF.getVectorLayerByName(SelectionP)
        counterP=0
        for featP in CoucheP.selectedFeatures():
            counterP+=1
        if counterP==0:
            QMessageBox.information(None,"information:","Il faut sélectionner au moins un point dans la couche_"+ str(CoucheP.name())+" !")
        # on utilise les points selectionnes
        # EnregistrementsP=CoucheP.selectedFeatures()
        # pour travailler automatiquement sur tous les enregistrements
        # Enregistrements=Couche.getFeatures(QgsFeatureRequest())
        
    def onComboL(self):
        SelectionL = self.ComboBoxLignes.currentText()
        #QMessageBox.information(None,"information:","couche selectionnee: "+ (SelectionL))
        CoucheL=fonctionsF.getVectorLayerByName(SelectionL)
        counterL=0
        for featL in CoucheL.selectedFeatures():
            counterL+=1
        if counterL==0:
            QMessageBox.information(None,"information:","Il faut sélectionner au moins un élément dans la couche_"+ str(CoucheL.name())+" !") 
        # on utilise les lignes selectionnees
                
    def doAbout(self):
        d = doAbout.Dialog()
        d.exec_()
    
    def Run(self):
        
        SelectionP = self.ComboBoxPoints.currentText()
        CoucheP=fonctionsF.getVectorLayerByName(SelectionP)
        SelectionL = self.ComboBoxLignes.currentText()
        CoucheL=fonctionsF.getVectorLayerByName(SelectionL)
        counterP=counterL=counterN=counterProgess=0
        
        for featP in CoucheP.selectedFeatures():
            counterP+=1
            
        #zdim est le compteur de la progress bar    
        zDim = counterP
        indexBerge=QgsSpatialIndex()
        for featL in CoucheL.selectedFeatures():
            indexBerge.insertFeature(featL)
            counterL+=1
            #QMessageBox.information(None,"DEBUGindex:",str(indexBerge)) 
        if counterP!=0:
            if  counterL!=0: 
                PtsProj= QgsVectorLayer("Point?crs=epsg:2154", "Proj_de_"+ str(CoucheP.name()), "memory")
                QgsMapLayerRegistry.instance().addMapLayer(PtsProj)
                prPtsProj = PtsProj.dataProvider()
                providerP = CoucheP.dataProvider()
                fieldsP = providerP.fields()
                for f in fieldsP:
                    znameField= f.name()
                    Type= str(f.typeName())
                    if Type == 'Integer': prPtsProj.addAttributes([ QgsField( znameField, QVariant.Int)])
                    if Type == 'Real': prPtsProj.addAttributes([ QgsField( znameField, QVariant.Double)])
                    if Type == 'String': prPtsProj.addAttributes([ QgsField( znameField, QVariant.String)])
                    else : prPtsProj.addAttributes([ QgsField( znameField, QVariant.String)])
                prPtsProj.addAttributes([QgsField("DistanceP", QVariant.Double),
                                          QgsField("XDep", QVariant.Double),
                                          QgsField("YDep", QVariant.Double),
                                          QgsField("Xproj", QVariant.Double),
                                          QgsField("Yproj", QVariant.Double),
                                          QgsField("Xmed", QVariant.Double),
                                          QgsField("Ymed", QVariant.Double)])
                #QMessageBox.information(None,"DEBUG3:","npos ")
                Segments= QgsVectorLayer("LineString?crs=epsg:2154", "Segments_de_decoupage", "memory")
                QgsMapLayerRegistry.instance().addMapLayer(Segments)
                prSegments = Segments.dataProvider()
                prSegments.addAttributes([  QgsField("Point_ID", QVariant.Int)])
                Segments.startEditing()
                for featP in CoucheP.selectedFeatures():
                    counterProgess+=1
                    geomP=featP.geometry()
                    PointID=featP.id()
                    Pointinput = loads(geomP.asWkb())
                    P = Point(Pointinput)
                    X=P.x
                    Y=P.y
                    nearest_point = None
                    nearest_pointID= None
                    minVal=0
                    #counterSelec=3
                    counterSelec=1
                    first= True
                    # nearestBerges est un array des 3 plus proche objets berges
                    #if  counterL<3:
                    #    counterSelec=counterL
                    nearestsfids=indexBerge.nearestNeighbor(QgsPoint(X,Y),counterSelec)
                    #QMessageBox.information(None,"DEBUGnearestIndex:",str(nearestsfids))
                    #http://blog.vitu.ch/10212013-1331/advanced-feature-requests-qgis
                    #layer.getFeatures( QgsFeatureRequest().setFilterFid( fid ) )
                    request = QgsFeatureRequest().setFilterFids( nearestsfids )
                    #list = [ feat for feat in CoucheL.getFeatures( request ) ]
                    # QMessageBox.information(None,"DEBUGnearestIndex:",str(list))
                    for featL in CoucheL.getFeatures(request):
                        geomL=featL.geometry()
                        PProj,Dist=fonctionsF.Projecteurdecoupeur(geomP,geomL)
                        #QMessageBox.information(None,"DEBUG", " Dist: "+ str(Dist))
                        if first:
                            first= False
                            minVal= Dist
                            nearest_point= PProj
                            nearest_pointID= PointID
                        else:
                            if Dist < minVal:
                                minVal=Dist
                                nearest_point=PProj
				nearest_pointID=PointID
		    PProjMin=nearest_point
		    #recupère à l'issue de la boucle sur les objets berges la distance min et le point        
                    PProjID=nearest_pointID
                    min_dist=minVal
                    Xdep=(geomP.asPoint().x())
                    Ydep=(geomP.asPoint().y())
                    Xarr=(PProjMin.asPoint().x())
                    Yarr=(PProjMin.asPoint().y())
                    Xmed=(Xdep+Xarr)/2
                    Ymed=(Ydep+Yarr)/2
                    newfeat = QgsFeature()
                    newfeat.setGeometry(PProjMin)
                    Values= featP.attributes()
                    Values.append(min_dist)
                    Values.append(geomP.asPoint().x())
                    Values.append(geomP.asPoint().y())
                    Values.append(PProjMin.asPoint().x())
                    Values.append(PProjMin.asPoint().y())
                    Values.append(Xmed)
                    Values.append(Ymed)
                    newfeat.setAttributes(Values)
                    # couche segments
                    Cx=(Xarr*5-Xdep)/4
                    Cy=(Yarr*5-Ydep)/4
                    Pd=QgsPoint(Xdep, Ydep)
                    Pa=QgsPoint(Cx,Cy)
                    Seg=[Pd,Pa]
                    GeomSeg=QgsGeometry().fromPolyline(Seg)
                    newfeatSeg=QgsFeature()
                    newfeatSeg.setGeometry(GeomSeg)
                    ValuesSeg=[PProjID]
                    #QMessageBox.information(None,"DEBUG", str(ValuesPoints))
                    newfeatSeg.setAttributes(ValuesSeg)
                    # ce qui suit ajoute les géom et valeurs des enregistrements,
                    prSegments.addFeatures([ newfeatSeg ])
                    #bascule en mode édition- comme icône crayon  :
                    PtsProj.startEditing()
                    # ce qui suit ajoute les géom et valeurs des enregistrements,
                    prPtsProj.addFeatures([ newfeat ])
                    # même effet que: PtsProj.addFeature(newfeat,True)
                    #Quitte le mode édition et enregistre les modifs:
                    PtsProj.commitChanges()
                    zPercent = int(100 * counterProgess / zDim)
                    self.progressBar.setValue(zPercent)
                    Segments.commitChanges()
                    self.iface.mapCanvas().refresh()    
            else: pass          
        else: pass
         
        processing.runalg("qgis:splitlineswithlines",CoucheL,Segments,"cut.shp")
        #processing.alghelp("qgis:splitlineswithlines")
        #ALGORITHM: Split lines with lines
        #INPUT_A <ParameterVector>
        #INPUT_B <ParameterVector>
        #OUTPUT <OutputVector>
        zlayerCut=iface.addVectorLayer("cut.shp",str(CoucheL.name())+"_cut",'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(zlayerCut)
        self.iface.mapCanvas().refresh()
        
        
