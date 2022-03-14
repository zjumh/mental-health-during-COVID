#ITS analyssis
import pandas as pd
import numpy as np
import statsmodels.api as sm
import pyecharts.options as opts
from pyecharts.charts import Scatter, Line, Grid
#read the csv containing the proportion of mental helath related tweets in states(CA,NY,TX,FL)
data = pd.read_csv("D:\program\code\\result\\4state.csv")
data.columns = ["date", "CA", "NY", "TX", "FL", "CA_c", "NY_c", "TX_c", "FL_c"]
data.sort_values(by='date', inplace=True)
num = list(range(0, len(data)))
data.index = num
#definie a function used for ITS
def its(data, time, day):
    n = data[data.date == time].index.values[0]
    day = day
    s = n - day
    m = n + day
    data1 = data.loc[s:m]
    listtime = list(range(1, len(data1)+1))
    data1['time'] = listtime
    list1 = np.full(day, 0).tolist()
    list2 = np.full(day + 1, 1).tolist()
    listdeal = list1 + list2
    data1['deal'] = listdeal
    listt_d = np.multiply(listtime, listdeal)
    data1['t_d'] = listt_d
    model = sm.formula.ols('p~time+deal+t_d', data=data1).fit()
    print(model.summary())
    # plot the scatter
    # prepare the values for plotting
    x_data = data1['time'].to_list()
    y_data = data1['p'].to_list()
    y = np.array(y_data)
    day = 15
    y_before = y.copy()
    y_after = y.copy()
    y_before[day:] = None
    y_after[:day] = None
    y_pre = model.fittedvalues.values.copy()
    y_pre0 = y_pre.copy()
    y_pre0[day:] = None
    y_pre1 = y_pre.copy()
    y_pre1[:day] = None
    z = [-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
#plot the scatter
    scatter = (
        Scatter(init_opts=opts.InitOpts(width="800px", height="500px"))
            .add_xaxis(xaxis_data=z)
            .add_yaxis(
            series_name="Before lockdown policy",
            y_axis=y_before,
            symbol_size=8,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="After lockdown policy",
            y_axis=y_after,
            symbol_size=8,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(pos_left="85%", pos_top="15%"),
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
    )
    # plot the line
    line = (
        Line(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(xaxis_data=z)
        .add_yaxis(
            series_name="Before lockdown policy",
            y_axis=y_pre0,
            # is_smooth=True,
            symbol='triangle',
            symbol_size=8,
            linestyle_opts=opts.LineStyleOpts(width=2),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(symbol=None)
        )
        .add_yaxis(
            series_name="After lockdown policy",
            y_axis=y_pre1,
            # is_smooth=True,
            symbol='diamond',
            symbol_size=8,
            linestyle_opts=opts.LineStyleOpts(width=2),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(symbol=None)
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            legend_opts=opts.LegendOpts(is_show=True, pos_left="85%", pos_top="15%",
                                        textstyle_opts=opts.TextStyleOpts(font_size=18)),
            xaxis_opts=opts.AxisOpts(type_="value",
                                     name='Days',
                                     name_location="end",
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=14),
                                     boundary_gap=False,
                                     axistick_opts=opts.AxisTickOpts(is_inside=True),
                                     axislabel_opts=opts.LabelOpts(interval=3, font_size=14)),
            yaxis_opts=opts.AxisOpts(type_="value",
                                     name="Proportion / %",
                                     axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                                     name_gap=45,
                                     name_location="middle",
                                     axistick_opts=opts.AxisTickOpts(is_inside=True),
                                     axislabel_opts=opts.LabelOpts(font_size=14),
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=16)
                                     )
        )
        .set_series_opts(markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(x="0")],
                         label_opts=opts.LabelOpts(is_show=False, position='rightTop'), symbol='none')
                         )
    )
    line.overlap(scatter)
    return line

data1 = data[['date', 'CA', 'CA_c']]
data1['p'] = data1['CA_c']/data1['CA']
line1 = its(data=data1, time="2020-03-19", day=15)
line1.set_global_opts(title_opts=opts.TitleOpts(pos_left="21%", pos_top="47%", title="California"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18)),
                      )
line1.render("D:\\research\COVID\\text\photo\\CA.html")
data2 = data[['date', 'NY', 'NY_c']]
data2['p'] = data2['NY_c']/data2['NY']
line2 = its(data=data2, time="2020-03-22", day=15)
line2.set_global_opts(title_opts=opts.TitleOpts(pos_left="71%", pos_top="47%", title="New York"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line2.render("D:\\research\COVID\\text\photo\\NY.html")
data3 = data[['date', 'TX', 'TX_c']]
data3['p'] = data3['TX_c']/data3['TX']
line3 = its(data=data3, time="2020-04-02", day=15)
line3.set_global_opts(title_opts=opts.TitleOpts(pos_left="23%", pos_top="94%", title="Texas"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line3.render("D:\\research\COVID\\text\photo\\TX.html")
data4 = data[['date', 'FL', 'FL_c']]
data4['p'] = data4['FL_c']/data4['FL']
line4 = its(data=data4, time="2020-04-03", day=15)
line4.set_global_opts(title_opts=opts.TitleOpts(pos_left="72%", pos_top="94%", title="Florida"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line4.render("D:\\research\COVID\\text\photo\\FL.html")
grid=(
    Grid(init_opts=opts.InitOpts(width="800px", height="500px"))
    .add(line1, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_bottom="57%", pos_top="9%"))
    .add(line2, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_bottom="57%", pos_top="9%"))
    .add(line3, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_top="57%", pos_bottom="9%"))
    .add(line4, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_top="57%", pos_bottom="9%"))
)
grid.render("D:\\research\COVID\\text\photo\\ITS.html")
