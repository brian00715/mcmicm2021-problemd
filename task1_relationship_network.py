import math

import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph

problem_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data'
data_by_artist_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_artist.csv'
data_by_year_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_year.csv'
full_music_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\full_music_data.csv'
influence_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\influence_data.csv'


def name_not_in_nodes(nodes, value):
    if nodes is None:
        return True
    for node in nodes:
        if node['name'] == value:
            return False
    return True


def is_not_leaf_node(links, root_node_name, node_name):
    for link in links:
        if node_name == link['target']:
            if link['source'] == root_node_name:
                return True
            else:
                return False



def get_relationship_network(influence_data_frame,node_limit = 10000):
    nodes = []
    links = []
    categories = []
    node_num = 501
    slide = np.arange(0, math.pi, math.pi / node_num)
    x = 500 * np.cos(slide)
    y = 500 * np.sin(slide)
    index_count = 0
    for row_index, row in influence_data_frame.iterrows():
        if index_count == node_limit:
            break
        if row_index < 0 or row_index > 40000:
            continue
        else:
            index_count += 1
        if name_not_in_nodes(nodes, row['influencer_name']):
            influencer_node_size = influence_data_frame['influencer_name'].to_list()[:node_limit].count(row['influencer_name'])
            # if (influencer_node_size < 20 or influencer_node_size > 500):
            #     continue
            nodes.append(
                {
                    "name": row['influencer_name'],
                    # "x":x[row_index],
                    # "y":y[row_index],
                    # "id":row['influencer_id'],
                    "symbolSize": influencer_node_size ,
                    "draggable": "False",
                    "value": 1,
                    "category": row['influencer_name'],

                },
            )
        if name_not_in_nodes(nodes, row['follower_name']):
            node_size = influence_data_frame['influencer_name'].to_list()[node_limit].count(row['follower_name'])
            nodes.append(
                {
                    "name": row['follower_name'],
                    # "id": row['follower_id'],
                    # "draggable": "False",
                    "symbolSize": node_size,
                    "value": 0,
                    "category": row['influencer_name'],
                }
            )
        links.append(
            {
                "source": row['influencer_name'],
                "target": row['follower_name'],
                "value": influencer_node_size,
                # "linestyle_opts":opts.LineStyleOpts(width=1)
                "symbol":['none','arrow'],
                "symbolSize":3

            }
        )
        if name_not_in_nodes(categories, row['influencer_name']):
            categories.append(
                {
                    "name": row['influencer_name'],
                }
            )
    print(len(nodes))
    (
        Graph(init_opts=opts.InitOpts(width="1000px", height='600px'))
            .add(
            "",
            nodes,
            links,
            categories,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(color='source', curve=0.1, width=0.5, opacity=0.7),
            label_opts=opts.LabelOpts(is_show=False, font_weight=0.2),
            is_rotate_label=True,
            # is_roam=True,
            # is_focusnode=True,
            layout='force',
            # linestyle_opts=opts.LineStyleOpts(color="source", curve=0.1),
            # label_opts=opts.LabelOpts(position="right"),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            # legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
            title_opts=opts.TitleOpts(title="Graph-关系图"),

        )
            .render("relationship_network.html")
    )


def search_all_nodes_in_list(list, node):
    """search node in list"""
    all_index = []
    index = 0
    while node in list[index:-1]:
        index = list.index(node, index, -1)
        all_index.append(index)
        index += 1
    return all_index


def get_music_influence(data_frame, num=42669):
    result = [[]]
    for row_index, row in data_frame.iterrows():
        print("进度:%.3f%%" % ((row_index + 1) / num * 100))
        if row['influencer_id'] in result[:][0]:
            continue
        temp = []
        temp.append(row['influencer_id'])
        if row_index == num:
            break
        direct_influence_num = data_frame['influencer_name'].to_list()[0:num].count(row['influencer_name'])
        indirect_influence_num = 0
        different_genre_num = 0  # 流派不同的人数
        max_year_period = 0  # 影响的年代数
        max_year = row['influencer_active_start']
        all_index = search_all_nodes_in_list(data_frame['influencer_name'].to_list()[0:num], row['influencer_name'])
        for index in all_index:  # 找到所有的influencer，即他们的follower
            if row['influencer_main_genre'] != data_frame.loc[index, 'influencer_main_genre']:
                different_genre_num += 1
            if data_frame.loc[index, 'follower_active_start'] > row['follower_active_start']:
                max_year = data_frame.loc[index, 'follower_active_start']
            follower_name = data_frame.loc[index, 'follower_name']
            indirect_influence_num += data_frame['influencer_name'].to_list().count(follower_name)
            all_follower_index = search_all_nodes_in_list(data_frame['influencer_name'].to_list(), follower_name)
            for follower_index in all_follower_index:  # follower的follower
                if data_frame.loc[follower_index, 'follower_active_start'] > row['follower_active_start']:
                    max_year = data_frame.loc[follower_index, 'follower_active_start']
                if row['influencer_main_genre'] != data_frame.loc[follower_index, 'influencer_main_genre']:
                    different_genre_num += 1
        max_year_period = max_year - row['influencer_active_start']
        temp.append(direct_influence_num)
        temp.append(indirect_influence_num)
        temp.append(different_genre_num)
        temp.append(max_year_period)
        temp.append(row['influencer_active_start'])
        result.append(temp)
    # print(result)
    export_frame = pd.DataFrame(result,
                                columns=['id', 'direct_influence_num', 'indirect_influence_num', 'different_genre_num',
                                         'max_year_period', 'influencer_active_start'])
    export_frame.to_csv("music_influence.csv")


if __name__ == '__main__':
    data_frame = pd.read_csv(influence_data_path, encoding='utf-8')
    get_relationship_network(data_frame,node_limit=2500)
    # get_music_influence(data_frame)

