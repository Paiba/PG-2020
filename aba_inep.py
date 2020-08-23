import pandas as pd
import bokeh as bk
import matplotlib as mpl
import numpy as np


from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs, CheckboxGroup
from bokeh.layouts import layout, Spacer
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
###
class Aba_inep:

         def __init__(self, dados):
               
                self.aba = 0
