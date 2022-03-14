# heatmap and map
#  Proportion distribution of mental health-related tweets in the USA.
#  a.Geographical distributions for the tweets from February 1st, 2020 to September 30th, 2021.
#  b.The monthly proportion of mental health-related tweets in the 50 states of the USA.
import pandas as pd
from pyecharts.charts import HeatMap, Map, Grid
import pyecharts.options as opts
import datetime
data = pd.read_csv("D:\\research\COVID\\text\\result\count\count1.csv")
df = pd.DataFrame(data.values.T, index=data.columns, columns=data['state'])
# remove the row of "state"
df = df.drop(['state'])
df['csv'] = df.index
df['month'] = df['csv'].apply(lambda x: x[:-6])
c = df.groupby(['month'])[['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','ME','MD','MA','MI','MN',
            'MO','MS','MT','NC',"ND","NE",'NH','NJ','NM','NV','NY','OH','OK','OR','PA','RL','SC','SD','TN','TX','UT',
            'VA','VT','WA','WI','WV','WY']].agg(['sum'])
c.to_csv("D:\\research\COVID\\text\\result\count\clean_state_count1.csv")
data_clean = pd.read_csv("D:\\research\COVID\\text\\result\count\clean_state_count1.csv")
data_mental = pd.read_csv("D:\\research\COVID\\text\\result\count\mental_state_month_count1.csv")
# preproce the data
data_clean = data_clean.drop([0, 1])
data_mental = data_mental.drop(["Unnamed: 0"], axis=1)
data_mental = pd.DataFrame(data_mental.values.T, index=data_mental.columns, columns=data_mental['state'])
data_mental = data_mental.drop(['state'])
data_mental['time'] = data_mental.index
data_mental['month'] = data_mental['time'].apply(lambda x: x.replace('20', ''))
data_mental = data_mental.sort_values(by='month', ascending=True)
#states in different parties
state = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','ME','MD','MA','MI','MN',
            'MO','MS','MT','NC',"ND","NE",'NH','NJ','NM','NV','NY','OH','OK','OR','PA','RL','SC','SD','TN','TX','UT',
            'VA','VT','WA','WI','WV','WY']
fullname1 = ['Alaska','Alabama', 'Arkansas','Arizona','California','Colorado','Connecticut','Delaware','Florida','Georgia',
'Hawaii','Iowa','Idaho','Illinois','Indiana','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan',
'Minnesota','Missouri','Mississippi','Montana','North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico',
'Nevada','New York','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee',
'Texas','Utah','Virginia','Vermont','Washington','Wisconsin','West Virginia','Wyoming',
]
data_clean.index = data_mental.index
data_mental[state] = data_mental[state].astype(int)
data_clean[state] = data_clean[state].astype(int)
data = pd.DataFrame()
data[state] = round(data_mental[state]/data_clean[state],4)
data.columns = fullname1
data['time'] = data.index
def timechange(time):
    time_format = datetime.datetime.strptime(time, '%y%b')
    end = datetime.datetime.strftime(time_format, '%Y-%m')
    return end
data['month'] = data['time'].apply(timechange)
data = data.sort_values(by='month',ascending=False)
# plot the heatmap
month = data['time'].to_list()
data_heatmap = []
data_value = []
for i in fullname1:
    for j in month:
        data_heatmap.append([i, j, data.loc[j, i]])
        data_value.append(data.loc[j, i])
heatmap = (HeatMap(init_opts=opts.InitOpts(width="800px", height="500px"))
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
                                              precision=4,
                                              pos_right="15%",
                                              pos_left="90%",
                                              #pos_top="45%",
                                              #'#FFFFFF', '#FFCC99', '#FF3300','#FF0000'
                                              range_color=['#feedde', '#fdbe85', '#fd8d3c', '#e6550d', '#a63603'],
                                              )
            )
)
grid = (Grid(init_opts=opts.InitOpts(width="800px", height="500px")).add(heatmap, grid_opts=opts.GridOpts(pos_bottom="2%", pos_top="5%", pos_left="2%", pos_right="12%",
                                                   is_contain_label=True), is_control_axis_index=True))
grid.render("D:\\research\COVID\\text\\photo\geo_heatmap1p.html")
# plot the map
del data_mental['time']
del data_mental['month']
del data_clean['state']
print(data_clean.index)
data_mental.loc['row_sum'] = data_mental.apply(lambda x: x.sum(), axis=0)
data_clean.loc['row_sum'] = data_clean.apply(lambda x: x.sum(), axis=0)
data = pd.DataFrame()
data[state] = round(data_mental[state]/data_clean[state], 4)
num = data.loc['row_sum'].to_list()
a = max(num)
b = min(num)
data_map = [list(z) for z in zip(fullname1, num)]
map1 = (
    Map(init_opts=opts.InitOpts(width="800px", height="400px"))
    .add("", data_pair=data_map, maptype="美国", is_map_symbol_show=False)
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_show=True, max_=0.027, min_=0.012,
                                          split_number=5,
                                          precision=3,
                                          is_piecewise=True,
                                          pieces=[
                                              {'min': 0.012, 'max': 0.015, "label": 'No data'},
                                              {'min': 0.015, 'max': 0.018, "label": '1.5% - 1.8%'},
                                              {'min': 0.018, 'max': 0.021, "label": '1.8% - 2.1%'},
                                              {'min': 0.021, 'max': 0.024, "label": '2.1% - 2.4%'},
                                              {'min': 0.024, 'max': 0.027, "label": '2.4% - 2.7%'}
                                          ],
                                          #'#feedde', '#fd8d3c', '#e6550d', '#a63603'
                                          range_color=['#EEEEEE', '#feedde', '#fd8d3c', '#e6550d', '#a63603'],
                                          pos_right="3%", pos_top="55%", textstyle_opts=opts.TextStyleOpts(font_size=16))
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
)
map1.render("D:\\research\COVID\\text\photo\place_photo1.html")
