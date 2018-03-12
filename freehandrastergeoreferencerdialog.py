# -*- coding: utf-8 -*-
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path
import string

from PyQt4 import QtGui
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QFileDialog, QMessageBox
from qgis.core import QgsProject

from ui_freehandrastergeoreferencer import Ui_FreehandRasterGeoreferencer
import utils


class FreehandRasterGeoreferencerDialog(QtGui.QDialog,
                                        Ui_FreehandRasterGeoreferencer):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        QObject.connect(self.pushButtonBrowse, SIGNAL(
            "clicked()"), self.showBrowserDialog)

    def clear(self):
        self.lineEditImagePath.setText("")

    def showBrowserDialog(self):
        bDir, found = QgsProject.instance().readEntry(
            utils.SETTINGS_KEY, utils.SETTING_BROWSER_RASTER_DIR, None)
        if not found:
            bDir = os.path.expanduser("~")

        filepath = u'%s' % (QFileDialog.getOpenFileName(
            self, "Select image", bDir, "Images (*.png *.bmp *.jpg *.tif)"))

        if filepath:
            self.lineEditImagePath.setText(filepath)
            bDir, _ = os.path.split(filepath)
            QgsProject.instance().writeEntry(utils.SETTINGS_KEY,
                                             utils.SETTING_BROWSER_RASTER_DIR,
                                             bDir)

    def accept(self):
        result, message, details = self.validate()
        if result:
            self.done(QtGui.QDialog.Accepted)
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle(u"Error")
            msgBox.setText(message)
            msgBox.setDetailedText(details)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()

    def validate(self):
        result = True
        message = ""
        details = ""

        self.imagePath = self.lineEditImagePath.text()
        _, extension = os.path.splitext(self.imagePath)
        extension = string.lower(extension)
        if not os.path.isfile(self.imagePath) or \
                (extension not in [".jpg", ".bmp", ".png", ".tif"]):
            result = False
            if len(details) > 0:
                details += '\n'
            details += u"The path must be an image file"

        if not result:
            message = "There were errors in the form"

        return result, message, details
