# Figure 5:The distribution of tweets in topics for health care workers and the general population
# A. Average number of tweets per user in each topic
# B. Logarithmic ratioa of the average number of tweets between health care workers and the general population on each topic

import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar, Grid
import numpy as np
from pyecharts.commons.utils import JsCode
# data preprocess
data_m = pd.read_csv("D:/research/COVID/text/result_review/data/count/user_topic_count1.csv")
data_topic = pd.read_csv("D:/research/COVID/text/result_review/excel/topic_keywords.csv")
# remove the tweets which have the same probability of belonging to each topic.
data_m = data_m[-(data_m['topic'] == 100)]
data = pd.merge(data_m, data_topic, on='topic')
data['order'] = data['hws_a_num']/data['gp_a_num']
data['order_log'] = np.log2(data['order'].to_list())
data = data.sort_values(by='order_log', axis=0)
color_function = """
    function(params){
        if(params.value>=0){
            return '#c23531';
        }
        return '#2f4554';
    }
"""
# plot the photo
# Figure 5A
data = data.sort_values(by='order', axis=0)
x = data['theme'].to_list()
y1 = data['hws_a_num'].to_list()
y2 = data['gp_a_num'].to_list()
y = data['order_log'].to_list()
Bar1 = (
    Bar(init_opts=opts.InitOpts(width="500px", height="700px"))
    .add_xaxis(xaxis_data=x)
    .add_yaxis(series_name="Health care workers",
               y_axis=y1,
               category_gap="35%",
               label_opts=opts.LabelOpts(is_show=False))
    .add_yaxis(series_name="General population",
               y_axis=y2,
               category_gap="35%",
               label_opts=opts.LabelOpts(is_show=False))
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position='right',is_show=True, formatter=JsCode(
                "function(x){return x.data.toFixed(3);}"
            )
                                               ))
    .set_global_opts(
        legend_opts=opts.LegendOpts(pos_right='2%', pos_top='5%', orient='vertical', textstyle_opts=opts.TextStyleOpts(font_size=18)),
        xaxis_opts=opts.AxisOpts(name="Average number",
                                 name_location="center",
                                 name_gap=22,
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=18),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True),
                                 axislabel_opts=opts.LabelOpts(horizontal_align="right", font_size=16)
                                 ),
        yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=False),
                                 axislabel_opts=opts.LabelOpts(font_size=16)))
    )
grid = (Grid(init_opts=opts.InitOpts(width="800px", height="600px")).add(Bar1, grid_opts=opts.GridOpts(pos_bottom="4%", pos_top='2%', pos_right='2%', pos_left="2%", is_contain_label=True), is_control_axis_index=True))
grid.render("D:/research/COVID/text/result_review/photo/job_topic.html")

# Figure 5B
Bar2 = (
    Bar(init_opts=opts.InitOpts(width="500px", height="700px"))
    .add_xaxis(xaxis_data=x)
    .add_yaxis(series_name="Health care workers",
               y_axis=y,
               category_gap="40%",
               label_opts=opts.LabelOpts(is_show=False),
               itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)))
    # .add_yaxis(series_name="General population",
    #            y_axis=y2,
    #            category_gap="40%",
    #            label_opts=opts.LabelOpts(is_show=False))
    .reversal_axis()
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=False, pos_right='2%', pos_top='5%', orient='vertical', textstyle_opts=opts.TextStyleOpts(font_size=18)),
        xaxis_opts=opts.AxisOpts(#name="log2(ratio)",
                                 name_location="center",
                                 name_gap=22,
                                 min_=-1.0,
                                 max_=1.0,
                                 split_number=10,
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=18),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True, is_align_with_label=True),
                                 axislabel_opts=opts.LabelOpts(horizontal_align="right", font_size=16)
                                 ),
        yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=False),
                                 axislabel_opts=opts.LabelOpts(font_size=16)))
    )
grid = (Grid(init_opts=opts.InitOpts(width="800px", height="500px")).add(Bar2, grid_opts=opts.GridOpts(pos_bottom="4%", pos_top='2%', pos_right='2%', pos_left="2%", is_contain_label=True), is_control_axis_index=True))
grid.render("D:/research/COVID/text/result_review/photo/job_topic1.html")
