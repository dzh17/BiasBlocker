
from clean_enhance import *
from clustering import *
from pd_df_builder import *
from read_data import *
import numpy as np

def df_prep(country,k_means):

    # read_data.py

    #news = read_data(f'{country}_summary.json')  
    #news_dict = get_dictionary(news)

    # pd_df_builder.py
    
    #news_df = pd_df_builder(news, news_dict) 

    # clean_enhance.py

    #news_df['Cleaned-Enhanced Content'] = pd.Series([clean(news_df['Original Content'][i]) for i in range(len(news_df))])
    #news_df.to_csv(rf'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\{country}news_df.csv', index = False, header=True)
    news_df = pd.read_csv(rf'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\{country}news_df.csv')

    # clustering.py 

    #[news_df,cluster_descript] = clustering(news_df,k_means)   # save aze and arm cluster descrs too, to withdraw them later
    #np.save('cluster_descript.npy', cluster_descript) 
    #news_df.to_csv(rf'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\{country}news_df_clustered.csv', index = False, header=True)
    
    news_df = pd.read_csv(rf'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\{country}news_df_clustered.csv')
    cluster_descript = np.load('cluster_descript.npy',allow_pickle='TRUE').item()

    print(news_df)
    
    return [news_df,cluster_descript]