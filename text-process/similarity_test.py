from nltk import word_tokenize, sent_tokenize   
from datetime import date       


def simil_test_1(text1,text2):
       
    global score
    text1 = word_tokenize(text1)
    text2 = word_tokenize(text2)
    num_common = 0
    
    for word in text1:
        if word in text2:
            num_common += 1 
    
    if len(text1) != 0 and len(text2) != 0:
        metric1 = num_common / len(text1)
        metric2 = num_common / len(text2)
    
        if len(text1)/len(text2) < 0.5 :
            weight = len(text1)/len(text2)
            score = (1-weight)*metric1 + weight*metric2
        elif 0.5 < len(text1)/len(text2) < 1:
            weight = len(text1)/len(text2)
            score = metric1 + weight*metric2
        elif len(text2)/len(text1) < 0.5 :
            weight = len(text2)/len(text1)
            score = (1-weight)*metric1 + weight*metric2
        elif 0.5 < len(text2)/len(text1) < 1 :
            weight = len(text2)/len(text1)
            score = metric1 + weight*metric2
        else:
            score = 0
            
    score = round(score,5)

    
    return score 
    
    
def simil_test_2(text1,text2):
    
    global score
    num_common = 0
    text1 = word_tokenize(text1)
    text2 = word_tokenize(text2)
    
    for word in text1:
        if word in text2:
            num_common += 1 
    
    if len(text1) != 0 and len(text2) != 0:
        metric1 = num_common / len(text1)
        metric2 = num_common / len(text2)
    
        score = metric1 + metric2         
    else:
        score = 0

    score = round(score,5)
    
    return score 

def N_maxes(lst1, N): 
    
    N_maxes = [] 
    lst = lst1.copy()
    
  
    for i in range(N):  
        max1 = 0
          
        for j in range(len(lst)):      
            if lst[j] > max1: 
                max1 = lst[j]
                  
        if max1 in lst:
            lst.remove(max1) 
        else:
            print("Blat noooldu alaaaa?")
        
        N_maxes.append(max1) 
          
    return N_maxes

# def pubdate_restrictor(ymd,df):
    
#     condition1 = (df['pub_Year']==ymd[0]) 
#     condition2 = (df['pub_Month']==ymd[1]) 
#     condition3 = (df['pub_Day'] >= ymd[2]-3)
#     condition4 = (df['pub_Day'] <= ymd[2]+3)
#     result = condition1 & condition2 & condition3 & condition4 
    
#     return result
  
def sim_cont_identifier(news_ymd,cluster_num, df, N):

    ymd = news_ymd[1:4]
    #temp = pubdate_restrictor(ymd,df)
    #clstr_df = df.loc[ df['Cluster'] == cluster_num & (df['pub_Year']==ymd[0]) & (df['pub_Month']==ymd[1]) & (df['pub_Day'] >= ymd[2]-3) & (df['pub_Day'] <= ymd[2]+3) ]
    fit_idxs = []
    for idx in range(len(df['pub_Day'])):
        temp1 = date(df['pub_Year'][idx],df['pub_Month'][idx],df['pub_Day'][idx]) 
        temp2 = date(ymd[0],ymd[1],ymd[2])
        temp = temp1 - temp2
        diff = abs(temp.days)
        if (df['Cluster'][idx] == cluster_num) & (diff <= 3) :
            fit_idxs.append(idx) 
    
    sim_content_full = []
    metric = []
    
    
    for idx in fit_idxs:
        txt = df['Cleaned-Enhanced Content'][idx]
        #print("The current news pubdate: {}".format(ymd),'\t\t\t',"The processed news pudlication Day {}".format([df['pub_Year'][idx],df['pub_Month'][idx],df['pub_Day'][idx]]))                     
        value = simil_test_2(news_ymd[0],txt)        # here we can try simil_test_2 and compare with results of simil_test1
        metric.append(value) 

    maxes = N_maxes(metric,N)
    templst1 = [metric.index(maxes[i]) for i in range(N)]
    templst2 = fit_idxs
    max_ids = [templst2[templst1[i]] for i in range(N)]
    
    for idx in max_ids:
        sim_content_full.append(df['Original Content'][idx])   # here we have to decide what's shown, a title or a content
    
    curntnews_simnews = {news_ymd[0]:sim_content_full}
    
    
    return curntnews_simnews
