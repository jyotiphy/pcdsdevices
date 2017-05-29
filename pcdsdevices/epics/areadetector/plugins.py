#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Overrides for AreaDetector Plugins.
"""

import logging

import ophyd
from ophyd.device import GenerateDatumInterface

from .base import ADBase

logger = logging.getLogger(__name__)


class PluginBase(ophyd.plugins.PluginBase, ADBase):
    # Original:
    #    @property
    #    def _asyn_pipeline_configuration_names(self):
    #        return [_.configuration_names.name for _ in self._asyn_pipeline]
    # This broke any instantiated plugin b/c _asyn_pipeline is a list that can
    # have None.
    @property
    def _asyn_pipeline_configuration_names(self):
        return [_.configuration_names.name for _ in self._asyn_pipeline if 
                hasattr(_, 'configuration_names')]

    def describe_configuration(self):
        # Avoid the method we are overriding
        ret = ADBase.describe_configuration(self)
        source_plugin = self.source_plugin
        if source_plugin is not None:
            ret.update(source_plugin.describe_configuration())
        return ret


class ImagePlugin(ophyd.plugins.ImagePlugin, PluginBase):
    pass


class StatsPlugin(ophyd.plugins.StatsPlugin, PluginBase):
    pass


class ColorConvPlugin(ophyd.plugins.ColorConvPlugin, PluginBase):
    pass


class ProcessPlugin(ophyd.plugins.ProcessPlugin, PluginBase):
    pass


class Overlay(ophyd.plugins.Overlay, ADBase):
    pass


class OverlayPlugin(ophyd.plugins.OverlayPlugin, PluginBase):
    pass


class ROIPlugin(ophyd.plugins.ROIPlugin, PluginBase):
    pass


class TransformPlugin(ophyd.plugins.TransformPlugin, PluginBase):
    pass


class FilePlugin(ophyd.plugins.FilePlugin, PluginBase, GenerateDatumInterface):
    pass


class NetCDFPlugin(ophyd.plugins.NetCDFPlugin, FilePlugin):
    pass


class TIFFPlugin(ophyd.plugins.TIFFPlugin, FilePlugin):
    pass


class JPEGPlugin(ophyd.plugins.JPEGPlugin, FilePlugin):
    pass


class NexusPlugin(ophyd.plugins.NexusPlugin, FilePlugin):
    pass


class HDF5Plugin(ophyd.plugins.HDF5Plugin, FilePlugin):
    pass


class MagickPlugin(ophyd.plugins.MagickPlugin, FilePlugin):
    pass


