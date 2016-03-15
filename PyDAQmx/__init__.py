# -*- coding: utf-8 -*-

from . import DAQmxConfig

from .DAQmxTypes import *
#from .DAQmxConstants import *
from .DAQmxFunctions import *
from .Task import Task
from . import headerparser


__version_info__ = (1, 3)
__version__ = '.'.join(str(num) for num in __version_info__)

__author__ ='Pierre Cladé'
