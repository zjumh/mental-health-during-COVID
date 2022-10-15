import pandas as pd
import numpy as np
import statsmodels.api as sm
import pyecharts.options as opts
from pyecharts.charts import Scatter, Line, Grid

#read the csv containing the proportion of mental helath related tweets in states
data = pd.read_csv("D:/research/COVID/text/result_review/data/count/its_count_all1.csv")
data_mental = pd.read_csv("D:/research/COVID/text/result_review/data/count/its_count_mental.csv")
data_mental = data_mental.fillna(0)
full_name = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
             'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
             'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
             'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
             'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
             'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
count = []
for i in full_name:
    count.append([i,data_mental[i].sum()])
data1 = pd.DataFrame(count)
data_mental.columns = data_mental.columns+'_m'
state_count = pd.DataFrame(count,columns=['state','count'])
# select the states containing more than 20000 tweets
its_state = state_count[state_count['count'] > 20000]['state'].to_list()
print(its_state)
data = pd.merge(data, data_mental, left_on='time', right_on='time_m')
data.sort_values(by='time', inplace=True)
num = list(range(0, len(data)))
data.index = num
data_policy = pd.read_excel("D:/research/COVID/text/data/lockdown_policy.xlsx")



# define a function used for ITS
def its(state,data, time, day):
    n = data[data['time'] == time].index.values[0]
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
    model_result = pd.DataFrame({f'{state}_params': model.params.to_list(), f'{state}_p': model.pvalues.to_list()})
    print(state,model.fvalue)
    print(model.summary())
    # plot the scatter
    # prepare the values for plotting
    x_data = data1['time'].to_list()
    y_data = data1['p'].to_list()
    y = np.array(y_data)
    y_before = y.copy()
    y_after = y.copy()
    y_before[day:] = None
    y_after[:day] = None
    y_pre = model.fittedvalues.values.copy()
    y_pre0 = y_pre.copy()
    y_pre0[day:] = None
    y_pre1 = y_pre.copy()
    y_pre1[:day] = None
    day_s = day * (-1)
    z = list(range(day_s, day))
# plot the scatter
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
        Line(init_opts=opts.InitOpts(width="600px", height="400px"))
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
            legend_opts=opts.LegendOpts(is_show=True,
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
                                     name_gap=35,
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
    return line, model_result

state_dic =dict(zip(data_policy['name'],data_policy['time']))
model_15 = []
model_21 = []
for state in its_state:
    data1 = data[['time',state,f'{state}_m']]
    data1['p'] = data1[f'{state}_m']/data1[state]
    time = state_dic[state]
    line1,model_result1 = its(state,data1,time,day=15)
    line1.render(f"D:/research/COVID/text/result_review/photo/ITS/{state}_15.html")
    line2,model_result2 = its(state,data1,time,day=21)
    line2.render(f"D:/research/COVID/text/result_review/photo/ITS/{state}_21.html")
    model_15.append(model_result1)
    model_21.append(model_result2)
its_15 = pd.concat(model_15,axis=1)
its_21 = pd.concat(model_21,axis=1)
its_result = pd.concat([its_15,its_21])
its_result.to_excel("D:/research/COVID/text/result_review/excel/sensitive analysis.xlsx")

# Figure 6
time = state_dic[state]
data1 = data[['time', 'Michigan', 'Michigan_m']]
data1['p'] = data1['Michigan_m']/data1['Michigan']
line1,result1 = its(data=data1, time="2020-03-24", day=15, state='Michigan')
line1.set_global_opts(title_opts=opts.TitleOpts(pos_left="21%", pos_top="47%", title='Michigan'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18)),
                      )
line1.render("D:/research/COVID/text/result_review/photo/Michigan.html")

data2 = data[['time', 'North Carolina', 'North Carolina_m']]
data2['p'] = data2['North Carolina_m']/data2['North Carolina']
line2,result2 = its(data=data2, time="2020-03-30", day=15,state='North Carolina')
line2.set_global_opts(title_opts=opts.TitleOpts(pos_left="71%", pos_top="47%", title="North Carolina"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line2.render("D:/research/COVID/text/result_review/photo/North Carolina.html")

data3 = data[['time', 'Ohio', 'Ohio_m']]
data3['p'] = data3['Ohio_m']/data3['Ohio']
line3,result3 = its(data=data3, time="2020-03-23", day=15, state='Ohio')
line3.set_global_opts(title_opts=opts.TitleOpts(pos_left="23%", pos_top="94%", title="Ohio"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line3.render("D:/research/COVID/text/result_review/photo/Ohio.html")

data4 = data[['time', 'Pennsylvania', 'Pennsylvania_m']]
data4['p'] = data4['Pennsylvania_m']/data4['Pennsylvania']
line4,result4 = its(data=data4, time="2020-04-01", day=15,state = 'Pennsylvania')
line4.set_global_opts(title_opts=opts.TitleOpts(pos_left="72%", pos_top="94%", title="Pennsylvania"),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line4.render("D:/research/COVID/text/result_review/photo/Pennsylvania.html")
grid1=(
    Grid(init_opts=opts.InitOpts(width="800px", height="500px"))
    .add(line1, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_bottom="57%", pos_top="9%"))
    .add(line2, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_bottom="57%", pos_top="9%"))
    .add(line3, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_top="57%", pos_bottom="9%"))
    .add(line4, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_top="57%", pos_bottom="9%"))
)
grid1.render("D:/research/COVID/text/result_review/photo/ITS.html")
data_result = pd.concat([result1,result2,result3,result4],axis=1)
data_result.to_excel("D:/research/COVID/text/result_review/excel/its.xlsx")

# Figure S5
def state_photo(state1):
    state = state1
    data1 = data[['time',state,f'{state}_m']]
    data1['p'] = data1[f'{state}_m']/data1[state]
    time = state_dic[state]
    line1,model_result1 = its(state,data1,time,day=15)
    return line1
line1 = state_photo('California')
line1.set_global_opts(title_opts=opts.TitleOpts(pos_left="21%", pos_top="27%", title='California'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18)),
                      )
line2 = state_photo('New York')
line2.set_global_opts(title_opts=opts.TitleOpts(pos_left="71%", pos_top="27%", title='New York'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line3 = state_photo('Texas')
line3.set_global_opts(title_opts=opts.TitleOpts(pos_left="23%", pos_top="50%", title='Texas'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line4 = state_photo('Florida')
line4.set_global_opts(title_opts=opts.TitleOpts(pos_left="72%", pos_top="50%", title='Florida'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line5 = state_photo('Illinois')
line5.set_global_opts(title_opts=opts.TitleOpts(pos_left="22%", pos_top="73%", title='Illinois'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18)),
                      )
line6 = state_photo('Washington')
line6.set_global_opts(title_opts=opts.TitleOpts(pos_left="70%", pos_top="73%", title='Washington'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line7 = state_photo('Massachusetts')
line7.set_global_opts(title_opts=opts.TitleOpts(pos_left="19%", pos_top="97%", title='Massachusetts'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
line8 = state_photo('Georgia')
line8.set_global_opts(title_opts=opts.TitleOpts(pos_left="72%", pos_top="97%", title='Georgia'),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=18))
                      )
grid2=(
    Grid(init_opts=opts.InitOpts(width="800px", height="1000px"))
    .add(line1, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_bottom="75%", pos_top="6%"))
    .add(line2, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_bottom="75%", pos_top="6%"))
    .add(line3, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_top="30%", pos_bottom="52%"))
    .add(line4, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_top="30%", pos_bottom="52%"))
    .add(line5, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_bottom="29%", pos_top="53%"))
    .add(line6, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_bottom="29%", pos_top="53%"))
    .add(line7, grid_opts=opts.GridOpts(pos_right="56%", pos_left="9%", pos_top="76%", pos_bottom="5%"))
    .add(line8, grid_opts=opts.GridOpts(pos_left="59%", pos_right="6%", pos_top="76%", pos_bottom="5%"))
)
grid2.render("D:/research/COVID/text/result_review/photo/ITS_state8.html")