import pandas as pd

from programs.task1_relationship_network import search_all_nodes_in_list

problem_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data'
data_by_artist_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_artist.csv'
data_by_year_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\data_by_year.csv'
full_music_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\full_music_data.csv'
influence_data_path = 'E:\\MCM&ICM2021\\2021_MCM-ICM_Problems\\2021_ICM_Problem_D_Data\\influence_data.csv'
data_by_artist_dim_reduced = 'E:\\MCM&ICM2021\\programs\\data_by_artist_dim_reduced.csv'


def refector_artist_by_genre(influence_data_frame, include_name=False, save_to_csv=False):
    # 根据流派对艺术家进行重构
    genre_dic = {}
    # 1. 包含姓名
    # {’流派‘：[艺术家id,艺术家名称,活跃年代]}
    if include_name == True:
        for row_index, row in influence_data_frame.iterrows():
            if row['influencer_main_genre'] not in genre_dic.keys():
                genre_dic[row['influencer_main_genre']] = [
                    [row['influencer_name'], row['influencer_id'], row['influencer_active_start']]]  # 创建list
            elif [row['influencer_name'], row['influencer_id'], row['influencer_active_start']] not in genre_dic[
                row['influencer_main_genre']]:
                genre_dic[row['influencer_main_genre']].append(
                    [row['influencer_name'], row['influencer_id'], row['influencer_active_start']])

            if row['follower_main_genre'] not in genre_dic.keys():
                genre_dic[row['follower_main_genre']] = [
                    [row['follower_name'], row['follower_id'], row['follower_active_start']]]
            elif [row['follower_name'], row['follower_id'], row['follower_active_start']] not in genre_dic[
                row['follower_main_genre']]:
                genre_dic[row['follower_main_genre']].append(
                    [row['follower_name'], row['follower_id'], row['follower_active_start']])
    # 2.不包含姓名
    else:
        for row_index, row in influence_data_frame.iterrows():
            if row['influencer_main_genre'] not in genre_dic.keys():
                genre_dic[row['influencer_main_genre']] = [
                    [row['influencer_id'], row['influencer_active_start']]]  # 创建list
            elif [row['influencer_id'], row['influencer_active_start']] not in genre_dic[row['influencer_main_genre']]:
                genre_dic[row['influencer_main_genre']].append([row['influencer_id'], row['influencer_active_start']])

            if row['follower_main_genre'] not in genre_dic.keys():
                genre_dic[row['follower_main_genre']] = [[row['follower_id'], row['follower_active_start']]]
            elif [row['follower_id'], row['follower_active_start']] not in genre_dic[row['follower_main_genre']]:
                genre_dic[row['follower_main_genre']].append([row['follower_id'], row['follower_active_start']])
    if save_to_csv == True:
        for key in genre_dic.keys():
            export_data_frame = pd.DataFrame(genre_dic[key], columns=['artist_names', 'id', 'active_start_years'])
            key = key.replace("/", '_')
            export_data_frame.to_csv(".\\artist_by_genre\\" + key + ".csv")
    return genre_dic


def get_artist_by_genre(influence_data_frame, artist_data_frame, genre_export, pca=False):
    # 艺术家id 艺术家姓名 <年代> < 音乐特征...>
    export_list = []
    loop_count = 0
    genre_dic = refector_artist_by_genre(influence_data_frame)  # 以流派为索引对艺术家进行分类 {’流派‘：[艺术家id,艺术家名称]}
    # print(genre_dic)
    print(genre_dic.keys())
    # 得到流派分类后，根据流派内艺术家的id去data_by_artist.csv中找对应的参数
    if pca == True:
        for elem in genre_dic[genre_export]:  # 根据id找索引，再得到信息
            loop_count += 1
            print("进度:", loop_count / len(genre_dic[genre_export]) * 100, '%')
            artist_data_list = artist_data_frame['artist_id'].to_list()
            all_index = search_all_nodes_in_list(artist_data_list, elem[0])
            for index in all_index:
                artist_info = [elem[0], artist_data_frame.loc[index, 'artist_name'], elem[1],
                               artist_data_frame.loc[index, 'danceability'],
                               artist_data_frame.loc[index, 'energy'],
                               artist_data_frame.loc[index, 'valence'],
                               artist_data_frame.loc[index, 'tempo'],
                               artist_data_frame.loc[index, 'loudness'],
                               artist_data_frame.loc[index, 'mode'],
                               artist_data_frame.loc[index, 'key'],
                               artist_data_frame.loc[index, 'acousticness']
                               ]
                # print(artist_info)
                export_list.append(artist_info)
            export_data_frame = pd.DataFrame(export_list,
                                             columns=['id', 'name', 'active_year', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5',
                                                      'pc6', 'pc7',
                                                      'pc8'])
        genre_export = genre_export.replace("/", '_')
        export_data_frame.to_csv(genre_export + '_artist_data_pca.csv')
    else:
        for elem in genre_dic[genre_export]:  # 根据id找索引，再得到信息
            loop_count += 1
            print("进度:", round(loop_count / len(genre_dic[genre_export]) * 100, 2), '%')
            artist_data_list = artist_data_frame['artist_id'].to_list()
            all_index = search_all_nodes_in_list(artist_data_list, elem[0])
            for index in all_index:
                artist_info = [elem[0], artist_data_frame.loc[index, 'artist_name'], elem[1],
                               artist_data_frame.loc[index, 'danceability'],
                               artist_data_frame.loc[index, 'energy'],
                               artist_data_frame.loc[index, 'valence'],
                               artist_data_frame.loc[index, 'tempo'],
                               artist_data_frame.loc[index, 'loudness'],
                               artist_data_frame.loc[index, 'mode'],
                               artist_data_frame.loc[index, 'key'],
                               artist_data_frame.loc[index, 'acousticness'],
                               artist_data_frame.loc[index, 'instrumentalness'],
                               artist_data_frame.loc[index, 'liveness'],
                               artist_data_frame.loc[index, 'speechiness'],
                               artist_data_frame.loc[index, 'duration_ms'],
                               artist_data_frame.loc[index, 'popularity'],
                               artist_data_frame.loc[index, 'count']
                               ]
                export_list.append(artist_info)
            export_data_frame = pd.DataFrame(export_list,
                                             columns=['id', 'name', 'year', 'danceability', 'energy', 'valence',
                                                      'tempo',
                                                      'loudness', 'mode', 'key', 'acousticness', 'instrumentalness',
                                                      'liveness', 'speechiness', 'duration_ms', 'popularity', 'count'])
        genre_export = genre_export.replace("/", '_')
        export_data_frame.to_csv(".\\data_by_genre\\" + genre_export + '_artist_data.csv')


if __name__ == "__main__":
    artist_data_frame_dim_reduced = pd.read_csv(data_by_artist_dim_reduced, encoding='ANSI')
    artist_data_frame = pd.read_csv(data_by_artist_path, encoding='utf-8')
    influence_data_frame = pd.read_csv(influence_data_path, encoding='utf-8')

    # genre_dic = refector_artist_by_genre(influence_data_frame, include_name=True, save_to_csv=True)
    # for key,values in genre_dic.items():
    #     print(key+':','*'*20)
    #     for value in values:
    #         print(value)

    genre_export = "Jazz"
    # get_artist_by_genre(influence_data_frame, artist_data_frame, genre_export,pca=False)
