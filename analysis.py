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

merged_df.head()
merged_df.info()

# drop column not related to shots taken or assists made
merged_df = merged_df.drop(columns=['LFS','RFS','HS','CK','FK','F','XG-G','PKG','SHT%','KP','AD','AD%','G+A','FC','FS','RC','YC'])
merged_df = merged_df.rename(columns={'G':'GOALS','xG':'EXPECTED_GOALS','S':'SHOTS','SOT':'SHOTS_ON_TARGET','A':'ASSISTS',
                                      'OFF':'OFFSIDE','T':'TOCHES','GA':'GOALS_AGAINST','XGA':'EXPECTED_GOALS_AGAINST','CLR':'CLEARANCE','PKA':'PENALTY_KICKS_TAKEN'})merged_df.head()

from sklearn.model_selection import train_test_split # type: ignore

x = merged_df.drop(columns='SHOTS')
y = merged_df['SHOTS']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, stratify=y, random_state=8)

from sklearn.pipeline import Pipeline
from category_encoders.target_encoder import TargetEncoder
from xgboost import XGBClassifier

estimators = [
    ('encoder', TargetEncoder()),
    ('clf',XGBClassifier(random_state=8))
]

pipe = Pipeline(steps=estimators)
pipe 
