import pandas as pd
import dateparser


def pd_df_builder(news, news_dict):
    
    titles = [keys for keys in news_dict.keys()]
    news_data = []

    for i in range(0,len(news)):
        if news[i]["title"] in titles:        
            news_data.extend([[news[i]["title"],news[i]["link"],news_dict[news[i]["title"]],news[i]["pubDate"]]])
             
    df = pd.DataFrame(news_data,columns = ['Title','URL',"Original Content","Publication Date"])
    

    years = []
    months = []
    days  = []

    for idx in range(len(df['Title'])):
        pub_date = dateparser.parse(df['Publication Date'][idx])
        years.append(pub_date.year)
        months.append(pub_date.month)
        days.append(pub_date.day)    
    
    df['pub_Year'] = pd.Series(years)
    df['pub_Month'] = pd.Series(months)
    df['pub_Day'] = pd.Series(days)
    
    return df
