import pandas as pd 
import glob 

# read in data frame and merge
df_att = pd.read_csv('player_stats_att.csv')
df_def = pd.read_csv('player_stats_def.csv')
df_gen = pd.read_csv('player_stats_gen.csv')

cols_to_use2 = df_def.columns.difference(df_att.columns)
merged_df2 = pd.merge(df_att, df_def[cols_to_use2], left_index=True, right_index=True, how='outer')
cols_to_use = df_gen.columns.difference(merged_df2.columns)
merged_df = pd.merge(merged_df2, df_gen[cols_to_use], left_index=True, right_index=True, how='outer')

# drop column not related to shots taken or assists made
merged_df = merged_df.drop(columns=['LFS','RFS','HS','CK','FK','F'])

merged_df.to_csv('merged_df.csv', index=False)

print(merged_df)