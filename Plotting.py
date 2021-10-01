from bokeh.models.annotations import Tooltip
from webcam_to_detect_objects import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, sources


fig = figure(x_axis_type = 'datetime', height = 250,
            width = 1000, title = "Motion Graph")


q = fig.quad(left = df["Start"], right = df["End"], bottom = 0, top = 1, color = "green")


output_file("Graph.html")

show(fig)