# # scikit-learn 没有绘制树状图的功能，需借助 SciPy 库完成
# import matplotlib.pyplot as plt
# from sklearn.datasets import make_blobs
# from scipy.cluster.hierarchy import dendrogram, ward
#
#
# # 生成模拟数据
# X, y = make_blobs(n_samples=13,
#                   random_state=42
#                  )
#
# print(X)
# print(y)
#
# # 在数据组 X 上应用 ward 聚类函数，返回聚类过程中所跨越距离的数组
# linkage_array = ward(X)
# print(linkage_array)
# # 绘制树状图
# dendrogram(linkage_array)
#
# # 标记数中划分为两个和三个簇的位置
# ax = plt.gca()
# bounds = ax.get_xbound()
#
# plt.plot(bounds,
#          [27, 27],
#          '-.',
#          c='y')
# plt.plot(bounds,
#          [14, 14],
#          '-.',
#          c='y'
#         )
#
# plt.text(x=bounds[1],
#          y=27,
#          s=' two clusters',
#          va='center',
#          fontsize=15
#         )
#
# # 添加文本注释
# plt.text(x=bounds[1],
#          y=14,
#          s=' three clusters',
#          va='center',
#          fontsize=15
#         )
#
# # 调整子区布局
# plt.subplots_adjust(left=0.1,
#                     right=0.75,
#                     top=0.9,
#                     bottom=0.1
#                    )
# plt.show()
# ==============================================================================
import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage, distance
import scipy.cluster.hierarchy as hierarchy
if __name__=='__main__':
    # data_frame = pd.read_csv("E:\MCM&ICM2021\programs\cluster_raw_data.csv")
    # data_frame = pd.read_csv("E:\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_artist.csv")
    # data_frame = pd.read_csv("E:\MCM&ICM2021\\programs\\data_by_genre_pca\\mean_character_by_genre.csv")
    data_frame = pd.read_csv("data_by_genre\\mean_data_by_genre.csv")
    genre_name = data_frame['genre'].to_list()
    # id = data_frame['artist_id'].to_list()
    # label_name = []
    # for i in range(len(genre_name)):
    #     label_name.append([str(genre_name[i]) + '(id:' + str(id[i]) + ')'])
    data_frame = data_frame.iloc[:, 1:]
    # data_frame['duration_ms'] = data_frame['duration_ms']/data_frame['duration_ms'].max()
    data_frame = (data_frame - data_frame.min()) / (data_frame.max() - data_frame.min())  # 标准化
    # print(data_frame)
    disMat = distance.pdist(data_frame, metric='cosine')  # 计算距离矩阵
    # hierarchy.set_link_color_palette(['#E88872','#96DEE3','#81E3C1','#8ECDE6','#8ECDE6'])  # 设置聚类调色盘
    Z = linkage(disMat, method='ward', metric='cosine')
    # print(Z)
    ax =plt.subplot()
    colors = ['#96DEE3','#BFE3A3','#AEAFE3','#E3BCA1']
    dendrogram(Z, labels=genre_name, leaf_rotation=0, orientation='right')
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]

    plt.savefig("E:\\LatexWorkspace\\MCM2021\\Team2117189\\figures\\genre_cluster_analyze.png",dpi=500,bbox_inches = 'tight')
    plt.show()
