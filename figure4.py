# Figure 4: Dynamic characteristics of topic proportions.
import pandas as pd
import pyecharts
import pyecharts.options as opts
from pyecharts.charts import ThemeRiver, Line, Grid
from pyecharts.render import make_snapshot
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import cblind as cb
import scicomap as sc
topic_month = pd.read_csv("D:/research/COVID/text/result_review/data/count/topic_month_count1.csv")
df_topic = pd.read_csv("D:/research/COVID/text/result_review/excel/topic_keywords.csv")
topic_month = topic_month[-(topic_month['topic']==100)]
df = pd.merge(topic_month,df_topic[['topic','theme']],on='topic')
df2 = df.groupby('month').agg({'id':'sum'}).reset_index()
df2.columns = ['month','total']
df3 = pd.merge(df, df2, on='month')
df3['proportion'] = df3['id']/df3['total']
df4= df3[df3['month']=='2020-02']
df4 = df4.sort_values(by='id')
topic1 = df4['theme'].to_list()[0:8]
df4 = df4.sort_values(by='id',ascending=False)
topic2 = df4['theme'].to_list()[0:8]
topic = []
for i in range(len(topic1)):
    topic.append(topic2[i])
    topic.append(topic1[i])
month_list = df3['month'].to_list()
month = list(set(month_list))
month.sort(key=month_list.index)

# plot the photo
# Figure 4
area = (
    Line()
    .add_xaxis(xaxis_data=month)
)
# a list of 16 colors
color_list = []
for i in range(len(topic)):
    name = topic[i]
    color = color_list[i]
    data2 = df3[df3['theme'].str.contains(name)]
    y_data = data2['proportion'].to_list()
    area.add_yaxis(
        series_name=name,
        y_axis=y_data,
        stack="总量",
        symbol="emptyCircle",
        is_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(opacity=1, color=color),
        is_smooth=True
    )
area.set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
        legend_opts=opts.LegendOpts(is_show=True),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                 axislabel_opts=opts.LabelOpts(font_size=16, rotate=90)),
    )
grid1 = (Grid(init_opts=opts.InitOpts(width="800px", height="600px"))
        .add(area, grid_opts=opts.GridOpts(pos_bottom="2%", pos_top="0%", pos_left="17%", pos_right="2%",
                                                   is_contain_label=True))
        )
grid1.render("D:/research/COVID/text/result_review/photo/theme_river.html")
print(topic)