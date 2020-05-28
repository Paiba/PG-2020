import pandas as pd
import tkinter as tk
import bokeh as bk
import matplotlib as mpl


from tkinter import filedialog
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Grid, HBar, LinearAxis, Plot, HoverTool,BoxSelectTool, Panel, Tabs
from bokeh.layouts import layout
from bokeh.palettes import Paired12
from bokeh.transform import factor_cmap
###
class Aba_geografica:

         def __init__(self, dados):
