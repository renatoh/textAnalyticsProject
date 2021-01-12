import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, k_means
import matplotlib.pyplot as plt

from nltk.stem import PorterStemmer

# path = '../resources/example-entities.csv'
from StemmedTfidfVectorizer import StemmedTfidfVectorizer
from process_clusters import write_clusters_to_file

path_entities = '../resources/entity_vectors_all.csv'

path_top_entities = 'top_entities_per_month.csv'

# path = '../resources/entity_vectors_all.csv'
# path = '../resources/entity_vectors_50.csv'
# df = pd.read_csv(path, encoding='utf-8')
df = pd.read_csv(path_entities)

# df['stemmed'] = df['entities'].apply(lambda x: [ps.stem(y) for y in x.split()])
# df['stemmed']
# print(textes)

textes = df['entities']
vectorizer = StemmedTfidfVectorizer(ngram_range=(1, 1), stop_words='english')

vectors = vectorizer.fit_transform(textes)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
dense_list = dense.tolist()

print("Tfidf-Vectors created")
# df = pd.DataFrame(dense_list, columns=feature_names)

number_clusters = 40
# k_means_values = []
# cluster_sizes = range(20,81,5)

# for cluster_size in cluster_sizes:
#     k = k_means(dense_list, n_clusters=cluster_size, verbose=False)[2]
#     # kmean_value = calc_kmean(cluster_size,dense_list)
#     print("k_mean for cluster_size %s is %s" % (cluster_size,k))
#     k_means_values.append(k)
#
#

# plt.plot(k_means_values,cluster_sizes)
# plt.show()


# calc_kmean(number_clusters, dense_list)


kmeans = KMeans(n_clusters=number_clusters, random_state=0)
predictions = kmeans.fit_predict(dense_list)

cluster_groups = {}
for i, m in enumerate(kmeans.labels_):
    month_in_cluster = cluster_groups.get(m, [])
    month_in_cluster.append(df['month'].loc[i])
    cluster_groups[m] = month_in_cluster;

    print('cluster:' + str(m) + 'doc-index:' + str(i) + ' which is month' + str(df['month'].loc[i]))

    # df['Mont'].loc[i]

write_clusters_to_file(cluster_groups)

# for k, item in cluster_groups.items():
#     print(item)
#     all_features_for_month_cluster = readAndCombineTopEntities(item)



# print(cluster_groups)
