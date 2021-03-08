import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Graph
import numpy as np

from programs.task1_relationship_network import name_not_in_nodes, is_not_leaf_node


def get_subnetwork(influence_data_frame, artist_name, node_max_num=200):
    """limit chain length = 2"""
    influencer_queue = []  # create a queue
    influencer_queue.extend([artist_name])
    flag = np.zeros(len(influence_data_frame['influencer_id']))  # 防止出现回环
    nodes = []
    symbolSize = influence_data_frame['influencer_name'].to_list().count(artist_name) / 2
    nodes.extend(
        [
            {
                "name": artist_name,
                "symbolSize": symbolSize,
                "draggable": "False",
                "value": 1,
                "category": artist_name,
            },
        ]
    )
    links = []
    categories = [{"name": artist_name}]
    index = 0
    influencer_list = influence_data_frame['influencer_name'].to_list()
    while len(influencer_queue) != 0:
        print(len(influencer_queue))
        if influencer_queue[0] in influencer_list[index + 1:-1]:
            index = influencer_list.index(influencer_queue[0], index + 1, -1)
            if influencer_queue[0] == influence_data_frame.loc[index, 'influencer_name']:
                follower_name = influence_data_frame.loc[index, 'follower_name']
                if name_not_in_nodes(nodes, follower_name):
                    links.append(
                        {
                            "source": influencer_queue[0],
                            "target": follower_name,
                            "symbol":['none','arrow'],
                            "symbolSize":3
                        })
                    if is_not_leaf_node(links, artist_name, follower_name):
                        node_size = (influence_data_frame['influencer_name'].to_list().count(follower_name) / 2) + 3
                        category = follower_name
                    else:
                        node_size = 3
                        category = influencer_queue[0]
                    nodes.append(
                        {
                            "name": follower_name,
                            "symbolSize": node_size,
                            "draggable": "False",
                            "value": 0,
                            "category": influencer_queue[0],
                            # "
                        },
                    )
                    if follower_name not in influencer_queue and flag[index] != 1 and is_not_leaf_node(links,
                                                                                                       artist_name,
                                                                                                       follower_name):
                        influencer_queue.append(follower_name)  # push queue
                        categories.append(
                            {
                                "name": follower_name
                            }
                        )
                        flag[index] = 1
        else:
            influencer_queue.pop(0)  # pop queue
            index = 0
    return nodes, links, categories


"""
创建某位艺术家的子关系网，递归到被影响者没有被影响者为止
"""
problem_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data'
data_by_artist_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_artist.csv'
data_by_year_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_year.csv'
full_music_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\full_music_data.csv'
influence_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\influence_data.csv'
# artist_name1 = 'Bob Dylan'
artist_name = "Alice in Chains"
# artist_name1 = 'The Beatles'


if __name__ == '__main__':
    influence_data_frame = pd.read_csv(influence_data_path, encoding='utf-8')
    nodes, links, categories = get_subnetwork(influence_data_frame, artist_name)

    (
        Graph(init_opts=opts.InitOpts(bg_color='#ffffff', width="1000px", height="600px"))
            .add(
            "",
            nodes,
            links,
            categories,
            repulsion=50,
            layout='force',
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.1, width=0.6),
            is_rotate_label=True,
            label_opts=opts.LabelOpts(is_show=True,position="middle",font_size=8)
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-关系图"),
        )
            .render("htmls\\"+artist_name + "_sub_network.html")
    )
