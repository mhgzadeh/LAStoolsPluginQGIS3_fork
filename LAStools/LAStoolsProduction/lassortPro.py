# -*- coding: utf-8 -*-

"""
***************************************************************************
    lassortPro.py
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
from qgis.core import QgsProcessingParameterBoolean

from ..LAStoolsUtils import LAStoolsUtils
from ..lastools_algorithm import LAStoolsAlgorithm

class lassortPro(LAStoolsAlgorithm):

    BY_GPS_TIME = "BY_GPS_TIME"
    BY_RETURN_NUMBER = "BY_RETURN_NUMBER"
    BY_POINT_SOURCE_ID = "BY_POINT_SOURCE_ID"

    def initAlgorithm(self, config):
        self.add_parameters_point_input_folder_gui()
        self.addParameter(QgsProcessingParameterBoolean(lassortPro.BY_GPS_TIME, "sort by GPS time", False))
        self.addParameter(QgsProcessingParameterBoolean(lassortPro.BY_RETURN_NUMBER, "sort by return number", False))
        self.addParameter(QgsProcessingParameterBoolean(lassortPro.BY_POINT_SOURCE_ID, "sort by point source ID", False))
        self.add_parameters_output_directory_gui()
        self.add_parameters_output_appendix_gui()
        self.add_parameters_point_output_format_gui()
        self.add_parameters_additional_gui()
        self.add_parameters_cores_gui()
        self.add_parameters_verbose_gui64()

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(LAStoolsUtils.LAStoolsPath(), "bin", "lassort")]
        self.add_parameters_verbose_commands64(parameters, context, commands)
        self.add_parameters_point_input_folder_commands(parameters, context, commands)
        if (self.parameterAsBool(parameters, lassortPro.BY_GPS_TIME, context)):
            commands.append("-gps_time")
        if (self.parameterAsBool(parameters, lassortPro.BY_RETURN_NUMBER, context)):
            commands.append("-return_number")
        if (self.parameterAsBool(parameters, lassortPro.BY_POINT_SOURCE_ID, context)):
            commands.append("-point_source")
        self.add_parameters_output_directory_commands(parameters, context, commands)
        self.add_parameters_output_appendix_commands(parameters, context, commands)
        self.add_parameters_point_output_format_commands(parameters, context, commands)
        self.add_parameters_additional_commands(parameters, context, commands)
        self.add_parameters_cores_commands(parameters, context, commands)

        LAStoolsUtils.runLAStools(commands, feedback)

        return {"": None}

    def name(self):
        return 'lassortPro'

    def displayName(self):
        return 'lassortPro'

    def group(self):
        return 'folder - processing points'

    def groupId(self):
        return 'folder - processing points'

    def createInstance(self):
        return lassortPro()
