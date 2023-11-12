# -*- coding: utf-8 -*-

"""
***************************************************************************
    lasviewPro.py
    ---------------------
    Date                 : October 2014 and August 2018
    Copyright            : (C) 2023 by rapidlasso GmbH
    Email                : info near rapidlasso point de
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Martin Isenburg'
__date__ = 'October 2014'
__copyright__ = '(C) 2023, rapidlasso GmbH'

import os
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterNumber

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lasviewPro(LAStoolsAlgorithm):

    POINTS = "POINTS"

    SIZE = "SIZE"
    SIZES = ["1024 768", "800 600", "1200 900", "1200 400", "1550 900", "1550 1150"]

    COLORING = "COLORING"
    COLORINGS = ["default", "classification", "elevation1", "elevation2", "intensity", "return", "flightline", "rgb"]

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.add_parameters_files_are_flightlines_gui()
        self.addParameter(QgsProcessingParameterNumber(lasviewPro.POINTS, "max number of points sampled", QgsProcessingParameterNumber.Integer, 5000000, False, 100000, 20000000))
        self.addParameter(QgsProcessingParameterEnum(lasviewPro.COLORING, "color by", lasviewPro.COLORINGS, False, 0))
        self.addParameter(QgsProcessingParameterEnum(lasviewPro.SIZE,"window size (x y) in pixels", lasviewPro.SIZES, False, 0))
        self.add_parameters_additional_gui()
        self.add_parameters_verbose_gui()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lasview")]
        self.add_parameters_verbose_commands(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        self.add_parameters_files_are_flightlines_commands(parameters, context, commands)
        points = self.parameterAsInt(parameters, lasviewPro.POINTS, context)
        commands.append("-points " + unicode(points))
        coloring = self.parameterAsInt(parameters, lasviewPro.COLORING, context)
        if (coloring != 0):
            commands.append("-color_by_" + lasviewPro.COLORINGS[coloring])
        size = self.parameterAsInt(parameters, lasviewPro.SIZE, context)
        if (size != 0):
            commands.append("-win " + lasviewPro.SIZES[size])
        self.add_parameters_additional_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lasviewPro'

    def displayName(self):
        return 'lasviewPro'

    def group(self):
        return 'folder - checking quality'

    def groupId(self):
        return 'folder - checking quality'

    def createInstance(self):
        return lasviewPro()
