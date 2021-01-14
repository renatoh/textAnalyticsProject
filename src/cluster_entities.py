import pandas as pd
from sklearn.cluster import KMeans, k_means

from StemmedTfidfVectorizer import StemmedTfidfVectorizer
from process_clusters import write_clusters_to_file

path_entities = '../resources/entity_vectors_all.csv'

path_top_entities = 'top_entities_per_month.csv'

df = pd.read_csv(path_entities)



textes = df['entities']
vectorizer = StemmedTfidfVectorizer(ngram_range=(1, 1), stop_words='english')

vectors = vectorizer.fit_transform(textes)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
dense_list = dense.tolist()

print("Tfidf-Vectors created")

number_clusters = 40



kmeans = KMeans(n_clusters=number_clusters, random_state=0)
predictions = kmeans.fit_predict(dense_list)

cluster_groups = {}
for i, m in enumerate(kmeans.labels_):
    month_in_cluster = cluster_groups.get(m, [])
    month_in_cluster.append(df['month'].loc[i])
    cluster_groups[m] = month_in_cluster

    print('cluster:' + str(m) + 'doc-index:' + str(i) + ' which is month' + str(df['month'].loc[i]))



write_clusters_to_file(cluster_groups)
