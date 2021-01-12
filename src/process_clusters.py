import pandas as pd
import ast
import pickle

path_top_entities = '../resources/top_entities_per_month.csv'

import csv

top_entities_df = pd.read_csv(path_top_entities)
cluster_map_path = '../resources/month_cluster.pkl'


def mergeDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = value + dict1[key]
    return dict3


print(top_entities_df.month)


def readAndCombineTopEntities(months_list):
    months_from_csv = dict(zip(top_entities_df['month'], top_entities_df['entities']))

    print(months_from_csv)

    merged_map = {}
    for month in months_list:

        if months_from_csv[month] is None:
            print("no entry found for month %s in file %s", month, path_top_entities)

        month_dic = ast.literal_eval(months_from_csv[month])
        merged_map = mergeDict(merged_map, month_dic)
    #TODO: return entities per month and aggregated entities
    return merged_map


def write_clusters_to_file(month_clusters):
    f = open(cluster_map_path, 'wb')
    pickle.dump(month_clusters, f)
    f.close()


def read_cluster_from_file():
    month_cluster = pickle.load(open(cluster_map_path, "rb"))
    return month_cluster


dict_from_file = read_cluster_from_file()

for k, item in dict_from_file.items():
    print(item)
    all_features_for_month_cluster = readAndCombineTopEntities(item)

print(all_features_for_month_cluster)