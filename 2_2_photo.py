#plot the line
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
#read the csv
df_total = pd.read_csv("D:\\research\COVID\\text\\result\count\\total_count.csv")
df_clean = pd.read_csv("D:\\research\COVID\\text\\result\count\clean_count.csv")
df_case = pd.read_csv("D:\\research\COVID\\text\\result\count\\newcase.csv")
df_mental = pd.read_csv("D:\\research\COVID\\text\\result\count\mental_4count.csv")
df_m = pd.read_csv("D:\\research\COVID\\text\\result\count\M_count17.csv")
df_p = pd.read_csv("D:\\research\COVID\\text\\result\count\P_count17.csv")
df_Mmental = pd.read_csv("D:\\research\COVID\\text\\result\count\mental_Mcount.csv")
df_Pmental = pd.read_csv("D:\\research\COVID\\text\\result\count\mental_Pcount.csv")
df_pclean = pd.read_csv("D:\\research\COVID\\text\\result\count\hc_count.csv")
df_mclean = pd.read_csv("D:\\research\COVID\\text\\result\count\gp_count.csv")
#rename the colname
df_total.columns = ['date', 'total']
df_clean.columns = ['date', 'clean']
df_mental.columns = ['date', 'anxiety', 'depression', 'insomnia', 'abuse']
df_m.columns = ['date', 'm']
df_p.columns = ['date', 'p']
df_Mmental.columns = ['date', 'Manxiety', 'Mdepression', 'Minsomnia', 'Mabuse']
df_Pmental.columns = ['date', 'Panxiety', 'Pdepression', 'Pinsomnia', 'Pabuse']
df_mclean.columns = ['date', 'mclean']
df_pclean.columns = ['date', 'pclean']
#process the case data
df_case['case'] = df_case['Canada']+df_case['Philippines']+df_case['UK']+df_case['USA']
df_case = df_case[['Date_reported', 'case']]
df_case.columns = ['date', 'case']
#merge the df
data1 = pd.merge(df_total, df_clean, how='outer', on='date')
data2 = pd.merge(data1, df_mental, how='outer', on='date')
data3 = pd.merge(df_m, df_p, how='outer', on='date')
data4 = pd.merge(df_Mmental, df_Pmental, how='outer', on='date')
data5 = pd.merge(data3, data4, how='outer', on='date')
data6 = pd.merge(data2, data5, how='outer', on='date')
data7 = pd.merge(data6, df_case, how='outer', on='date')
data8 = pd.merge(df_mclean,df_pclean,how='outer', on='date')
data9 = pd.merge(data7, data8, how='outer', on='date')
data9['time'] = pd.to_datetime(data9['date'])
#count the total number weekly
data = data9.resample('7D', on='time', label='right').sum()
#count the percent of mental
data['anxiety_p'] = round(data['anxiety']/data['clean']*100, 3)
data['depression_p'] = round(data['depression']/data['clean']*100, 3)
data['insomnia_p'] = round(data['insomnia']/data['clean']*100, 3)
data['abuse_p'] = round(data['abuse']/data['clean']*100, 3)
data['Manxiety_p'] = round(data['Manxiety']/data['mclean']*100, 4)
data['Mdepression_p'] = round(data['Mdepression']/data['mclean']*100, 4)
data['Minsomnia_p'] = round(data['Minsomnia']/data['mclean']*100, 4)
data['Mabuse_p'] = round(data['Mabuse']/data['mclean']*100, 4)
data['Panxiety_p'] = round(data['Panxiety']/data['pclean']*100, 3)
data['Pdepression_p'] = round(data['Pdepression']/data['pclean']*100, 3)
data['Pinsomnia_p'] = round(data['Pinsomnia']/data['pclean']*100, 3)
data['Pabuse_p'] = round(data['Pabuse']/data['pclean']*100, 3)
data['time'] = data.index
data['date'] = data['time'].apply(lambda x: datetime.datetime.strftime(x, '%Y/%m/%d'))
data.to_csv("D:\\research\COVID\\text\\result\count\\count7D1.csv",index=False)
#because the data in the last row contained less than 7 days, so we need to remove it
data = pd.read_csv("D:\\research\COVID\\text\\result\count\\count7D1.csv")
data['time'] = pd.to_datetime(data['time'])
data['date'] = data['time'].apply(lambda x: datetime.strftime(x+timedelta(days=-1), '%y %b %d'))
data.drop(data.index[len(data)-1], inplace=True)
data['num'] = data.index
symbol_size = 8
text_size = 28
label_size = 26
#line1: the trend of mental health tweets
x = data['num'].to_list()
y1 = data['anxiety'].to_list()
y2 = data['depression'].to_list()
y3 = data['insomnia'].to_list()
y4 = data['abuse'].to_list()
date = data['date'].to_list()
line1 = (
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
        .add_js_funcs()
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=False),
        legend_opts=opts.LegendOpts(pos_left='12.5%', pos_top='1.5%', orient='vertical',
                                    textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        xaxis_opts=opts.AxisOpts(type_="value",
                                 boundary_gap=False,
                                 max_=90,
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
                                                                   "'21 Sep 10', '21 Sep 17', '21 Sep 24'];"
                                                                   "console.log(params, item); return date[params];}"
                                                               )),
                                 minor_tick_opts=opts.MinorTickOpts(is_show=True, split_number=5, length=3),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        yaxis_opts=opts.AxisOpts(type_="value",
                                 name="Number",
                                 name_gap=55,
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
grid1 = (Grid(init_opts=opts.InitOpts(width="800px", height="600px", theme=ThemeType.INFOGRAPHIC)).add(line1,grid_opts=opts.GridOpts(
    pos_bottom="5%",pos_top="2.5%",pos_left="5%",pos_right="3%",is_contain_label=True),is_control_axis_index=True))
grid1.render("D:\\research\COVID\\text\photo\mental_n.html")

##line2: the trend of mental health related tweets proportion
y1 = data['anxiety_p'].to_list()
y2 = data['depression_p'].to_list()
y3 = data['insomnia_p'].to_list()
y4 = data['abuse_p'].to_list()
line2 = (
    Line(init_opts=opts.InitOpts(width="800px", height="400px", theme=ThemeType.INFOGRAPHIC))
    .add_xaxis(xaxis_data=x)
    .add_yaxis(
        series_name="anxiety",
        y_axis=y1,
        #is_smooth=True,
        symbol='circle',
        symbol_size=symbol_size,
        linestyle_opts=opts.LineStyleOpts(width=2),
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        series_name="depression",
        y_axis=y2,
        #is_smooth=True,
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
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=False),
        legend_opts=opts.LegendOpts(pos_right='7%', pos_top='3%', orient='vertical', textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        xaxis_opts=opts.AxisOpts(type_="value",
                                 boundary_gap=False,
                                 max_=90,
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
                                                                   "'21 Sep 10', '21 Sep 17', '21 Sep 24'];"
                                                                   "console.log(params, item); return date[params];}"
                                                               )),
                                 minor_tick_opts=opts.MinorTickOpts(is_show=True, split_number=5, length=3),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        yaxis_opts=opts.AxisOpts(type_="value",
                                 name="Proportion/%",
                                 name_gap=41,
                                 name_location="middle",
                                 axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                 linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True),
                                 axislabel_opts=opts.LabelOpts(font_size=label_size),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size))

    )
)
grid2 = (Grid(init_opts=opts.InitOpts(width="800px", height="600px", theme=ThemeType.INFOGRAPHIC)).add(line2, grid_opts=opts.GridOpts(pos_bottom="2%", pos_top="2.5%", pos_left="5%", pos_right="2%", is_contain_label=True), is_control_axis_index=True))
grid2.render("D:\\research\COVID\\text\\photo\\mental_p.html")
##line3: the trend of insomnia related tweets proportion
text_size=18
label_size=16
line3 = (
    Line(init_opts=opts.InitOpts(width="800px", height="400px", theme=ThemeType.INFOGRAPHIC))
    .add_xaxis(xaxis_data=date)
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
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=False),
        legend_opts=opts.LegendOpts(pos_right='5%', pos_top='3%', orient='vertical', textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        xaxis_opts=opts.AxisOpts(type_="category",
                                 boundary_gap=False,
                                 axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                 linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True),
                                 axislabel_opts=opts.LabelOpts(interval=3, rotate=90, font_size=label_size),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size)),
        yaxis_opts=opts.AxisOpts(type_="value",
                                 name="proportion/%",
                                 name_gap=50,
                                 name_location="middle",
                                 axisline_opts=opts.AxisLineOpts(is_show=True,
                                                                 linestyle_opts=opts.LineStyleOpts(color="#000000")),
                                 axistick_opts=opts.AxisTickOpts(is_inside=True),
                                 axislabel_opts=opts.LabelOpts(font_size=label_size),
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=text_size))

    )
)
grid3 = (Grid(init_opts=opts.InitOpts(width="800px", height="450px", theme=ThemeType.INFOGRAPHIC)).add(line3, grid_opts=opts.GridOpts(pos_bottom="2%", pos_top="2.5%", pos_left="5%", pos_right="2%", is_contain_label=True), is_control_axis_index=True))
grid3.render("D:\\research\COVID\\text\\photo\\mental_insomnia_p.html")