""" 
    What we've done:

        1) Created some data
        2) Plotted it
        3) Created a Slider widget to interact with the data
        4) Told the script to output the plot and widget to a browser

"""

import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Slider
from bokeh.layouts import row, widgetbox
from bokeh.io import curdoc

#+++++++++++++++++++++++++ GENERAL SETUP +++++++++++++++++++++++++++++++++++++++
# Create some data to describe the sin wave.
N = 100
x = np.linspace(0, 4*np.pi, N)

def sin_func(x, amp=1.0, phi=0.0, w =1.0):

    return amp*np.sin(w*x + phi)

y = sin_func(x)

#+++++++++++++++++++++ SETUP BOKEH STUFF +++++++++++++++++++++++++++++++++++++++
# Add our data as a dictionary via the "data" argument in ColumnDataSource: 
source = ColumnDataSource(data=dict(x = x, y = y))

# Create the plot, set the figure height, width, specify plot tools:
plot = figure(plot_height=400, plot_width=900,
              tools="box_zoom,crosshair,pan,reset,save,wheel_zoom",
              x_range=[min(x), max(x)])

# Draw the plot:
plot.line('x', 'y', source = source, alpha=0.6, line_width=2)

# axes labels:
plot.xaxis.axis_label = "x"
plot.yaxis.axis_label = "y"

# Define widget(s):                                                                                
phase = Slider(title="Phase", value=0, start=0, end=2*np.pi, step=0.1)

#+++++++++++++++++++++ BOKEH WIDGET CALLBACKS +++++++++++++++++++++++++++++++++++
# This function updates data values whenever the user interacts with a widget.
def update_data(attrname, old, new):

    # Get the current slider values
    phi = phase.value

    # re-assign data values:
    x = np.linspace(0, 4*np.pi, N)
    y = sin_func(x, phi = phi)

    # update source's data:
    source.data = dict(x = x, y = y)

#+++++++++++++++++++++ BOKEH WIDGET & PLOT UPDATES +++++++++++++++++++++++++++++++

# Here we loop over each widget of interest and "on change" we update.
widgets = [phase]
for widget in widgets:
    widget.on_change('value', update_data)

# Here we're adding a widget box containing our widgets to the inputs...
inputs = widgetbox(*widgets)

# ...and adding our widget box and plot all in one row with specified width 
curdoc().add_root(row(inputs, plot, width=1600))
curdoc().title = "A Sine Wave"