import os 
import pandas as pd
import joblib


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



MODEL_FILE="model.pkl"
PIPELINE_FILE="pipeline.pkl"


def build_pipeline(num_attr,cat_attr):
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
    return full_pipeline


if not os.path.exists(MODEL_FILE):
    # 1 load dataset 
    housing= pd.read_csv("housing.csv")
    # 2 creaate a stratified col 
    housing["income_cat"]=pd.cut(housing["median_income"],bins=[0.0, 1.5, 3.0, 4.5, 6, np.inf], labels=[1,2,3,4,5])
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2,random_state=42)
    for train_index, _ in split.split(housing, housing["income_cat"]):
        housing=housing.loc[train_index].drop("income_cat",axis=1)

    # 3 sepration of labels and features
    housing_label=housing["median_house_value"].copy()
    # feature data
    housing=housing.drop("median_house_value",axis=1)

        # 4 separate  num and cat
    num_attr= housing.drop("ocean_proximity",axis=1).columns.tolist()
    cat_attr=["ocean_proximity"]
    
    pipeline=build_pipeline(num_attr=num_attr,cat_attr=cat_attr)
    housing_prepared=pipeline.fit_transform(housing)

    model=RandomForestRegressor(random_state=42)
    model.fit(housing_prepared,housing_label)

    joblib.dump(model,MODEL_FILE)
    joblib.dump(pipeline,PIPELINE_FILE)
    print("congrats model saved")

else:
    model=joblib.load(MODEL_FILE)
    pipeline=joblib.load(PIPELINE_FILE)
    input_data=pd.read_csv("input.csv")
    transform_input=pipeline.transform(input_data)
    predictions=model.predict(transform_input)
    input_data["median_house_value"]=predictions
    input_data.to_csv("ouput.csv",index=False)
    print("congrats for output labels")