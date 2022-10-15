# Figure 3: Proportion distribution of mental health-related tweets in the USA
#  Heatmap: Geographical distributions for the tweets from February 1st, 2020 to April 30th, 2022.
#  Map: The monthly proportion of mental health-related tweets in the 50 states of the USA.
import pandas as pd
from pyecharts.charts import HeatMap, Map, Grid
import pyecharts.options as opts
import datetime
import statsmodels.api as sm

# data preprocessing
data = pd.read_csv("D:/research/COVID/text/result_review/data/count/state_count_all1.csv")
data =data.fillna(0)
data['mental_total'] = data['anxiety_spam']+data['depression_spam']+data['insomnia_spam']+data['abuse_spam']
data['mental_p'] = round(data['mental_total']/data['clean'],4)
data['95CI'] = data.apply(lambda x:[round(num,4) for num in sm.stats.proportion_confint(x['mental_total'],x['clean'],alpha=0.05,method='normal')],axis=1)
data['95CI'] = data['95CI'].apply(lambda x:tuple(x)).astype(str)
data['proportion'] = data['mental_p'].astype(str)
data['m_p'] = data['proportion']+data['95CI']
data_95ci = pd.pivot(data,index='month',columns='state',values='m_p')
data_95ci.to_excel("D:/research/COVID/text/result_review/excel/mental_state_ci.xlsx")

# remove the row of "state"
data_hp = pd.pivot(data,index='month',columns='state',values='mental_p')
fullname1 = ['Alaska','Alabama', 'Arkansas','Arizona','California','Colorado','Connecticut','Delaware','Florida','Georgia',
'Hawaii','Iowa','Idaho','Illinois','Indiana','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan',
'Minnesota','Missouri','Mississippi','Montana','North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico',
'Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee',
'Texas','Utah','Virginia','Vermont','Washington','Wisconsin','West Virginia','Wyoming']

# Figure 3
# plot the heatmap
data_hp = data_hp.sort_index(ascending=False)
month = data_hp.index.to_list()
data_heatmap = []
data_value = []
for i in fullname1:
    for j in month:
        data_heatmap.append([i, j, data_hp.loc[j, i]])
        data_value.append(data_hp.loc[j, i])
heatmap = (HeatMap(init_opts=opts.InitOpts(width="800px", height="700px"))
            .add_xaxis(fullname1)
            .add_yaxis("proportion", month, data_heatmap)
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category", axistick_opts=opts.AxisTickOpts(is_show=False),
                                     axislabel_opts=opts.LabelOpts(interval=0,rotate=-90,font_size=14,
                                                                  # rich={'Alaska': {color:'red'}}
                                                                   ),
                                     position='top'),
            yaxis_opts=opts.AxisOpts(axistick_opts=opts.AxisTickOpts(is_show=False),
                                     axislabel_opts=opts.LabelOpts(font_size=13)),
            visualmap_opts=opts.VisualMapOpts(max_=max(data_value), min_=min(data_value),
                                              pos_right="15%",
                                              pos_left="90%",
                                              precision=4,
                                              #pos_top="45%",
                                              #'#FFFFFF', '#FFCC99', '#FF3300','#FF0000'
                                              range_color=['#FFFFFF', '#FFCC99', '#FF3300','#FF0000'],
                                              #range_text=['{}%'.format(max(data_value)),'{}%'.format(min(data_value))]
                                              #range_color=['#feedde', '#fdbe85', '#fd8d3c', '#e6550d', '#a63603'],
                                              )
            )
)
grid = (Grid(init_opts=opts.InitOpts(width="800px", height="650px")).add(heatmap, grid_opts=opts.GridOpts(pos_bottom="2%", pos_top="5%", pos_left="2%", pos_right="12%",
                                                   is_contain_label=True), is_control_axis_index=True))
grid.render("D:/research/COVID/text/result_review/photo/geo_heatmap.html")

# plot the map
data_geo = data.groupby('state').agg({'clean':'sum','mental_total':'sum'})
data_geo['mental_p'] = round(data_geo['mental_total']/data_geo['clean'],4)
data_map = []
for i in fullname1:
    data_map.append([i,data_geo['mental_p'][i]])
map1 = (
    Map(init_opts=opts.InitOpts(width="800px", height="400px"))
    .add("", data_pair=data_map, maptype="美国", is_map_symbol_show=False)
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_show=True, max_=0.027, min_=0.012,
                                          split_number=5,
                                          precision=3,
                                          is_piecewise=True,
                                          pieces=[
                                              {'min': 0.02, 'max': 0.022, "label": 'No data'},
                                              {'min': 0.022, 'max': 0.024, "label": '2.2% - 2.4%'},
                                              {'min': 0.024, 'max': 0.026, "label": '2.4% - 2.6%'},
                                              {'min': 0.026, 'max': 0.028, "label": '2.6% - 2.8%'},
                                              {'min': 0.028, 'max': 0.030, "label": '2.8% - 3.0%'}
                                          ],
                                          #'#feedde', '#fd8d3c', '#e6550d', '#a63603'
                                          range_color=['#EEEEEE', '#feedde', '#fd8d3c', '#e6550d', '#a63603'],
                                          pos_right="3%", pos_top="55%", textstyle_opts=opts.TextStyleOpts(font_size=16))
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
map1.render("D:/research/COVID/text/result_review/photo/place_photo.html")