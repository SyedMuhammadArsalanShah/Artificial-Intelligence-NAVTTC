import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.compose import  ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model  import LinearRegression
from sklearn.tree  import DecisionTreeRegressor
from sklearn.ensemble  import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error


# 1 load dataset 
housing= pd.read_csv("housing.csv")
# 2 creaate a stratified col 
housing["income_cat"]=pd.cut(housing["median_income"],bins=[0.0, 1.5, 3.0, 4.5, 6, np.inf], labels=[1,2,3,4,5])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2,random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strata_train=housing.loc[train_index].drop("income_cat",axis=1)
    strata_test=housing.loc[test_index].drop("income_cat",axis=1)

housing=strata_train.copy()


# 3 sepration of labels and features
housing_label=housing["median_house_value"].copy()

housing=housing.drop("median_house_value",axis=1)

# 4 separate  num and cat
num_attr= housing.drop("ocean_proximity",axis=1).columns.tolist()
cat_attr=["ocean_proximity"]

# 5 pipelines

num_pipelines=Pipeline([
 ("impute",SimpleImputer(strategy="median")),
 ("scalar",StandardScaler()),

])

cat_pipelines=Pipeline([

 ("onehot",OneHotEncoder(handle_unknown="ignore")),

])

# full pipeline

full_pipeline=ColumnTransformer([
 ("num", num_pipelines, num_attr),
 ("cat", cat_pipelines, cat_attr),

])

housing_prepared= full_pipeline.fit_transform(housing)

print(housing_prepared.shape)



lin_reg= LinearRegression()
lin_reg.fit(housing_prepared,housing_label)

tree_reg= DecisionTreeRegressor(random_state=42)
tree_reg.fit(housing_prepared,housing_label)



forest_reg= RandomForestRegressor(random_state=42)
forest_reg.fit(housing_prepared,housing_label)



lin_predicts=lin_reg.predict(housing_prepared)
tree_predicts=tree_reg.predict(housing_prepared)
forest_predicts=forest_reg.predict(housing_prepared)


lin_rmse=root_mean_squared_error(housing_label, lin_predicts)
tree_rmse=root_mean_squared_error(housing_label, tree_predicts)
forest_rmse=root_mean_squared_error(housing_label, forest_predicts)



print("Linear",lin_rmse)
print("Dec",tree_rmse)
print("Fore",forest_rmse)