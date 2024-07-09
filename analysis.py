import pandas as pd 
import glob
import numpy as np

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
merged_df = merged_df.drop(columns=['LFS','RFS','HS','CK','FK','F','XG-G','PKG','SHT%','KP','AD','AD%'
                                    ,'G+A','FC','FS','RC','YC'])
merged_df = merged_df.rename(columns={'G':'GOALS','xG':'EXPECTED_GOALS','S':'SHOTS','SOT':'SHOTS_ON_TARGET',
                                      'A':'ASSISTS','OFF':'OFFSIDE','T':'TOUCHES','GA':'GOALS_AGAINST',
                                      'XGA':'EXPECTED_GOALS_AGAINST','CLR':'CLEARANCE',
                                      'PKA':'PENALTY_KICKS_TAKEN'})
#merged_df.to_csv('merged_df.csv', index=False)

# need to create column into one dimensional array for data split - using SHOTS column for now
merged_df['result'] = np.where(merged_df['SHOTS'] >= 1, 1, 0)

from sklearn.model_selection import train_test_split # type: ignore

X = merged_df.drop(columns=['SHOTS','result'])
y = merged_df['result']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, stratify=y, random_state=8)

from sklearn.pipeline import Pipeline
from category_encoders.target_encoder import TargetEncoder
from xgboost import XGBClassifier

estimators = [
    ('encoder', TargetEncoder()),
    ('clf',XGBClassifier(random_state=8))
]

pipe = Pipeline(steps=estimators)
print(pipe)

from skopt import BayesSearchCV 
from skopt.space import Real, Categorical, Integer

search_space = {
    'clf__max_depth': Integer(2,8),
    'clf__learning_rate': Real(0.001, 1.0, prior='log-uniform'),
    'clf__subsample': Real(0.5, 1.0),
    'clf__colsample_bytree': Real(0.5, 1.0),
    'clf__colsample_bylevel': Real(0.5, 1.0),
    'clf__colsample_bynode': Real(0.5, 1.0),
    'clf__reg_alpha': Real(0.0, 10.0),
    'clf__reg_lambda': Real(0.0, 10.0),
    'clf__gamma': Real(0.0, 10.0)
}

opt = BayesSearchCV(pipe, search_space, cv=5, n_iter=11, scoring='roc_auc', random_state=8)

opt.fit(X_train,y_train)

print(opt.best_estimator_)
print(opt.best_score_)
print(opt.score(X_test,y_test))

from xgboost import plot_importance

xgboost_step = opt.best_estimator_.steps[1]
xgboost_model = xgboost_step[1]
print(plot_importance(xgboost_model))

