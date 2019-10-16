# -*- coding: utf-8 -*-

import bokeh.plotting as bp
from bokeh.models import DatetimeTickFormatter, Legend
from bokeh.models.tools import HoverTool
from bokeh.io import output_file
        
#%%
def create_plot(df, x=None, size=(None, None), title=None, colors=None, circles=True, output=None):
    '''
    Creates plots of all variables against x variable.
    
    Parameters
    ----------
    df: pandas.DataFrame
        dataframe of variables that we want to plot
    x: str
        name of variable from df which we want to be on x-axis.
    size: tuple(int, int)
        width and height        
    title: str, optional
        plot title
    colors: list of strings, optional
        list of plots colors
    circles: boolean, default True
        if True circles will be added.
    output: str
        path in which we want to save the plot
    '''
    size=(None, None)
    plot_width = size[0] or 1000
    plot_height = size[1] or 700
    colors = ['green', 'red', 'yellow', 'orange', 'blue' , 'brown', 'purple', 'black']
    x = pd.to_datetime(df.Data)
    y = df.drop(columns=x.name)
    
    p = bp.figure(plot_width=plot_width, plot_height=plot_height,
                x_axis_type='datetime', toolbar_location='above',
                output_backend='webgl')
    
    lines = []
    for i, color in zip(range(y.shape[1]), colors):
        lines.append(p.line(x, y.iloc[:,i], line_width=1, color=color))
    
    p.xaxis.axis_label = 'Data'
    p.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"])
    p.yaxis.axis_label = 'MW'
    
    p.add_tools(HoverTool(tooltips=[(x.name,'@x{%F}'), ('MW', '@y')], renderers=[*lines], mode='mouse',
                                formatters={'x':'datetime'}))
    items = [(column, [line]) for column, line in zip(y.columns, lines)]
    legend = Legend(items=items, location=('center'), click_policy='hide')
    #p.legend.click_policy = "hide"
    p.add_layout(legend, 'below')       
    
    output_file('wykres.html') 
    #+ pd.Timestamp.today().strftime('%Y-%m-%d %Hh%Mm')
     #           +'.html')
    bp.save(p)

#%%
