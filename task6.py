import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line, Graph, HeatMap
from pyecharts.globals import ThemeType

from programs.task1_relationship_network import name_not_in_nodes, search_all_nodes_in_list

data_by_year_path = r'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\data_by_year.csv'
full_music_data_path = r'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\full_music_data.csv'
electronic_full_data_path = r'.\full_music_data_by_genre\Electronic_average.csv'
electronic_artist_data_path = r'E:\MCM&ICM2021\programs\data_by_genre\Electronic_artist_data.csv'


def get_genre_change_line_graph(genre_name):
    path = '.\\full_music_data_by_genre\\' + genre_name + '_average.csv'
    # -------------数据处理部分
    character_by_year_frame = pd.read_csv(path)
    del character_by_year_frame['explicit']
    x_data = character_by_year_frame['year'].to_list()
    for i in range(len(x_data)):
        x_data[i] = str(x_data[i])
    column_name = []
    for i in range(13):
        column_name.append(character_by_year_frame.columns[i])
    character_by_year_frame = character_by_year_frame.iloc[:, :13]
    character_by_year_frame = (character_by_year_frame - character_by_year_frame.min()) / (
            character_by_year_frame.max() - character_by_year_frame.min())
    # -------------作图部分
    y_data = []
    for i in range(13):
        y_data.append(pd.Series(character_by_year_frame.iloc[:, i]).to_list())
    # print(len(y_data[0]))
    line_graph = Line(init_opts=opts.InitOpts(theme=ThemeType.INFOGRAPHIC))
    line_graph.add_xaxis(xaxis_data=x_data)
    for i in range(7, 13):
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
            axisline_opts=opts.AxisLineOpts(is_show=True,
                                            linestyle_opts=opts.LineStyleOpts()
                                            ),
            splitline_opts=opts.SplitLineOpts(is_show=True),
            min_=0,
            # max_=1.2,
        ),
        xaxis_opts=opts.AxisOpts(
            name='Year', boundary_gap=False, is_show=True, name_location='middle', name_gap=40,
            name_textstyle_opts=opts.TextStyleOpts(font_size=16, color='#000000'),
            axisline_opts=opts.LineStyleOpts(color='#000000')
        ),
        legend_opts=opts.LegendOpts(
            legend_icon='rect',
            pos_top=12,
        ))
    line_graph.set_series_opts(linestyle_opts=opts.LineStyleOpts(width=2))
    line_graph.render("electronic_by_year_line.html")


def get_electrolic_network(influence_data_frame, influencer_list, follower_list):
    all_influencer_name = influence_data_frame['influencer_name'].to_list()
    categories = []
    nodes = []
    links = []
    for i in range(len(influencer_list)):
        if name_not_in_nodes(nodes, influencer_list[i]):
            all_index = search_all_nodes_in_list(all_influencer_name, influencer_list[i])
            follower_of_this_influencer = 0
            for index in all_index:
                if influence_data_frame['follower_name'][index] in follower_list:
                    follower_of_this_influencer += 1
                    # print(influence_data_frame['follower_name'][index])
                    links.append(
                        {
                            "source": influencer_list[i],
                            "target": influence_data_frame['follower_name'][index],
                            # "value": influencer_node_size,
                            "symbol": ['none', 'arrow'],
                            "symbolSize": 3

                        })
                    if name_not_in_nodes(nodes, influence_data_frame['follower_name'][index]):
                        nodes.append(
                            {
                                "name": influence_data_frame['follower_name'][index],
                                "draggable": False,
                                "symbolSize": 3,
                                "value": 0,
                                "category": influencer_list[i],
                            }
                        )
            nodes.append(
                {
                    "name": influencer_list[i],
                    "draggable": True,
                    "symbolSize": follower_of_this_influencer + 2,
                    "value": 0,
                    "category": influencer_list[i],
                }
            )
            categories.append(
                {
                    "name": influencer_list[i],
                }
            )
    # for i in range(len(nodes)):
    #     print(nodes[i]['name'])
    # print(links)
    (
        Graph(init_opts=opts.InitOpts(width="1000px", height='600px'))
            .add(
            "",
            nodes,
            links,
            categories,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(color='source', curve=0.2, width=1, opacity=0.7),
            label_opts=opts.LabelOpts(is_show=True, font_weight=0.05, border_width=0.05),
            is_rotate_label=True,
            # is_roam=True,
            # is_focusnode=True,
            layout='circular',
            # linestyle_opts=opts.LineStyleOpts(color="source", curve=0.1),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            # legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
            title_opts=opts.TitleOpts(title="Graph-关系图"),

        )
            .render("electronic_relationship_network.html")
    )

def compare_influencer_follower_each_indicator(influence_data_frame,electronic_data_frame,indicator_name):
    all_influencer_name = influence_data_frame['influencer_name'].to_list()
    all_follower_name = influence_data_frame['follower_name'].to_list()

    all_artist_list = electronic_data_frame['artist_names'].to_list()  # full_music_data中的eletronic流派的艺术家
    influencer_list = []
    follower_list = []
    # 找影响者和追随者
    for i in range(len(all_artist_list)):
        all_artist_list[i] = all_artist_list[i][2:-2]  # 字符串切片
        if all_artist_list[i] in all_influencer_name and all_artist_list[i] not in influencer_list:
            influencer_list.append(all_artist_list[i])
        if all_artist_list[i] in all_follower_name and all_artist_list[i] not in follower_list:
            follower_list.append(all_artist_list[i])

    # 画出影响者和追随者的关系图
    # get_electrolic_network(influence_data_frame,influencer_list,follower_list)

    # 影响者对追随者音乐指标的影响，作折线图
    mean_music_indicator = [0.436632933, 0.287731911, 0.378874751, 107.4108681, -19.85367205, 0.818181818, 5.272727273,
                            0.683017848, 0.503862481, 0.135397013, 0.056912944, 363882.5623, 37.57792467, 43.72727273
                            ]
    # 分别得到影响者和追随者的音乐指标
    influencer_data = []  # 索引与influencer_list相对应
    follower_data = []
    all_artist_data = []
    for i in range(len(all_artist_list)):
        if all_artist_list[i] in influencer_list:
            influencer_data.append(pd.Series(electronic_data_frame.iloc[i, 2:-3]).to_list())
        else:
            influencer_data.append(np.zeros(14).tolist())  # 添加空数组，用来和完整数据对齐
        if all_artist_list[i] in follower_list:
            follower_data.append(pd.Series(electronic_data_frame.iloc[i, 2:-3]).to_list())
        else:
            follower_data.append(np.zeros(14).tolist())
        all_artist_data.append(pd.Series(electronic_data_frame.iloc[i, 2:-3]).to_list())
    all_artist_data = np.array(all_artist_data)
    influencer_data = np.array(influencer_data)
    follower_data = np.array(follower_data)  # 对齐后follower_data和influencer_data是同维度的
    influencer_mean_data_by_year = []  # 随年代变化的均值
    follower_mean_data_by_year = []
    all_artist_mean_data_by_year = []
    year_list = electronic_data_frame['year'].to_list()
    # export_data_frame = pd.DataFrame(all_artist_data)
    # export_data_frame['year'] = year_list
    # export_data_frame.to_csv('.\\electronic\\all_artist_data.csv')

    # 找到影响者对应的年份，用索引筛选数据.由于已经对其数据，因此可以用索引找到年份.
    # 得到本年度内所有影响者和追随者指标的平均值
    # print('*'*20)
    # print(follower_data)
    last_year = year_list[0]
    for i in range(len(follower_data)):
        this_year = year_list[i]
        if this_year != last_year:  # 年份不同了，计算平均值
            influencer_mean_data = 0
            all_artist_this_year_data = all_artist_data[year_list.index(last_year):i - 1]

            if year_list.index(last_year) != i - 1:
                influencer_this_year_data = influencer_data[year_list.index(last_year):i - 1]
                follower_this_year_data = follower_data[year_list.index(last_year):i - 1]
                all_artist_this_year_data = all_artist_data[year_list.index(last_year):i - 1]
                all_artist_mean_data = all_artist_this_year_data.mean(0)
                influencer_mean_data = influencer_this_year_data.mean(0)  # 列向量的平均值
                follower_mean_data = follower_this_year_data.mean(0)
            else:  # last_year就是去年，即一年只有一组数据
                influencer_mean_data = influencer_data[i]
                follower_mean_data = follower_data[i]
                all_artist_mean_data = all_artist_data[i]
            if influencer_mean_data.sum() == 0:  # 用nan替换0值，这样画图才正常
                # mean_data = np.zeros(14)
                influencer_mean_data = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                                        np.nan, np.nan, np.nan, np.nan, ]
            if follower_mean_data.sum() == 0:
                follower_mean_data = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                                      np.nan, np.nan, np.nan, np.nan, ]
            influencer_mean_data_by_year.append(influencer_mean_data)
            follower_mean_data_by_year.append(follower_mean_data)
            all_artist_mean_data_by_year.append(all_artist_mean_data)
            last_year = this_year
    influencer_mean_data_by_year = np.array(influencer_mean_data_by_year)
    influencer_mean_data_by_year = influencer_mean_data_by_year.T
    follower_mean_data_by_year = np.array(follower_mean_data_by_year)
    follower_mean_data_by_year = follower_mean_data_by_year.T
    all_artist_mean_data_by_year = np.array(all_artist_mean_data_by_year)
    all_artist_mean_data_by_year = all_artist_mean_data_by_year.T
    # for i in range(len(influencer_mean_data_by_year)):
    #     print(influencer_mean_data_by_year)

    # ---------------画图
    # indicator_name = 'liveness'  # >>>>>>要画的指标名<<<<<<<

    column_name = electronic_data_frame.columns[2:-4].to_list()
    data_index = column_name.index(indicator_name)
    x_data = electronic_data_frame['year'].drop_duplicates().to_list()
    for i in range(len(x_data)):
        x_data[i] = str(x_data[i])
    influencer_y_data = influencer_mean_data_by_year[data_index]
    follower_y_data = follower_mean_data_by_year[data_index]
    # print(all_artist_mean_data_by_year)
    line_graph = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    line_graph.add_xaxis(xaxis_data=x_data)
    line_graph.add_yaxis(
        series_name='Average of This Genre',
        y_axis=all_artist_mean_data_by_year[data_index],
        is_smooth=True,
        # stack="数值",
        label_opts=opts.LabelOpts(is_show=False),
        is_connect_nones=True,
    )
    line_graph.add_yaxis(
        series_name='Influencer',
        y_axis=influencer_y_data,
        is_smooth=True,
        # stack="数值",
        label_opts=opts.LabelOpts(is_show=False),
        is_connect_nones=True,
    ),
    line_graph.add_yaxis(
        series_name='Follower',
        y_axis=follower_y_data,
        is_smooth=True,
        # stack="数值",
        label_opts=opts.LabelOpts(is_show=False),
        is_connect_nones=True
    )

    line_graph.set_global_opts(
        title_opts=opts.TitleOpts(title=indicator_name),
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
            # min_=0,
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
    line_graph.render('htmls\\electronic\\influencer vs. follower\\' + indicator_name + '_by_year_line_chart.html')


def get_pearson_corr_heatmap(electronic_data_frame):
    electronic_data_frame = electronic_data_frame.iloc[:,2:-4]
    # print(electronic_data_frame)
    pearson_corr = electronic_data_frame.corr('spearman')
    pearson_corr = pearson_corr.reset_index(drop=True)
    gnere_name = electronic_data_frame.columns.to_list()
    pure_data = pearson_corr
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
                is_show=False, max_=0.8, min_=-0.5, pos_left='right', pos_top='center',
                range_text=['Pearson Correlation Coefficient', ''],
                range_color=['#1C64A6','#C6D8EB','#C7A8A5','#C41C14',]
            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30))
        )
            .render(".\\electronic\\pearson_corr_heatmap.html")
    )
    # for i in range(len(value)):
    #     for j in range(len(value[i])):
    #         if value[i][j] == 1:
    #             value[i][j] = 0
    # (
    #     Bar3D()
    #         .add(
    #         series_name="",
    #         data=value,
    #         xaxis3d_opts=opts.Axis3DOpts(type_="category", data=gnere_name, interval=0.5),
    #         yaxis3d_opts=opts.Axis3DOpts(type_="category", data=gnere_name),
    #         zaxis3d_opts=opts.Axis3DOpts(type_="value", max_=1, min_=-0.5),
    #     )
    #         .set_global_opts(
    #         visualmap_opts=opts.VisualMapOpts(
    #             pos_left='right',
    #             max_=1,
    #             min_=-1,
    #             range_text=['Cosine Similarity', ''],
    #             range_color=[
    #                 "#313695",
    #                 "#4575b4",
    #                 "#74add1",
    #                 "#abd9e9",
    #                 "#e0f3f8",
    #                 "#ffffbf",
    #                 "#fee090",
    #                 "#fdae61",
    #                 "#f46d43",
    #                 "#d73027",
    #                 "#a50026",
    #             ],
    #         ),
    #     )
    #         .render("cos_sim_value_btw_genre_3dbar.html")
    # )


if __name__ == '__main__':
    electronic_data_frame = pd.read_csv("full_music_data_by_genre\\Electronic.csv")
    influence_data_frame = pd.read_csv(
        'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\influence_data.csv')
    # 1. 获取某一流派的歌曲随时间变化过程（来自full_music_data）
    # get_genre_change_line_graph('Electronic')


    # 2. 分析electronic中追随者和影响者的各指标的对比变化关系
    compare_influencer_follower_each_indicator(influence_data_frame,electronic_data_frame,'loudness')

    # 3. 计算electronic中各指标间的斯皮尔曼相关系数
    # get_pearson_corr_heatmap(electronic_data_frame)