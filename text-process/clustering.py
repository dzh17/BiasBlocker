from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.cluster import KMeans
import pandas as pd
import nltk
from nltk import word_tokenize, sent_tokenize          


def clustering(df,true_k):
    
    # removing the rows where NaN values are present under any of columns
    df = df.dropna() 
    df = df.reset_index(drop=True)
    
    titles = [df['Title'][i] for i in range(len(df)) if df['Cleaned-Enhanced Content'].isnull().values[i]==False]
    cln_content = [df['Cleaned-Enhanced Content'][i] for i in range(len(df)) if df['Cleaned-Enhanced Content'].isnull().values[i]==False]
                 
    vectorizer = TfidfVectorizer(stop_words={'english'})
    vec_cln_content = vectorizer.fit_transform(cln_content)
                 
    
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
    model.fit(vec_cln_content)
    labels=model.labels_
    content_cls=pd.DataFrame(list(zip(titles,labels)),columns=['Title','Cluster'])
    print(content_cls.sort_values(by=['Cluster']))
    
              
    updated_df = pd.merge(df, content_cls,on='Title')                 
    for i in range(true_k):
        print(f" The number of news articles in a cluster {i} is {sum(updated_df['Cluster']==i)}")
                 
    lem = nltk.WordNetLemmatizer()
    cluster = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    keys = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14"]
    values = [cluster[i] for i in range(true_k)]
    cluster_descript = {}
    
    for cluster_num in range(true_k):
        for news_num in range(len(updated_df['Title'])):
            if updated_df['Cluster'][news_num] == cluster_num:
                clear_content  = [word for word in word_tokenize(updated_df['Cleaned-Enhanced Content'][news_num])]
                cluster[cluster_num].extend(clear_content)
            else:
                continue
                
        cluster[cluster_num] = list(set(cluster[cluster_num]))
        temp_dict = {keys[cluster_num]:cluster[cluster_num]}
        cluster_descript.update(temp_dict)

    
    return [updated_df,cluster_descript]
