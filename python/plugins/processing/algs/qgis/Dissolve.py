# -*- coding: utf-8 -*-

"""
***************************************************************************
    Dissolve.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QgsFeature, QgsGeometry
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterBoolean
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputVector
from processing.tools import vector, dataobjects


class Dissolve(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    FIELD = 'FIELD'
    DISSOLVE_ALL = 'DISSOLVE_ALL'

    #==========================================================================
    #def getIcon(self):
    #   return QtGui.QIcon(os.path.dirname(__file__) + "/icons/dissolve.png")
    #==========================================================================

    def processAlgorithm(self, progress):
        useField = not self.getParameterValue(Dissolve.DISSOLVE_ALL)
        fieldname = self.getParameterValue(Dissolve.FIELD)
        vlayerA = dataobjects.getObjectFromUri(
            self.getParameterValue(Dissolve.INPUT))
        vproviderA = vlayerA.dataProvider()
        fields = vlayerA.fields()
        writer = self.getOutputFromName(
            Dissolve.OUTPUT).getVectorWriter(fields,
                                             vproviderA.geometryType(),
                                             vproviderA.crs())
        outFeat = QgsFeature()
        nElement = 0
        features = vector.features(vlayerA)
        nFeat = len(features)

        if not useField:
            first = True
            for inFeat in features:
                nElement += 1
                progress.setPercentage(int(nElement * 100 / nFeat))
                if first:
                    attrs = inFeat.attributes()
                    tmpInGeom = QgsGeometry(inFeat.geometry())
                    if tmpInGeom.isGeosEmpty() or not tmpInGeom.isGeosValid():
                        continue
                    outFeat.setGeometry(tmpInGeom)
                    first = False
                else:
                    tmpInGeom = QgsGeometry(inFeat.geometry())
                    if tmpInGeom.isGeosEmpty() or not tmpInGeom.isGeosValid():
                        continue
                    tmpOutGeom = QgsGeometry(outFeat.geometry())
                    try:
                        tmpOutGeom = QgsGeometry(tmpOutGeom.combine(tmpInGeom))
                        outFeat.setGeometry(tmpOutGeom)
                    except:
                        raise GeoAlgorithmExecutionException(
                            self.tr('Geometry exception while dissolving'))
            outFeat.setAttributes(attrs)
            writer.addFeature(outFeat)
        else:
            fieldIdx = vlayerA.fieldNameIndex(fieldname)
            unique = vector.getUniqueValues(vlayerA, int(fieldIdx))
            nFeat = len(unique)
            myDict = {}
            attrDict = {}
            for item in unique:
                myDict[unicode(item).strip()] = []
                attrDict[unicode(item).strip()] = None

            unique = None

            for inFeat in features:
                attrs = inFeat.attributes()
                tempItem = attrs[fieldIdx]
                tmpInGeom = QgsGeometry(inFeat.geometry())
                if tmpInGeom.isGeosEmpty() or not tmpInGeom.isGeosValid():
                    continue

                if attrDict[unicode(tempItem).strip()] == None:
                    # keep attributes of first feature
                    attrDict[unicode(tempItem).strip()] = attrs

                myDict[unicode(tempItem).strip()].append(tmpInGeom)

            features = None

            for key, value in myDict.items():
                nElement += 1
                progress.setPercentage(int(nElement * 100 / nFeat))
                for i in range(len(value)):
                    tmpInGeom = value[i]

                    if i == 0:
                        tmpOutGeom = tmpInGeom
                    else:
                        try:
                            tmpOutGeom = QgsGeometry(
                                tmpOutGeom.combine(tmpInGeom))
                        except:
                            raise GeoAlgorithmExecutionException(
                                self.tr('Geometry exception while dissolving'))
                outFeat.setGeometry(tmpOutGeom)
                outFeat.setAttributes(attrDict[key])
                writer.addFeature(outFeat)

        del writer

    def defineCharacteristics(self):
        self.name = 'Dissolve'
        self.group = 'Vector geometry tools'
        self.addParameter(ParameterVector(Dissolve.INPUT,
                                          self.tr('Input layer'),
                                          [ParameterVector.VECTOR_TYPE_POLYGON, ParameterVector.VECTOR_TYPE_LINE]))
        self.addParameter(ParameterBoolean(Dissolve.DISSOLVE_ALL,
                                           self.tr('Dissolve all (do not use field)'), True))
        self.addParameter(ParameterTableField(Dissolve.FIELD,
                                              self.tr('Unique ID field'), Dissolve.INPUT, optional=True))
        self.addOutput(OutputVector(Dissolve.OUTPUT, self.tr('Dissolved')))
