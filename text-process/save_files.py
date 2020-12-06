import pandas as pd


azenews_df['Cleaned-Enhanced Content'] = pd.Series([clean_enhance_text(azenews_df['Original Content'][i]) for i in range(len(azenews_df))])
armnews_df['Cleaned-Enhanced Content'] = pd.Series([clean_enhance_text(armnews_df['Original Content'][i]) for i in range(len(armnews_df))])

azenews_df.to_csv(r'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\azenews_df.csv', index = False, header=True)
armnews_df.to_csv(r'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\armnews_df.csv', index = False, header=True)

[azenews_df,aze_cluster_descript] = clustering(azenews_df)   # save aze and arm cluster descrs too, to withdraw them later
[armnews_df,arm_cluster_descript] = clustering(armnews_df)

azenews_df.to_csv(r'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\azenews_df_clustered.csv', index = False, header=True)
armnews_df.to_csv(r'C:\Users\tahir\11 GlobalDefTech Hackathon\deployment\armnews_df_clustered.csv', index = False, header=True)
