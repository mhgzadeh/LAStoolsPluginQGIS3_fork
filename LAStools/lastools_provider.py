# -*- coding: utf-8 -*-

"""
/***************************************************************************
    lastools_provider.py
    ---------------------
    Date                 : November 2023
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

__author__ = 'rapidlasso'
__date__ = 'September 2023'
__copyright__ = '(C) 2023, rapidlasso GmbH'

from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig

from .lastools.core.processing import (
    LasIndex, LasIndexPro,
    LasMerge, LasMergePro,
    LasOverage, LasOveragePro,
    LasBoundary, LasBoundaryPro,
    LasClip,
    LasTile, LasTilePro,
    LasSplit,
    LasNoise, LasNoisePro,
    LasDiff,
    Las3dPolyHorizontalVerticalDistance, Las3dPolyRadialDistance,
    LasIntensity, LasIntensityAttenuationFactor,
)
from .lastools.core.data_convert import (
    Las2txt, Las2txtPro,
    Txt2Las, Txt2LasPro,
    Las2LasFilter, Las2LasProFilter,
    Las2LasProject, Las2LasProProject,
    Las2LasTransform, Las2LasProTransform,
    Las2Shp,
    Shp2Las,
)
from .lastools.core.classification_filtering import (
    LasGround, LasGroundPro,
    LasGroundNew, LasGroundProNew,
    LasClassify, LasClassifyPro,
    LasThin, LasThinPro,
)
from .lastools.core.data_compression import (
    LasZip, LasZipPro
)
from .lastools.core.dsm_dtm_generation_prodctions import (
    Las2Dem, Las2DemPro,
    Las2Iso,
    LasGrid, LasGridPro,
    LasHeight, LasHeightClassify, LasHeightPro, LasHeightProClassify,
    LasCanopy, LasCanopyPro,
    Blast2Dem, Blast2DemPro,
    Blast2Iso, Blast2IsoPro,
)
from .lastools.core.publishing import (
    LasPublish, LasPublishPro
)
from .lastools.core.quality_control_information import (
    LasInfo, LasInfoPro,
    LasOverlap, LasOverlapPro,
    LasControl,
    LasValidate, LasValidatePro,
)
from .lastools.core.visualization_colorization import (
    LasView, LasViewPro,
    LasColor,
)
from .lastools.core.pipelines import (
    FlightLinesToCHMFirstReturn, FlightLinesToCHMHighestReturn, FlightLinesToCHMSpikeFree,
    FlightLinesToDTMandDSMFirstReturn, FlightLinesToDTMandDSMSpikeFree,
    FlightLinesToMergedCHMFirstReturn, FlightLinesToMergedCHMHighestReturn, FlightLinesToMergedCHMPitFree,
    FlightLinesToMergedCHMSpikeFree,
    HugeFileClassify, HugeFileNormalize, HugeFileGroundClassify,
)
from .lastools.core.utils import paths


class LAStoolsProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)
        self.algos = None

    def load(self):
        """In this method we add settings needed to configure our
        provider.
        """
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(), 'LASTOOLS_ACTIVATED', 'Activate', True))
        ProcessingConfig.addSetting(
            Setting(self.name(), 'LASTOOLS_FOLDER', 'LAStools folder', "C:\LAStools", valuetype=Setting.FOLDER))
        ProcessingConfig.addSetting(Setting(self.name(), 'WINE_FOLDER', 'Wine folder', "", valuetype=Setting.FOLDER))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        ProcessingConfig.removeSetting('LASTOOLS_ACTIVATED')
        ProcessingConfig.removeSetting('LASTOOLS_FOLDER')
        ProcessingConfig.removeSetting('WINE_FOLDER')
        pass

    def isActive(self):
        """Return True if the provider is activated and ready to run algorithms"""
        return ProcessingConfig.getSetting('LASTOOLS_ACTIVATED')

    def setActive(self, active):
        ProcessingConfig.setSettingValue('LASTOOLS_ACTIVATED', active)

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        processing_algorithms = [
            LasIndex(), LasIndexPro(),
            LasMerge(), LasMergePro(),
            LasOverage(), LasOveragePro(),
            LasBoundary(), LasBoundaryPro(),
            LasClip(),
            LasTile(), LasTilePro(),
            LasSplit(),
            LasNoise(), LasNoisePro(),
            LasDiff(),
            Las3dPolyRadialDistance(), Las3dPolyHorizontalVerticalDistance(),
            LasIntensity(), LasIntensityAttenuationFactor()
        ]
        self.algos = processing_algorithms

        data_convert_algorithms = [
            Las2txt(), Las2txtPro(),
            Txt2Las(), Txt2LasPro(),
            Las2LasFilter(), Las2LasProFilter(),
            Las2LasProject(), Las2LasProProject(),
            Las2LasTransform(), Las2LasProTransform(),
            Las2Shp(),
            Shp2Las(),
        ]
        self.algos.extend(data_convert_algorithms)

        classification_filtering_algorithms = [
            LasGround(), LasGroundPro(),
            LasGroundNew(), LasGroundProNew(),
            LasClassify(), LasClassifyPro(),
            LasThin(), LasThinPro(),
        ]
        self.algos.extend(classification_filtering_algorithms)

        data_compression_algorithms = [
            LasZip(), LasZipPro(),
        ]
        self.algos.extend(data_compression_algorithms)

        dsm_dtm_generation_productions_algorithms = [
            Las2Dem(), Las2DemPro(),
            Las2Iso(),
            LasGrid(), LasGridPro(),
            LasHeight(), LasHeightClassify(), LasHeightPro(), LasHeightProClassify(),
            LasCanopy(), LasCanopyPro(),
            Blast2Dem(), Blast2DemPro(),
            Blast2Iso(), Blast2IsoPro(),
        ]
        self.algos.extend(dsm_dtm_generation_productions_algorithms)

        publishing_algorithms = [
            LasPublish(), LasPublishPro(),
        ]
        self.algos.extend(publishing_algorithms)

        quality_control_information_algorithms = [
            LasInfo(), LasInfoPro(),
            LasOverlap(), LasOverlapPro(),
            LasControl(),
            LasValidate(), LasValidatePro(),
        ]
        self.algos.extend(quality_control_information_algorithms)

        visualization_colorization_algorithms = [
            LasView(), LasViewPro(),
            LasColor(),
        ]
        self.algos.extend(visualization_colorization_algorithms)

        pipelines_algorithms = [
            FlightLinesToCHMFirstReturn(), FlightLinesToCHMHighestReturn(), FlightLinesToCHMSpikeFree(),
            FlightLinesToDTMandDSMFirstReturn(), FlightLinesToDTMandDSMSpikeFree(),
            FlightLinesToMergedCHMFirstReturn(), FlightLinesToMergedCHMHighestReturn(), FlightLinesToMergedCHMPitFree(),
            FlightLinesToMergedCHMSpikeFree(),
            HugeFileClassify(), HugeFileGroundClassify(), HugeFileNormalize(),

        ]
        self.algos.extend(pipelines_algorithms)

        for algorithm in self.algos:
            self.addAlgorithm(algorithm)

    def icon(self):
        return QIcon(f'{paths["img"]}/lastools.png')

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'LAStools'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "LAStools") and localised.
        """
        return 'LAStools'

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "LAStools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return 'LAStools LiDAR and point cloud processing'
