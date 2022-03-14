# the tweets number in each topic among HCWs and the general population
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar, Grid
data_m = pd.read_csv("D:/research/COVID/text/result/count/M_topic17.csv")
data_p = pd.read_csv("D:/research/COVID/text/result/count/P_topic17.csv")
#ensure the encoding way before reading the file, usually "UTF-8" or "ANSI"
data_topic = pd.read_csv("D:/research/COVID/text/result/LDA model 17.csv", encoding='ANSI')
data_m.columns = ["topic", "num_m"]
data_p.columns = ["topic", "num_p"]
del data_topic["key words"]
data_topic.columns = ["topic", "theme"]
data1 = pd.merge(data_m, data_p, how='outer', on='topic')
data = pd.merge(data_topic, data1, how='outer', on='topic')
#in fact, some tweets had the same possibility to be
data.drop(data.index[len(data)-1], inplace=True)
sum1 = data['num_m'].sum()
sum2 = data['num_p'].sum()
data['proportion_m'] = data['num_m']/sum1
data['proportion_p'] = data['num_p']/sum2
data['order'] = data['proportion_m']/data['proportion_p']
#for i in range(len(data)):
#    if data['p_value'][i] > 0:
#        data['order'][i] = data['proportion_m'][i]
#    else:
#        data['order'][i] = 1-data['proportion_p'][i]
data = data.sort_values(by='order', axis=0)
x = data['theme'].to_list()
y1 = data['proportion_m'].to_list()
y2 = data['proportion_p'].to_list()
Bar = (
    Bar(init_opts=opts.InitOpts(width="500px", height="700px"))
    .add_xaxis(xaxis_data=x)
    .add_yaxis(series_name="Healthcare workers",
               y_axis=y1,
               category_gap="40%",
               label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis(series_name="General population",
               y_axis=y2,
               category_gap="40%",
               label_opts=opts.LabelOpts(is_show=False))
    .reversal_axis()
    .set_global_opts(
        legend_opts=opts.LegendOpts(pos_right='2%', pos_top='5%', orient='vertical', textstyle_opts=opts.TextStyleOpts(font_size=18)),
        xaxis_opts=opts.AxisOpts(name="Proportion",
                                 name_location="center",
                                 name_gap=22,
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=18),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True),
                                 axislabel_opts=opts.LabelOpts(horizontal_align="right", font_size=16)
                                 ),
        yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=False),
                                 axislabel_opts=opts.LabelOpts(font_size=16)))
    )
grid = (Grid(init_opts=opts.InitOpts(width="800px", height="500px")).add(Bar, grid_opts=opts.GridOpts(pos_bottom="4%", pos_top='2%', pos_right='2%', pos_left="2%", is_contain_label=True), is_control_axis_index=True))
grid.render("D:\\research\COVID\\text\\photo\\job_topic.html")
