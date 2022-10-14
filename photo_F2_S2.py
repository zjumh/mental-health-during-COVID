# Figure 2: Trends of four types of mental health symptoms-related tweets by number and proportion of tweets
# Figure S2: Trends of four mental health symptoms-related tweets
import pandas as pd
from _datetime import datetime,timedelta
from scipy import stats
import matplotlib.pyplot as plt
import pyecharts.options as opts
from pyecharts.charts import Line, Grid
from pyecharts.render import make_snapshot
from pyecharts.globals import ThemeType
from snapshot_phantomjs import snapshot
from pyecharts.commons.utils import JsCode

# the daily number of total tweets, mental health-related tweets
time_count = pd.read_csv("D:/research/COVID/text/result_review/data/count/time_count_all1.csv")
# the new case number in four countries
case_count = pd.read_csv("D:/research/COVID/text/data/WHO-COVID-19-global-data_new.csv")
c_list = ['Philippines','Canada','United States of America','The United Kingdom']
case_count = case_count[case_count['Country'].isin(c_list)]
def timechange(time):
    time_format = datetime.strptime(time, '%Y/%m/%d')
    end = datetime.strftime(time_format, '%Y-%m-%d')
    return end
case_count['time'] = case_count['Date_reported'].apply(lambda x:timechange(x))
case_count_new = pd.pivot(data=case_count,index='time',columns='Country',values='New_cases')
case_count_new = case_count_new.reset_index()
case_count_new['new_case'] = case_count_new['Philippines']+case_count_new['Canada']+case_count_new['United States of America']+case_count_new['The United Kingdom']
time_count = pd.merge(time_count,case_count_new[['time','new_case']],on='time')
time_count['time'] = pd.to_datetime(time_count['time'])
time_count_p = time_count.resample('7D', on='time', label='right').sum().reset_index()
time_count_p['date'] = time_count_p['time'].apply(lambda x: datetime.strftime(x+timedelta(days=-1), '%y %b %d'))
time_count_p['anxiety_p'] = time_count_p['anxiety_spam']*100/time_count_p['clean']
time_count_p['depression_p'] = time_count_p['depression_spam']*100/time_count_p['clean']
time_count_p['insomnia_p'] = time_count_p['insomnia_spam']*100/time_count_p['clean']
time_count_p['abuse_p'] = time_count_p['abuse_spam']*100/time_count_p['clean']
# remove the last column
time_count_p.drop(time_count_p.index[len(time_count_p)-1], inplace=True)

# plot the photo
# Figure S2
symbol_size = 5
text_size = 14
label_size = 12
x = list(range(0,len(time_count_p)))
y1 = time_count_p['anxiety_spam'].to_list()
y2 = time_count_p['depression_spam'].to_list()
y3 = time_count_p['insomnia_spam'].to_list()
y4 = time_count_p['abuse_spam'].to_list()
y5 = time_count_p['new_case'].to_list()
date = time_count_p['date'].to_list()
line_n = (
    Line(init_opts=opts.InitOpts(width="800px", height="400px", theme=ThemeType.INFOGRAPHIC))
        .add_xaxis(xaxis_data=x)
        .add_yaxis(
        series_name="anxiety",
        y_axis=y1,
        # is_smooth=True,
        symbol='circle',
        symbol_size=symbol_size,
        linestyle_opts=opts.LineStyleOpts(width=2),
        label_opts=opts.LabelOpts(is_show=False)
    )
        .add_yaxis(
        series_name="depression",
        y_axis=y2,
        # is_smooth=True,
        symbol='rect',
        symbol_size=symbol_size,
        linestyle_opts=opts.LineStyleOpts(width=2),
        label_opts=opts.LabelOpts(is_show=False)
    )
        .add_yaxis(
        series_name="insomnia",
        y_axis=y3,
        # is_smooth=True,
        symbol='triangle',
        symbol_size=symbol_size,
        itemstyle_opts=opts.ItemStyleOpts(color="#483D8B"),
        linestyle_opts=opts.LineStyleOpts(width=2, color="#483D8B"),
        label_opts=opts.LabelOpts(is_show=False)
    )
        .add_yaxis(
        series_name="addiction",
        y_axis=y4,
        # is_smooth=True,
        symbol='diamond',
        symbol_size=symbol_size,
        itemstyle_opts=opts.ItemStyleOpts(color="#D2691E"),
        linestyle_opts=opts.LineStyleOpts(width=2, color="#D2691E"),
        label_opts=opts.LabelOpts(is_show=False)
    )
        .add_yaxis(
        series_name="new case",
        y_axis=y5,
        # is_smooth=True,
        symbol='pin',
        yaxis_index=1,
        symbol_size=symbol_size,
        itemstyle_opts=opts.ItemStyleOpts(color="#D2691E"),
        linestyle_opts=opts.LineStyleOpts(width=2, color="#D2691E"),
        label_opts=opts.LabelOpts(is_show=False)
    )
        .extend_axis(
        yaxis=opts.AxisOpts(name="New case number",name_location="middle",name_gap=32,
        axisline_opts=opts.AxisLineOpts(is_show=True,is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#000000")),
        axistick_opts=opts.AxisTickOpts(is_inside=True),
        axislabel_opts=opts.LabelOpts(is_show=True,font_size=label_size, formatter=JsCode("function(x){return Number(x/1000000)+'M';}")),
        name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)
                            )
    )
        .add_js_funcs()
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=False),
        legend_opts=opts.LegendOpts(pos_left='12.5%', pos_top='1.5%', orient='vertical',
                                    textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        xaxis_opts=opts.AxisOpts(type_="value",
                                 boundary_gap=False,
                                 max_=120,
                                 interval=10,
                                 axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                 linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True, is_show=True),
                                 axislabel_opts=opts.LabelOpts(interval=10, rotate=90, font_size=label_size,
                                                               # 要实现的就是这个坐标的转换
                                                               formatter=JsCode(
                                                                   "function(params, item) { "
                                                                   "var date = ['20 Feb 07', '20 Feb 14', '20 Feb 21', "
                                                                   "'20 Feb 28', '20 Mar 06', '20 Mar 13', '20 Mar 20', "
                                                                   "'20 Mar 27', '20 Apr 03', '20 Apr 10', '20 Apr 17', "
                                                                   "'20 Apr 24', '20 May 01', '20 May 08', '20 May 15', "
                                                                   "'20 May 22', '20 May 29', '20 Jun 05', '20 Jun 12', "
                                                                   "'20 Jun 19', '20 Jun 26', '20 Jul 03', '20 Jul 10', "
                                                                   "'20 Jul 17', '20 Jul 24', '20 Jul 31', '20 Aug 07', "
                                                                   "'20 Aug 14', '20 Aug 21', '20 Aug 28', '20 Sep 04', "
                                                                   "'20 Sep 11', '20 Sep 18', '20 Sep 25', '20 Oct 02', "
                                                                   "'20 Oct 09', '20 Oct 16', '20 Oct 23', '20 Oct 30', "
                                                                   "'20 Nov 06', '20 Nov 13', '20 Nov 20', '20 Nov 27', "
                                                                   "'20 Dec 04', '20 Dec 11', '20 Dec 18', '20 Dec 25', "
                                                                   "'21 Jan 01', '21 Jan 08', '21 Jan 15', '21 Jan 22', "
                                                                   "'21 Jan 29', '21 Feb 05', '21 Feb 12', '21 Feb 19', "
                                                                   "'21 Feb 26', '21 Mar 05', '21 Mar 12', '21 Mar 19', "
                                                                   "'21 Mar 26', '21 Apr 02', '21 Apr 09', '21 Apr 16', "
                                                                   "'21 Apr 23', '21 Apr 30', '21 May 07', '21 May 14', "
                                                                   "'21 May 21', '21 May 28', '21 Jun 04', '21 Jun 11', "
                                                                   "'21 Jun 18', '21 Jun 25', '21 Jul 02', '21 Jul 09', "
                                                                   "'21 Jul 16', '21 Jul 23', '21 Jul 30', '21 Aug 06', "
                                                                   "'21 Aug 13', '21 Aug 20', '21 Aug 27', '21 Sep 03', "
                                                                   "'21 Sep 10', '21 Sep 17', '21 Sep 24', '21 Sep 24', "
                                                                   "'21 Oct 01', '21 Oct 08', '21 Oct 15', '21 Oct 22', "
                                                                   "'21 Oct 29', '21 Nov 05', '21 Nov 12', '21 Nov 19', "
                                                                   "'21 Nov 26', '21 Dec 03', '21 Dec 10', '21 Dec 17', "
                                                                   "'21 Dec 24', '21 Dec 31', '22 Jan 07', '22 Jan 14', "
                                                                   "'22 Jan 21', '22 Jan 28', '22 Feb 04', '22 Feb 11', "
                                                                   "'22 Feb 18', '22 Feb 25', '22 Mar 04', '22 Mar 11', "
                                                                   "'22 Mar 18', '22 Mar 25', '22 Apr 01', '22 Apr 08', "
                                                                   "'22 Apr 15', '22 Apr 22', '22 Apr 29'];"
                                                                   "console.log(params, item); return date[params];}"
                                                               )),
                                 minor_tick_opts=opts.MinorTickOpts(is_show=True, split_number=5, length=3),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        yaxis_opts=opts.AxisOpts(type_="value",
                                 name="Tweet Number",
                                 name_gap=32,
                                 name_location="middle",
                                 axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                 linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True),
                                 axislabel_opts=opts.LabelOpts(font_size=label_size,
                                                               # 这是设好的一个格式，比较简单
                                                               formatter=JsCode(
                                                                   "function(x){return Number(x/1000)+'K';}"
                                                               )),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)
                                 )

    )
)
grid1 = (Grid(init_opts=opts.InitOpts(width="800px", height="500px", theme=ThemeType.INFOGRAPHIC)).add(line_n,grid_opts=opts.GridOpts(
    pos_bottom="5%",pos_top="2.5%",pos_left="5%",pos_right="3%",is_contain_label=True),is_control_axis_index=True))
grid1.render("D:/research/COVID/text/result_review/photo/mental_n.html")

# Figure 2
y1 = time_count_p['anxiety_p'].to_list()
y2 = time_count_p['depression_p'].to_list()
y3 = time_count_p['insomnia_p'].to_list()
y4 = time_count_p['abuse_p'].to_list()


def line_photo(symptom):
    y1 = time_count_p[f'{symptom}_p'].to_list()
    line1 = (
        Line(init_opts=opts.InitOpts(width="800px", height="400px", theme=ThemeType.INFOGRAPHIC))
        .add_xaxis(xaxis_data=x)
        .add_yaxis(
            series_name='addiction',
            y_axis=y1,
            #is_smooth=True,
            symbol='circle',
            symbol_size=symbol_size,
            linestyle_opts=opts.LineStyleOpts(width=2),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=False),
            legend_opts=opts.LegendOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="value",
                                     boundary_gap=False,
                                     max_=120,
                                     interval=10,
                                     axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                     linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                     axistick_opts=opts.AxisTickOpts(is_inside=True),
                                     axislabel_opts=opts.LabelOpts(interval=10, rotate=90, font_size=label_size,
                                                                   # 要实现的就是这个坐标的转换
                                                                   formatter=JsCode(
                                                                       "function(params, item) { "
                                                                       "var date = ['20 Feb 07', '20 Feb 14', '20 Feb 21', "
                                                                       "'20 Feb 28', '20 Mar 06', '20 Mar 13', '20 Mar 20', "
                                                                       "'20 Mar 27', '20 Apr 03', '20 Apr 10', '20 Apr 17', "
                                                                       "'20 Apr 24', '20 May 01', '20 May 08', '20 May 15', "
                                                                       "'20 May 22', '20 May 29', '20 Jun 05', '20 Jun 12', "
                                                                       "'20 Jun 19', '20 Jun 26', '20 Jul 03', '20 Jul 10', "
                                                                       "'20 Jul 17', '20 Jul 24', '20 Jul 31', '20 Aug 07', "
                                                                       "'20 Aug 14', '20 Aug 21', '20 Aug 28', '20 Sep 04', "
                                                                       "'20 Sep 11', '20 Sep 18', '20 Sep 25', '20 Oct 02', "
                                                                       "'20 Oct 09', '20 Oct 16', '20 Oct 23', '20 Oct 30', "
                                                                       "'20 Nov 06', '20 Nov 13', '20 Nov 20', '20 Nov 27', "
                                                                       "'20 Dec 04', '20 Dec 11', '20 Dec 18', '20 Dec 25', "
                                                                       "'21 Jan 01', '21 Jan 08', '21 Jan 15', '21 Jan 22', "
                                                                       "'21 Jan 29', '21 Feb 05', '21 Feb 12', '21 Feb 19', "
                                                                       "'21 Feb 26', '21 Mar 05', '21 Mar 12', '21 Mar 19', "
                                                                       "'21 Mar 26', '21 Apr 02', '21 Apr 09', '21 Apr 16', "
                                                                       "'21 Apr 23', '21 Apr 30', '21 May 07', '21 May 14', "
                                                                       "'21 May 21', '21 May 28', '21 Jun 04', '21 Jun 11', "
                                                                       "'21 Jun 18', '21 Jun 25', '21 Jul 02', '21 Jul 09', "
                                                                       "'21 Jul 16', '21 Jul 23', '21 Jul 30', '21 Aug 06', "
                                                                       "'21 Aug 13', '21 Aug 20', '21 Aug 27', '21 Sep 03', "
                                                                       "'21 Sep 10', '21 Sep 17', '21 Sep 24', '21 Sep 24', "
                                                                       "'21 Oct 01', '21 Oct 08', '21 Oct 15', '21 Oct 22', "
                                                                       "'21 Oct 29', '21 Nov 05', '21 Nov 12', '21 Nov 19', "
                                                                       "'21 Nov 26', '21 Dec 03', '21 Dec 10', '21 Dec 17', "
                                                                       "'21 Dec 24', '21 Dec 31', '22 Jan 07', '22 Jan 14', "
                                                                       "'22 Jan 21', '22 Jan 28', '22 Feb 04', '22 Feb 11', "
                                                                       "'22 Feb 18', '22 Feb 25', '22 Mar 04', '22 Mar 11', "
                                                                       "'22 Mar 18', '22 Mar 25', '22 Apr 01', '22 Apr 08', "
                                                                       "'22 Apr 15', '22 Apr 22', '22 Apr 29'];"
                                                                       "console.log(params, item); return date[params];}"
                                                                   )),
                                    minor_tick_opts=opts.MinorTickOpts(is_show=True, split_number=5, length=3),
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
            yaxis_opts=opts.AxisOpts(type_="value",
                                     name="Proportion/%",
                                     name_gap=32,
                                     name_location="middle",
                                     axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                     linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                     axistick_opts=opts.AxisTickOpts(is_inside=True),
                                     axislabel_opts=opts.LabelOpts(font_size=label_size),
                                     name_textstyle_opts=opts.TextStyleOpts(font_size=text_size))

        )
    )
    line1.render(f"D:/research/COVID/text/result_review/photo/{symptom}_p.html")
    return line1


line1 = line_photo('anxiety')
line1.set_global_opts(legend_opts=opts.LegendOpts(pos_left="8%", pos_top='top',textstyle_opts=opts.TextStyleOpts(font_size=16)))
line2 = line_photo('depression')
line2.set_global_opts(legend_opts=opts.LegendOpts(pos_left="30%", pos_top='top',textstyle_opts=opts.TextStyleOpts(font_size=16)))
line3 = line_photo('insomnia')
line3.set_global_opts(legend_opts=opts.LegendOpts(pos_left="53%", pos_top='top',textstyle_opts=opts.TextStyleOpts(font_size=16)))
line4 = line_photo('abuse')
line4.set_global_opts(legend_opts=opts.LegendOpts(pos_left="73%", pos_top='top',textstyle_opts=opts.TextStyleOpts(font_size=16)))
grid=(
    Grid(init_opts=opts.InitOpts(width="800px", height="500px"))
    .add(line1, grid_opts=opts.GridOpts(pos_right="53%", pos_left="9%", pos_bottom="61%", pos_top="6%"))
    .add(line2, grid_opts=opts.GridOpts(pos_left="56%", pos_right="6%", pos_bottom="61%", pos_top="6%"))
    .add(line3, grid_opts=opts.GridOpts(pos_right="53%", pos_left="9%", pos_top="53%", pos_bottom="14%"))
    .add(line4, grid_opts=opts.GridOpts(pos_left="56%", pos_right="6%", pos_top="53%", pos_bottom="14%"))
)
grid.render("D:/research/COVID/text/result_review/photo/mental_p.html")