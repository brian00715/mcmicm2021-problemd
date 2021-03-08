import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType

data_by_year_path = r'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\data_by_year.csv'
data_by_year_var_path = r'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\data_by_year_variation.csv'
full_music_data_path = r'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\full_music_data.csv'

def get_character_by_year_line(data_by_year_path):
    character_by_year_frame = pd.read_csv(data_by_year_path)
    x_data = character_by_year_frame['year'].to_list()
    for i in range(len(x_data)):
        x_data[i] = str(x_data[i])
    character_by_year_frame = (character_by_year_frame - character_by_year_frame.min()) / (
            character_by_year_frame.max() - character_by_year_frame.min())
    #------作图部分
    column_name = []
    y_data = []
    for i in range(1, 14):
        column_name.append(character_by_year_frame.columns[i])
        y_data.append(pd.Series(character_by_year_frame.iloc[:, i]).to_list())
    line_graph = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    line_graph.add_xaxis(xaxis_data=x_data)
    for i in range(7):
        if i == 5:
            continue
        line_graph.add_yaxis(
            series_name=column_name[i],
            y_axis=y_data[i],
            is_smooth=True,
            # stack="数值",
            label_opts=opts.LabelOpts(is_show=False),
        )
    line_graph.set_global_opts(
        title_opts=opts.TitleOpts(),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            name='0-1 Normalized Value',
            name_location='middle',
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),
            name_gap=40,
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=1)
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            min_=0,
            # max_=1.2,
        ),
        xaxis_opts=opts.AxisOpts(
            name='Year', boundary_gap=False, is_show=True, name_location='middle', name_gap=40,
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),
        ),
        legend_opts=opts.LegendOpts(
            legend_icon='rect',
            pos_top=12,
            # orient='vertical',
            # align='left',
        ))
    line_graph.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=2))
    line_graph.render("htmls\\character_by_year_line_chart.html")

def get_character_var_by_year_line(path):
    """找到革命性的音乐家"""
    # 画特征变化量的图
    data_by_year_var_frame = pd.read_csv(path)
    x_data = data_by_year_var_frame['year'].to_list()
    for i in range(len(x_data)):
        x_data[i] = str(x_data[i])
    # ------作图部分
    column_name = []
    y_data = []
    for i in range(1, 14):
        column_name.append(data_by_year_var_frame.columns[i])
        y_data.append(pd.Series(data_by_year_var_frame.iloc[:, i]).to_list())
    line_graph = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    line_graph.add_xaxis(xaxis_data=x_data)
    for i in range(0,7):
        if i == 5: # 去除mode
            continue
        line_graph.add_yaxis(
            series_name=column_name[i],
            y_axis=y_data[i],
            is_smooth=True,
            # stack="数值",
            label_opts=opts.LabelOpts(is_show=False),
        )
    line_graph.set_global_opts(
        title_opts=opts.TitleOpts(),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        yaxis_opts=opts.AxisOpts(
            name='0-1 Normalized Value',
            name_location='middle',
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),
            name_gap=40,
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=1)
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(
            name='Year', boundary_gap=False, is_show=True, name_location='middle', name_gap=40,
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),
        ),
        legend_opts=opts.LegendOpts(
            legend_icon='rect',
            pos_top=12,
        ))
    line_graph.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=2))
    line_graph.render("htmls\\character_by_year_var_line_chart.html")



if __name__ == '__main__':
    # 1. 画出指标随时间变化的折线图
    get_character_by_year_line(data_by_year_path)

    # 2. 画出指标变化量折线图
    get_character_var_by_year_line(data_by_year_var_path)

    # 3.统计艺术家音乐指标的变化
    # full_music_data = pd.read_csv(full_music_data_path)
    special_year = [1946,1950,1961,1967,2017]

