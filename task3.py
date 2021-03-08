import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Radar, Line, Bar, HeatMap, Bar3D
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType


def get_genre_radar(csv_file_path1, csv_file_path2):
    genre_data_frame = pd.read_csv(csv_file_path1).iloc[:, 4:]  # 流派内艺术家的音乐特征
    # del genre_data_frame['popularity']
    print(genre_data_frame)
    std_data = (genre_data_frame - genre_data_frame.min()) / (genre_data_frame.max() - genre_data_frame.min())  # 标准化
    mean_data = std_data.mean(0)
    for i in range(len(mean_data)):
        mean_data[i] = round(mean_data[i], 3) # 保留三位小数
    data1 = [{"value": mean_data.to_list()}]
    genre_data_frame = pd.read_csv(csv_file_path2).iloc[:, 4:]  # 流派内艺术家的音乐特征
    std_data = (genre_data_frame - genre_data_frame.min()) / (genre_data_frame.max() - genre_data_frame.min())  # 标准化
    mean_data = std_data.mean(0)
    for i in range(len(mean_data)):
        mean_data[i] = round(mean_data[i], 3)
    data2 = [{"value": mean_data.to_list()}]
    c_schema = [
        {"name": "danceability", "max": 1, "min": 0},
        {"name": "energy", "max": 1, "min": 0},
        {"name": "valence", "max": 1, "min": 0},
        {"name": "tempo", "max": 1, "min": 0},
        {"name": "loudness", "max": 1, "min": 0},
        {"name": "mode", "max": 1, "min": 0},
        {"name": "key", "max": 1, "min": 0},
        {"name": "acousticness", "max": 1, "min": 0},
        {"name": "instrumentalness", "max": 1, "min": 0},
        {"name": "liveness", "max": 1, "min": 0},
        {"name": 'speechiness', "max": 1, "min": 0},
        {"name": "duration", "max": 1, "min": 0},
        {"name": "popularity", "max": 1, "min": 0},
        {"name": "count", "max": 1, "min": 0},
    ]
    bg_color1 = ("new echarts.graphic.LinearGradient(0, 0, 0, 1, "
                "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)")
    bg_color2= ("new echarts.graphic.LinearGradient(0, 0, 0, 1, "
                 "[{offset: 0, color: '#6453DB'}, {offset: 1, color: '#61FFE4'}], false)")
    c = (
        Radar(init_opts=opts.InitOpts(theme=ThemeType.WHITE))
            # .set_colors(["#F26881",'#7AC0D6'])
            .add_schema(
            schema=c_schema,
            shape="circle",
            center=["50%", "50%"],
            radius="80%",
            angleaxis_opts=opts.AngleAxisOpts(  # 角度轴设置
                min_=0,
                max_=360,
                is_clockwise=False,
                interval=5,
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            radiusaxis_opts=opts.RadiusAxisOpts(  # 半径轴设置
                min_=0,
                max_=1,
                interval=0.2,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1,)
                ),

            ),
            polar_opts=opts.PolarOpts(),
            splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts()),
            splitline_opt=opts.SplitLineOpts(is_show=True),
            textstyle_opts=opts.TextStyleOpts(color='#000000')
        )
            .add(
            series_name="Stage & Screen",
            data=data1,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.8,color="#F26881"),
            linestyle_opts=opts.LineStyleOpts(width=1,color="#F26881" ),
            label_opts=opts.LabelOpts(is_show=False,color='#cccccc')
        )
            .add(
            series_name="Classical",
            data=data2,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.8, color="#DCBFDE"),# DCBFDE 80CAE0
            linestyle_opts=opts.LineStyleOpts(width=1,color="#DCBFDE" ), # DCBFDE
            label_opts=opts.LabelOpts(is_show=False,color='#cccccc'),
            color="#DCBFDE"
        )
            .render("Stage & Screen_Classical_music_character_radar.html")
    )


def get_genre_line(genre_name):
    genre_name = genre_name.replace("/", '_')
    data_by_grene = pd.read_csv('E:\\MCM&ICM2021\\programs\\data_by_genre\\' + genre_name + '_artist_data.csv')
    last_year = data_by_grene.iloc[0, 3]
    mean_value_dic = {}  # {’year‘:[mean1,mean2,...]}
    start_index = 0
    for row_index, row in data_by_grene.iterrows():
        # if row_index == 0:
        #     continue
        year = data_by_grene.iloc[row_index, 3]
        if year != last_year:
            temp = data_by_grene.iloc[start_index:row_index, 4:]
            # print(temp)
            start_index = row_index
            temp = temp.mean(0)
            mean_value_dic[last_year] = temp.to_list()
            last_year = year
    export_data_frame = pd.DataFrame().from_dict(mean_value_dic)
    export_data_frame = export_data_frame.T
    # print(export_data_frame)
    export_data_frame = (export_data_frame - export_data_frame.min()) / (
            export_data_frame.max() - export_data_frame.min())
    # print(export_data_frame)
    export_data_frame = export_data_frame.T
    # print(export_data_frame)
    mean_value_list = []
    for i in range(14):
        mean_value_list.append(export_data_frame.iloc[i, :].to_list())
    print(mean_value_list)
    # export_data_frame.to_csv(genre_name+'_mean_by_year.csv')
    column_name = []
    for i in range(4, 18):
        column_name.append(data_by_grene.columns[i])
    x_data = []
    for key, values in mean_value_dic.items():
        x_data.append(str(key))

    line_graph = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    line_graph.add_xaxis(xaxis_data=x_data[2:])  # 从1950开始
    for i in range(8, 14):
        line_graph.add_yaxis(
            series_name=column_name[i],
            y_axis=mean_value_list[i][2:],
            is_smooth=True,
            # stack="总量",
            label_opts=opts.LabelOpts(is_show=False),
        )
    line_graph.set_global_opts(
        title_opts=opts.TitleOpts(title=genre_name.replace('_', '/'), subtitle='Vocals and Description'),
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
            max_=1.2,
        ),
        xaxis_opts=opts.AxisOpts(
            name='Year', boundary_gap=False, is_show=True, name_location='middle', name_gap=40,
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),
        ),
        legend_opts=opts.LegendOpts(
            # type_='scroll',
            legend_icon='rect',
            pos_top=12,
            # orient='vertical',
            # align='left',
        )
    )
    line_graph.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=2))
    line_graph.render(genre_name + "_character_line_chart.html")

def get_genre_member_bar():
    gnere_by_year_data = pd.read_csv('genre_by_year.csv')
    # choose_genre = ['Jazz', 'Country', 'R&B;', 'Electronic', 'Reggae', 'Blues', 'Vocal']
    choose_genre = gnere_by_year_data.columns[1:].to_list()
    # del choose_genre[13]
    print(choose_genre)
    x_data = gnere_by_year_data['year'].to_list()
    y_data = []
    bar_graph = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)).add_xaxis(x_data)
    for i in range(len(choose_genre)):
        bar_graph.add_yaxis(
            series_name=choose_genre[i],
            y_axis=gnere_by_year_data[choose_genre[i]].to_list(),
            stack="人数",
            bar_width=45,
            label_opts=opts.LabelOpts(is_show=False),
        )
    bar_graph.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar_graph.set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        xaxis_opts=opts.AxisOpts(
            name='Year', boundary_gap=True, is_show=True, name_location='middle', name_gap=40,
            name_textstyle_opts=opts.TextStyleOpts(font_size=16),
        ),
        yaxis_opts=opts.AxisOpts(name='Number of Artists', name_gap=40,
                                 name_textstyle_opts=opts.TextStyleOpts(font_size=16), name_location='middle')
    )
    bar_graph.render("genre_member_bar_stack.html")

def get_gnere_cos_sim_heatmap_bar3d():
    cos_sim_value_bwt_gnere_data = pd.read_csv('cos_similarity_between_each_genre.csv')
    gnere_name = cos_sim_value_bwt_gnere_data.columns.to_list()[1:]
    pure_data = cos_sim_value_bwt_gnere_data.iloc[:, 1:]
    value = []  # 构造填充数据
    for row_index, row in pure_data.iterrows():
        for i in range(len(row)):
            value.append([i, row_index, round(pure_data.iloc[row_index, i], 2)])
    c = (
        HeatMap(init_opts=opts.InitOpts())
            .add_xaxis(gnere_name)
            .add_yaxis(
            "series0",
            gnere_name,
            value,
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="HeatMap-Label 显示"),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False, max_=0.65, min_=-0.3, pos_left='right', pos_top='center',
                range_text=['Cosine Similarity', ''],
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30))
        )
            .render("cos_sim_value_btw_genre_heatmap.html")
    )
    for i in range(len(value)):
        for j in range(len(value[i])):
            if value[i][j] == 1:
                value[i][j] = 0
    (
        Bar3D()
            .add(
            series_name="",
            data=value,
            xaxis3d_opts=opts.Axis3DOpts(type_="category", data=gnere_name, interval=0.5),
            yaxis3d_opts=opts.Axis3DOpts(type_="category", data=gnere_name),
            zaxis3d_opts=opts.Axis3DOpts(type_="value", max_=1, min_=-0.5),
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                pos_left='right',
                max_=1,
                min_=-1,
                range_text=['Cosine Similarity', ''],
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            ),
        )
            .render("cos_sim_value_btw_genre_3dbar.html")
    )

if __name__ == '__main__':
    # 1. 绘制某流派艺术家音乐特征平均值的雷达图,用以在流派之间对比音乐特征的差异
    # get_genre_radar(r'E:\MCM&ICM2021\programs\data_by_genre\Stage & Screen_artist_data.csv',
    #                 r'E:\MCM&ICM2021\programs\data_by_genre\Classical_artist_data.csv')

    # 2. 获得不同时间内流派人数变化情况的堆叠柱状图
    get_genre_member_bar()

    # 3. 获得不同时间内某个流派各项指标的变化,画重叠折线图
    # get_genre_line('Pop/Rock')

    # 4. 绘制流派之间音乐特征相似性的热力图/3D柱状图
    # get_gnere_cos_sim_heatmap_bar3d()
