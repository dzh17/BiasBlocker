
from news_scrapper_clusterizer import *
from similarity_test import *
from df_prep import *

def relevance(country,URL,N_news,k_means):

    # df_prep.py
    
    [news_df,cluster_descript] = df_prep(country,k_means)

    # news_scrapper_clusterizer.py
    
    [news_orig, news_year,news_month,news_day] = scrapper(URL)
    [news_norm,cluster] = clusterizer(news_orig,cluster_descript,k_means)

    # similarity_test.py
    current_news = [news_norm,news_year,news_month,news_day]
    curntnews_simnews = sim_cont_identifier(current_news,cluster,news_df, N_news)



    return curntnews_simnews[news_norm]